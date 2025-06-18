import subprocess
import logging
import os
import sqlite3
import re
import time
import textwrap
import difflib
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple
from abc import ABC, abstractmethod

import pandas as pd

import pymysql
from pymysql import Connection as MySQLConnection
from pymysql import Error as MySQLError

import psycopg2
from psycopg2._psycopg import connection as PGSQLConnection
from psycopg2 import Error as PGSQLError

from execution_result import ExecutionResult

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class DatabaseSystem(ABC):
    @property
    @abstractmethod
    def config(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def get_connection(cls, db_config=config):
        pass

    @classmethod
    @abstractmethod
    def connect(cls, db_config: Dict[str, Any], db_name: Optional[str] = None):
        pass

    @classmethod
    @abstractmethod
    def execute(cls, sql: str, db_config=config) -> ExecutionResult:
        pass

    @classmethod
    def close(cls, db_name: str = None):
        pass


class MySQLDatabaseSystem(DatabaseSystem):
    config = {
        "host": "127.0.0.1",
        "port": 13306,
        "user": "root",
        "password": "mysql_root_password",
        "db_name": "mysql",
    }

    _connections = {}  # Use a more generic name

    @classmethod
    def get_connection(
        cls, db_config=config
    ) -> Tuple[Optional[MySQLConnection], Optional[str]]:
        db_name = db_config["db_name"]
        connection = cls._connections.get(db_name)

        if connection is None:
            logging.info(f"Attempting to connect to MySQL database: {db_name}")
            try:
                connection = pymysql.connect(
                    database=db_config["db_name"],
                    user=db_config["user"],
                    password=db_config["password"],
                    host=db_config["host"],
                    port=int(db_config["port"]),
                )
                cls._connections[db_name] = connection
                logging.info(f"Successfully connected to MySQL database: {db_name}")
            except MySQLError as e:
                logging.error(
                    f"Error while connecting to MySQL database '{db_name}': {e}"
                )
                return None, str(e)  # Return error message
        else:
            logging.info(f"Reusing existing connection for MySQL database: {db_name}")
        return connection, None  # Return connection and no error

    @classmethod
    def execute(cls, sql: str, db_config=config) -> ExecutionResult:
        db_name = db_config["db_name"]
        connection, connect_error = cls.get_connection(db_config)

        if connection is None:
            return ExecutionResult(
                error_message=f"Failed to get database connection: {connect_error}"
            )

        database_tables = {}
        result_tables = {}
        error_message = None

        try:
            with connection.cursor() as cursor:
                # Start a transaction to ensure no permanent changes
                connection.begin()  # For explicitness

                try:
                    # Execute the SQL query
                    cursor.execute(sql)

                    # Fetch results
                    if (
                        cursor.description
                    ):  # Check if there are results to fetch (e.g., from a SELECT)
                        result = cursor.fetchall()
                        if result:
                            columns = [desc[0] for desc in cursor.description]
                            result_df = pd.DataFrame(result, columns=columns)
                            result_tables["result"] = result_df

                    # Get all table data after execution (before rollback)
                    cursor.execute("SHOW TABLES")
                    tables = [row[0] for row in cursor.fetchall()]

                    for table_name in tables:
                        try:
                            cursor.execute(f"SELECT * FROM `{table_name}`")
                            table_data = cursor.fetchall()
                            columns = [desc[0] for desc in cursor.description]
                            database_tables[table_name] = pd.DataFrame(
                                table_data, columns=columns
                            )
                        except MySQLError as e:
                            logging.warning(
                                f"Could not retrieve data for table {table_name}: {e}"
                            )
                finally:
                    # Always roll back to ensure no permanent changes
                    connection.rollback()

        except MySQLError as e:
            logging.error(f"Error during SQL execution.")
            error_message = str(e)
            # Ensure rollback if an error occurs outside the inner try block
            if connection.open:
                connection.rollback()

        return ExecutionResult(
            database_tables=database_tables,
            result_tables=result_tables,
            error_message=error_message,
        )

    @classmethod
    def close(cls, db_name: str = None):
        if db_name:
            if db_name in cls._connections:
                connection = cls._connections.pop(db_name)
                if connection.open:
                    connection.close()
                    logging.info(f"MySQL connection to '{db_name}' is closed.")
            else:
                logging.warning(f"No active connection found for database: {db_name}")
        else:  # Close all connections
            for db_name, connection in list(cls._connections.items()):
                if connection.open:
                    connection.close()
                    logging.info(f"MySQL connection to '{db_name}' is closed.")
                cls._connections.pop(db_name)
            logging.info("All MySQL connections closed.")


class PGSQLDatabaseSystem(DatabaseSystem):
    config = {
        "host": "127.0.0.1",
        "port": 15432,
        "user": "root",
        "password": "postgres_password",
        "db_name": "postgres",
    }

    _connections = {}

    @classmethod
    def get_connection(
        cls, db_config=config
    ) -> Tuple[Optional[PGSQLConnection], Optional[str]]:
        db_name = db_config["db_name"]
        connection = cls._connections.get(db_name)

        if connection is None or connection.closed:
            logging.info(f"Attempting to connect to PostgreSQL database: {db_name}")
            try:
                connection = psycopg2.connect(
                    database=db_config["db_name"],
                    user=db_config["user"],
                    password=db_config["password"],
                    host=db_config["host"],
                    port=int(db_config["port"]),
                )
                cls._connections[db_name] = connection
                logging.info(
                    f"Successfully connected to PostgreSQL database: {db_name}"
                )
            except PGSQLError as e:
                logging.error(
                    f"Error while connecting to PostgreSQL database '{db_name}': {e}"
                )
                return None, str(e)
        else:
            logging.info(
                f"Reusing existing connection for PostgreSQL database: {db_name}"
            )
        return connection, None

    @classmethod
    def execute(cls, sql: str, db_config=config) -> ExecutionResult:
        db_name = db_config["db_name"]
        connection, connect_error = cls.get_connection(db_config)

        if connection is None:
            return ExecutionResult(
                error_message=f"Failed to get database connection: {connect_error}"
            )

        database_tables = {}
        result_tables = {}
        error_message = None

        try:
            with connection.cursor() as cursor:
                # Start a transaction to ensure no permanent changes
                connection.autocommit = False  # For explicitness

                try:
                    # Execute the SQL query
                    cursor.execute(sql)

                    # Fetch results
                    if (
                        cursor.description
                    ):  # Check if there are results to fetch (e.g., from a SELECT)
                        result = cursor.fetchall()
                        if result:
                            columns = [desc.name for desc in cursor.description]
                            result_df = pd.DataFrame(result, columns=columns)
                            result_tables["result"] = result_df

                    # Get all table data after execution (before rollback)
                    # In PostgreSQL, query pg_catalog.pg_tables or information_schema.tables
                    cursor.execute(
                        "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
                    )
                    tables = [row[0] for row in cursor.fetchall()]

                    for table_name in tables:
                        try:
                            cursor.execute(f'SELECT * FROM "{table_name}"')
                            table_data = cursor.fetchall()
                            columns = [desc.name for desc in cursor.description]
                            database_tables[table_name] = pd.DataFrame(
                                table_data, columns=columns
                            )
                        except PGSQLError as e:
                            logging.warning(
                                f"Could not retrieve data for table {table_name}: {e}"
                            )
                finally:
                    # Always roll back to ensure no permanent changes
                    connection.rollback()

        except PGSQLError as e:
            logging.error(f"Error during SQL execution.")
            error_message = str(e)
            # Ensure rollback if an error occurs outside the inner try block
            if not connection.closed:
                connection.rollback()

        return ExecutionResult(
            database_tables=database_tables,
            result_tables=result_tables,
            error_message=error_message,
        )

    @classmethod
    def close(cls, db_name: str = None):
        if db_name:
            if db_name in cls._connections:
                connection = cls._connections.pop(db_name)
                if not connection.closed:
                    connection.close()
                    logging.info(f"PostgreSQL connection to '{db_name}' is closed.")
            else:
                logging.warning(f"No active connection found for database: {db_name}")
        else:  # Close all connections
            for db_name, connection in list(cls._connections.items()):
                if not connection.closed:
                    connection.close()
                    logging.info(f"PostgreSQL connection to '{db_name}' is closed.")
                cls._connections.pop(db_name)
            logging.info("All PostgreSQL connections closed.")


if __name__ == "__main__":
    pgsql_sql = "SELECT rs.raceId as race_id, (SELECT string_agg(constructorId::TEXT, ',' ORDER BY res.resultId) FROM results res WHERE res.raceId = rs.raceId) as constructor_ids, (SELECT string_agg(p.stop::TEXT, ', ' ORDER BY p.raceId) FROM pitstops p WHERE rs.raceId = p.raceId) AS stops FROM races rs"
    mysql_sql = textwrap.dedent(
        """SELECT
        rs.raceId AS race_id,
        (SELECT GROUP_CONCAT(res.constructorId ORDER BY res.resultId SEPARATOR ',') FROM results res WHERE res.raceId = rs.raceId) AS constructor_ids,
        (SELECT GROUP_CONCAT(p.stop ORDER BY p.raceId SEPARATOR ', ') FROM pitStops p WHERE rs.raceId = p.raceId) AS stops
    FROM
        races rs;"""
    )
    PGSQLDatabaseSystem.config["db_name"] = "formula_1"
    MySQLDatabaseSystem.config["db_name"] = "formula_1"

    try:
        result_pgsql = PGSQLDatabaseSystem.execute(pgsql_sql)
        result_mysql = MySQLDatabaseSystem.execute(mysql_sql)
        def title(s):
            s = str(s)
            width = len(s) + 10
            border_line = ("#" * (width + 4) + "\n") * 2
            blank_line = ("##" + " " * width + "##\n") * 2
            text_line = ("##" + " " * 5 + s + " " * 5 + "##\n")
            return border_line + blank_line + text_line + blank_line + border_line
        print(title("mysql result"))
        print(result_mysql)
        print(title("pgsql result"))
        print(result_pgsql)
        print(title("equivalence"))
        print("Result equivalence:", result_mysql.result_equals(result_pgsql))
        print("Modification equivalence:", result_mysql.database_equals(result_pgsql))
        print(result_mysql.compare(result_pgsql))
    finally:
        PGSQLDatabaseSystem.close()
        MySQLDatabaseSystem.close()
