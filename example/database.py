import subprocess
import logging
import os
import sqlite3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


MYSQL_DATABASE_CONFIG = {
    "host": "127.0.0.1",
    "port": 13306,
    "user": "root",
    "password": "mysql_root_password",
}

PG_DATABASE_CONFIG = {
    "host": "127.0.0.1",
    "port": 15432,
    "user": "root",
    "password": "postgres_password",
}