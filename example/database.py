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

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@dataclass
class ExecutionResult:
    database_tables: Dict[str, pd.DataFrame] = field(default_factory=dict)
    result_tables: Dict[str, pd.DataFrame] = field(default_factory=dict)
    error_message: Optional[str] = None

    def _normalize_tables(self, tables: Dict[str, pd.DataFrame]):
        normalized_tables = {}
        for name, table in tables.items():
            normalized_table = table.sort_values(by=list(table.columns)).reset_index(drop=True)
            normalized_tables[name.lower()] = normalized_table
        return dict(sorted(normalized_tables.items()))

    @property
    def normalized_database_tables(self):
        return self._normalize_tables(self.database_tables)
    
    @property
    def normalized_result_tables(self):
        return self._normalize_tables(self.result_tables)


    def __eq__(self, other):
        if not isinstance(other, ExecutionResult):
            return NotImplemented

        if self.error_message is not None or other.error_message is not None:
            return False

        if self.database_tables.keys() != other.database_tables.keys():
            return False
        for key in self.database_tables:
            if not self.database_tables[key].equals(other.database_tables[key]):
                return False

        if self.result_tables.keys() != other.result_tables.keys():
            return False
        for key in self.result_tables:
            if not self.result_tables[key].equals(other.result_tables[key]):
                return False

        return True

    def __str__(self) -> str:
        parts = []

        if self.database_tables:
            parts.append("--- Database Tables ---")
            for name, df in self.normalized_database_tables.items():
                parts.append(f"Table: {name}")
                parts.append(df.head(5).to_string(index=False)) # Display first 5 rows, no index
                if len(df) > 5:
                    parts.append(f"(... {len(df) - 5} more rows not shown)")
                parts.append("") # Add an empty line for spacing

        if self.result_tables:
            parts.append("--- Result Tables ---")
            for name, df in self.normalized_result_tables.items():
                parts.append(f"Table: {name}")
                parts.append(df.head(5).to_string(index=False)) # Display first 5 rows, no index
                if len(df) > 5:
                    parts.append(f"(... {len(df) - 5} more rows not shown)")
                parts.append("") # Add an empty line for spacing

        if self.error_message:
            parts.append("--- Error Message ---")
            parts.append(self.error_message)

        if not parts:
            return "ExecutionResult: No data or error message."

        return "\n".join(parts)

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

        if connection is None or not connection.is_connected():
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
            return ExecutionResult(error_message=f"Failed to get database connection: {connect_error}")

        database_tables = {}
        result_tables = {}
        error_message = None

        try:
            with connection.cursor() as cursor:
                # Start a transaction to ensure no permanent changes
                connection.begin() # For explicitness

                try:
                    # Execute the SQL query
                    cursor.execute(sql)

                    # Fetch results
                    if cursor.description: # Check if there are results to fetch (e.g., from a SELECT)
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
                            database_tables[table_name] = pd.DataFrame(table_data, columns=columns)
                        except MySQLError as e:
                            logging.warning(f"Could not retrieve data for table {table_name}: {e}")
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
                logging.info(f"Successfully connected to PostgreSQL database: {db_name}")
            except PGSQLError as e:
                logging.error(
                    f"Error while connecting to PostgreSQL database '{db_name}': {e}"
                )
                return None, str(e)
        else:
            logging.info(f"Reusing existing connection for PostgreSQL database: {db_name}")
        return connection, None

    @classmethod
    def execute(cls, sql: str, db_config=config) -> ExecutionResult:
        db_name = db_config["db_name"]
        connection, connect_error = cls.get_connection(db_config)

        if connection is None:
            return ExecutionResult(error_message=f"Failed to get database connection: {connect_error}")

        database_tables = {}
        result_tables = {}
        error_message = None

        try:
            with connection.cursor() as cursor:
                # Start a transaction to ensure no permanent changes
                connection.autocommit = False # For explicitness

                try:
                    # Execute the SQL query
                    cursor.execute(sql)

                    # Fetch results
                    if cursor.description: # Check if there are results to fetch (e.g., from a SELECT)
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
                            database_tables[table_name] = pd.DataFrame(table_data, columns=columns)
                        except PGSQLError as e:
                            logging.warning(f"Could not retrieve data for table {table_name}: {e}")
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
        else:   # Close all connections
            for db_name, connection in list(cls._connections.items()):
                if not connection.closed:
                    connection.close()
                    logging.info(f"PostgreSQL connection to '{db_name}' is closed.")
                cls._connections.pop(db_name)
            logging.info("All PostgreSQL connections closed.")

if __name__ == "__main__":
    pgsql_sql = "SELECT rs.raceId as race_id, (SELECT string_agg(constructorId::TEXT, ',' ORDER BY res.resultId) FROM results res WHERE res.raceId = rs.raceId) as constructor_ids, (SELECT string_agg(p.stop::TEXT, ', ' ORDER BY p.raceId) FROM pitstops p WHERE rs.raceId = p.raceId) AS stops FROM races rs"
    mysql_sql = textwrap.dedent("""SELECT
        rs.raceId AS race_id,
        (SELECT GROUP_CONCAT(res.constructorId ORDER BY res.resultId SEPARATOR ',') FROM results res WHERE res.raceId = rs.raceId) AS constructor_ids,
        (SELECT GROUP_CONCAT(p.stop ORDER BY p.raceId SEPARATOR ', ') FROM pitStops p WHERE rs.raceId = p.raceId) AS stops
    FROM
        races rs;""")
    PGSQLDatabaseSystem.config["db_name"] = "formula_1"
    MySQLDatabaseSystem.config["db_name"] = "formula_1"

    try:
        result_pgsql = PGSQLDatabaseSystem.execute(pgsql_sql)
        result_mysql = MySQLDatabaseSystem.execute(mysql_sql)
        print("==== MySQL Result ==== ")
        print(result_mysql)
        print("==== PGSQL Result ==== ")
        print(result_pgsql)
        print("==== Equivalence ==== ")
        print(result_mysql == result_pgsql)
        diff = difflib.unified_diff(str(result_mysql).lower().splitlines(), str(result_pgsql).lower().splitlines())
        print("\n".join(diff))
    finally:
        PGSQLDatabaseSystem.close()
        MySQLDatabaseSystem.close()