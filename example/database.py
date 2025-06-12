import subprocess
import logging
import os
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from sqlite3_to_mysql import SQLite3toMySQL
import psycopg2
from psycopg2 import sql as pgsql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # Required for CREATE DATABASE

MYSQL_DATABASE_CONFIG = {
    "host": "127.0.0.1",
    "port": 13306,
    "user": "root",
    "password": "mysql_root_password",
}

PG_DATABASE_CONFIG = {
    "host": "127.0.0.1",
    "port": 15432,
    "user": "postgres",
    "password": "postgres_password",
}

def create_pgsql_db(pgsql_db_name: str) -> bool:
    """
    Creates a PostgreSQL database using psycopg2. If the database already exists,
    it logs a warning and skips creation.

    Args:
        pgsql_db_name: The name of the PostgreSQL database to create.

    Returns:
        True if the database exists or was successfully created, False otherwise.
    """
    pg_host = PG_DATABASE_CONFIG["host"]
    pg_port = PG_DATABASE_CONFIG["port"]
    pg_user = PG_DATABASE_CONFIG["user"]
    pg_password = PG_DATABASE_CONFIG["password"]

    conn = None
    try:
        # Connect to the default 'postgres' database to create a new database
        # CREATE DATABASE cannot be run inside a transaction block,
        # so autocommit needs to be enabled.
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            user=pg_user,
            password=pg_password,
            dbname="postgres" # Connect to a default database like 'postgres' or 'template1'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(pgsql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [pgsql_db_name])
        if cursor.fetchone():
            logging.warning(f"Database '{pgsql_db_name}' already exists. Skipping creation.")
            cursor.close()
            conn.close()
            return True

        # If not, create the database
        logging.info(f"Attempting to create database '{pgsql_db_name}'...")
        cursor.execute(pgsql.SQL("CREATE DATABASE {}").format(pgsql.Identifier(pgsql_db_name)))
        logging.info(f"Database '{pgsql_db_name}' created successfully.")
        return True

    except psycopg2.Error as e:
        logging.error(f"Error creating database '{pgsql_db_name}': {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False
    finally:
        if conn:
            conn.close()

def migrate_from_sqlite3_to_pgsql(sqlite3_db_file: str, pgsql_db_name: str):
    """
    Migrates data from a SQLite3 database to a PostgreSQL database using pgloader.

    Args:
        sqlite3_db_file: The path to the SQLite3 database file.
        pgsql_db_name: The name of the target database in PostgreSQL.
    """
    pg_host = PG_DATABASE_CONFIG["host"]
    pg_port = PG_DATABASE_CONFIG["port"]
    pg_user = PG_DATABASE_CONFIG["user"]
    pg_password = PG_DATABASE_CONFIG["password"]

    # Construct the pgloader command
    pgloader_command = [
        "pgloader",
        f"sqlite://{sqlite3_db_file}",
        f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pgsql_db_name}"
    ]

    logging.info(f"Executing command: {' '.join(pgloader_command)}")

    try:
        # Execute the command
        result = subprocess.run(
            pgloader_command,
            check=True,  # Raise an exception for non-zero exit codes
            capture_output=True,
            text=True
        )
        logging.info("Migration successful!")
        logging.info("STDOUT:\n%s\n", result.stdout)
        if result.stderr:
            logging.warning("STDERR:\n%s\n", result.stderr)
    except subprocess.CalledProcessError as e:
        logging.error("Migration failed with error code %d", e.returncode)
        logging.error("STDOUT:\n%s\n", e.stdout)
        logging.error("STDERR:\n%s\n", e.stderr)
    except FileNotFoundError:
        logging.error("Error: pgloader command not found.")
        logging.error("Please ensure pgloader is installed and accessible in your system's PATH.")
    except Exception as e:
        logging.error("An unexpected error occurred: %s", e)


if __name__ == "__main__":
    create_pgsql_db("accounting")
    migrate_from_sqlite3_to_pgsql("downloads/BookSQL/accounting.sqlite", "accounting")