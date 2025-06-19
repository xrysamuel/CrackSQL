import pandas as pd
from faker import Faker
import random
import pymysql
import psycopg2
from sqlalchemy import create_engine, text
import numpy as np
import os # Import the os module for creating directories

# --- Configuration ---
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 13306,
    "user": "root",
    "password": "mysql_root_password",
    "database": "high_school"
}

PGSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 15432,
    "user": "root",
    "password": "postgres_password",
    "database": "high_school"
}

OUTPUT_DIR = "my_dataset" # Directory to save CSV files

# --- Data Generation Functions ---

def generate_high_school_data(num_students=1000, num_courses=300, num_teachers=100, seed=42):
    """
    Generates synthetic high school data for students, courses, and teachers.
    Ensures reproducibility using a fixed seed.
    """
    Faker.seed(seed)
    random.seed(seed)
    np.random.seed(seed)
    fake = Faker('zh_CN') # Use Chinese locale for names

    print("Generating student data...")
    students_data = []
    for i in range(1, num_students + 1):
        student_id = f"S{i:04d}"
        student_name = fake.name()
        class_name = f"Class {random.randint(1, 20):02d}" # Assume 20 classes
        students_data.append([student_id, student_name, class_name])
    students_df = pd.DataFrame(students_data, columns=['student_id', 'student_name', 'class_name'])
    print(f"Generated {len(students_df)} students.")

    print("Generating teacher data...")
    teachers_data = []
    for i in range(1, num_teachers + 1):
        teacher_id = f"T{i:03d}"
        teacher_name = fake.name()
        teachers_data.append([teacher_id, teacher_name])
    teachers_df = pd.DataFrame(teachers_data, columns=['teacher_id', 'teacher_name'])
    print(f"Generated {len(teachers_df)} teachers.")

    print("Generating course data...")
    course_names = [
        "语文", "数学", "英语", "物理", "化学", "生物", "历史", "地理", "政治", "体育",
        "美术", "音乐", "信息技术", "通用技术", "心理健康", "生涯规划", "编程入门", "数据科学基础",
        "人工智能概论", "经济学原理", "哲学基础", "艺术鉴赏", "形体与健康", "社会实践", "创新思维"
    ]
    courses_data = []
    # Ensure each course has a valid teacher_id
    teacher_ids = teachers_df['teacher_id'].tolist()
    if not teacher_ids:
        raise ValueError("No teachers generated, cannot assign courses.")

    for i in range(1, num_courses + 1):
        course_id = f"C{i:03d}"
        course_name = random.choice(course_names) + str(random.randint(1,5)) # Add a number to make names more unique
        teacher_id = random.choice(teacher_ids)
        courses_data.append([course_id, course_name, teacher_id])
    courses_df = pd.DataFrame(courses_data, columns=['course_id', 'course_name', 'teacher_id'])
    print(f"Generated {len(courses_df)} courses.")

    return students_df, courses_df, teachers_df

# --- Database Interaction Functions ---

def create_database(db_type, config):
    """Creates the high_school database if it doesn't exist."""
    print(f"\nAttempting to connect to {db_type} to create database...")
    if db_type == "MySQL":
        conn = None
        try:
            # Connect without specifying a database first
            conn = pymysql.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"]
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
            conn.commit()
            print(f"Database '{config['database']}' ensured in MySQL.")
        except pymysql.Error as e:
            print(f"Error creating MySQL database: {e}")
            raise
        finally:
            if conn:
                conn.close()
    elif db_type == "PostgreSQL":
        conn = None
        try:
            # Connect to default database (postgres) to create new one
            conn = psycopg2.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                database="postgres" # Connect to default 'postgres' db
            )
            conn.autocommit = True # Allow CREATE DATABASE outside of transaction block
            cursor = conn.cursor()
            # Check if database exists before creating
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{config['database']}'")
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f"CREATE DATABASE {config['database']}")
                print(f"Database '{config['database']}' created in PostgreSQL.")
            else:
                print(f"Database '{config['database']}' already exists in PostgreSQL.")
        except psycopg2.Error as e:
            print(f"Error creating PostgreSQL database: {e}")
            raise
        finally:
            if conn:
                conn.close()

def import_data_to_db(df, table_name, db_type, config):
    """Imports a pandas DataFrame into a specified database table."""
    print(f"Importing data to {db_type} table: {table_name}...")
    try:
        if db_type == "MySQL":
            # SQLAlchemy engine for more robust DataFrame import
            engine_url = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            engine = create_engine(engine_url)
            with engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name}")) # Drop table if exists to ensure clean import
                conn.commit() # Commit DDL
                df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Data successfully imported to MySQL table '{table_name}'.")
        elif db_type == "PostgreSQL":
            engine_url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            engine = create_engine(engine_url)
            with engine.connect() as conn:
                conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE")) # CASCADE for PG to drop dependent objects
                conn.commit() # Commit DDL
                df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"Data successfully imported to PostgreSQL table '{table_name}'.")
    except Exception as e:
        print(f"Error importing data to {db_type} table '{table_name}': {e}")
        raise

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Generate Data
    students_df, courses_df, teachers_df = generate_high_school_data()

    # 2. Save Data to Local CSV Files
    print(f"\n--- Saving Data to local CSV files in '{OUTPUT_DIR}/' ---")
    os.makedirs(OUTPUT_DIR, exist_ok=True) # Create the output directory if it doesn't exist
    try:
        students_df.to_csv(os.path.join(OUTPUT_DIR, 'students.csv'), index=False, encoding='utf-8')
        print(f"Saved students.csv to '{OUTPUT_DIR}/'.")
        teachers_df.to_csv(os.path.join(OUTPUT_DIR, 'teachers.csv'), index=False, encoding='utf-8')
        print(f"Saved teachers.csv to '{OUTPUT_DIR}/'.")
        courses_df.to_csv(os.path.join(OUTPUT_DIR, 'courses.csv'), index=False, encoding='utf-8')
        print(f"Saved courses.csv to '{OUTPUT_DIR}/'.")
    except Exception as e:
        print(f"Error saving CSV files: {e}")


    # 3. Import to MySQL
    print("\n--- Importing Data to MySQL ---")
    try:
        create_database("MySQL", MYSQL_CONFIG)
        import_data_to_db(students_df, 'students', "MySQL", MYSQL_CONFIG)
        import_data_to_db(teachers_df, 'teachers', "MySQL", MYSQL_CONFIG)
        import_data_to_db(courses_df, 'courses', "MySQL", MYSQL_CONFIG)
        print("\nMySQL import process completed.")
    except Exception as e:
        print(f"MySQL import failed: {e}")

    # 4. Import to PostgreSQL
    print("\n--- Importing Data to PostgreSQL ---")
    try:
        create_database("PostgreSQL", PGSQL_CONFIG)
        import_data_to_db(students_df, 'students', "PostgreSQL", PGSQL_CONFIG)
        import_data_to_db(teachers_df, 'teachers', "PostgreSQL", PGSQL_CONFIG)
        import_data_to_db(courses_df, 'courses', "PostgreSQL", PGSQL_CONFIG)
        print("\nPostgreSQL import process completed.")
    except Exception as e:
        print(f"PostgreSQL import failed: {e}")

    print("\nDatabase generation, CSV export, and import script finished.")
    print("Please verify the data in your MySQL and PostgreSQL instances and the local CSV files.")