import sys
import logging
import shutil
import os
import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


from dataset import parse_sql_translation_pairs
from database import MySQLDatabase, PGSQLDatabase
exit()

sys.path.append("../backend")

from cracksql import translate, initkb

def initkb_func():
    initkb("./init_config.yaml")  # 首先在`.yaml`中填写基本配置
    logging.info("Knowledge base initialized successfully")


def trans_func():
    target_db_config = dict(**MYSQL_DATABASE_CONFIG, db_name="superhero")

    vector_config = {
        "src_kb_name": "postgresql_knowledge",
        "tgt_kb_name": "mysql_knowledge"
    }

    print("Starting SQL translation...")
    translated_sql, model_ans_list, used_pieces, lift_histories = translate(
        model_name="qwen-plus", 
        src_sql="WITH labeled_ends AS (SELECT lag(sa.ts) OVER (PARTITION BY sa.superhero_id, sa.activity_code ORDER BY sa.ts) = sa.ts - interval '5' minute IS NOT TRUE AS begins_period, sa.ts, lead(sa.ts) OVER (PARTITION BY sa.superhero_id, sa.activity_code ORDER BY sa.ts) = sa.ts + interval '5' minute IS NOT TRUE AS ends_period, sa.superhero_id, sa.activity_code FROM superhero_activities sa), periods AS (SELECT labeled_ends.ts, CASE WHEN labeled_ends.ends_period THEN labeled_ends.ts ELSE lead(labeled_ends.ts) OVER (PARTITION BY labeled_ends.superhero_id, labeled_ends.activity_code ORDER BY labeled_ends.ts) END AS period_end, labeled_ends.superhero_id, labeled_ends.activity_code, labeled_ends.begins_period FROM labeled_ends WHERE labeled_ends.begins_period OR labeled_ends.ends_period) SELECT tstzrange(periods.ts, periods.period_end, '[]') AS valid_interval, periods.superhero_id, periods.activity_code FROM periods WHERE periods.begins_period ORDER BY periods.superhero_id, periods.activity_code, periods.ts",
        src_dialect="postgresql",
        tgt_dialect="mysql",
        target_db_config=target_db_config,
        vector_config=vector_config,
        out_dir="./output", 
        retrieval_on=False, 
        top_k=3
    )

    print("Translation completed!")
    print(f"Translated SQL: {translated_sql}")
    print(f"Model answer list: {model_ans_list}")
    print(f"Used knowledge pieces: {used_pieces}")
    print(f"Lift histories: {lift_histories}")

def to_continue_if_instance_exists():
    instance_path = "instance"

    if os.path.exists(instance_path) and os.path.isdir(instance_path):
        logging.warning(f"The '{instance_path}' directory exists in the current location.")
        logging.warning("This might prevent your configuration or code changes from taking effect.")
        logging.warning("If you want your changes to apply, please manually delete or move the 'instance' directory.")

        user_input = input("Do you want to continue? [Y/n]: ").strip().lower()
        if user_input == 'y' or user_input == '':
            return True
        else:
            return False
    return True

def to_init_knowledge_base():
    logging.info("Initializing the knowledge base will convert documents related to database management systems located in '../data/processed_document' into a vector database. You can skip this step if you have performed it before.")

    user_input = input("Do you want to initialize the database knowledge base? [Y/n]: ").strip().lower()
    if user_input == 'y' or user_input == '':
        return True
    else:
        return False


if __name__ == "__main__":
    # STEP 1
    to_continue = to_continue_if_instance_exists()
    if not to_continue:
        logging.info("Terminated.")
        exit()

    # STEP 2
    pairs = parse_sql_translation_pairs("test.json")

    # STEP 3
    to_init = to_init_knowledge_base()
    if to_init:
        logging.info("Proceeding with knowledge base initialization...")
        initkb_func()
    else:
        logging.info("Skipping knowledge base initialization.")

    # STEP 4
    trans_func()