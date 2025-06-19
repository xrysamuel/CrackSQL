import sys
import logging
import os
import re
import datetime
from typing import Optional, List, Tuple, Dict

from dataset import (
    parse_sql_translation_pairs,
    save_sql_translation_pairs,
    SQLTranslationPair, 
    Dialect
)
from database import (
    MySQLDatabaseSystem,
    PGSQLDatabaseSystem,
    DatabaseSystem,
    ExecutionResult
)
from test_args import get_test_translate_args

sys.path.append("../backend")

from cracksql import translate, initkb

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


DIALECT_MAPPING: Dict[str, Tuple[DatabaseSystem, str, str]] = {
    Dialect.MYSQL: (MySQLDatabaseSystem, "mysql_knowledge", "mysql"),
    Dialect.POSTGRESQL: (PGSQLDatabaseSystem, "postgresql_knowledge", "postgresql")
    # Dialect.SQLITE: TODO
}

POSSIBLE_DB_NAMES = [
    "high_school",
    "debit_card_specializing",
    "financial",
    "formula_1",
    "california_schools",
    "card_games",
    "european_football_2",
    "thrombosis_prediction",
    "toxicology",
    "student_club",
    "superhero",
    "codebase_community",
] # TODO: Replace this temporary solution.


def initialize_knowledge_base():
    initkb("./init_config.yaml")
    logging.info("Knowledge base initialized successfully")

def cracksql_translate_pair(pair: SQLTranslationPair) -> SQLTranslationPair:
    if not pair.tgt_dialect in DIALECT_MAPPING:
        logging.error(f"Target dialect '{pair.tgt_dialect}' is not supported.")
        return pair
    if not pair.src_dialect in DIALECT_MAPPING:
        logging.error(f"Source dialect '{pair.src_dialect}' is not supported.")
        return pair
    tgt_db_system, tgt_kb_name, tgt_dialect = DIALECT_MAPPING[pair.tgt_dialect]
    src_db_system, src_kb_name, src_dialect = DIALECT_MAPPING[pair.src_dialect]

    vector_config = {
        "src_kb_name": src_kb_name,
        "tgt_kb_name": tgt_kb_name,
    }

    logging.info("Starting SQL translation...")
    db_name = None
    for possible_db_name in POSSIBLE_DB_NAMES: # TODO: Replace this temporary solution.
        src_db_system.config["db_name"] = possible_db_name
        result = src_db_system.execute(pair.src_sql, src_db_system.config)
        if result.error_message is not None:
            continue
        else:
            db_name = possible_db_name
            break

    if db_name is None:
        logging.error(f"Cannot find possible database name for '{pair.src_sql}'.")
        return pair
    
    tgt_db_system.config["db_name"] = db_name
    translated_sql, model_ans_list, used_pieces, lift_histories = translate(
        model_name="qwen-plus",
        src_sql=pair.src_sql,
        src_dialect=src_dialect,
        tgt_dialect=tgt_dialect,
        target_db_config=tgt_db_system.config,
        vector_config=vector_config,
        out_dir="./output",
        retrieval_on=False,
        top_k=3,
    )

    logging.info("Translation completed!")
    pair.tgt_sql = translated_sql
    pair.additional_info = {
        "model_answer_list": model_ans_list,
        "used_knowledge_pieces": used_pieces,
        "lift_histories": lift_histories,
    }
    return pair


def confirm_continue_if_instance_exists():
    instance_path = "instance"

    if os.path.exists(instance_path) and os.path.isdir(instance_path):
        logging.warning(
            f"The '{instance_path}' directory exists in the current location."
        )
        logging.warning(
            "This might prevent your configuration or code changes from taking effect."
        )
        logging.warning(
            "If you want your changes to apply, please manually delete or move the 'instance' directory."
        )

        user_input = input("Do you want to continue? [Y/n]: ").strip().lower()
        if user_input == "y" or user_input == "":
            return True
        else:
            return False
    return True


def comfirm_init_knowledge_base():
    logging.info(
        "Initializing the knowledge base will convert documents related to database management systems located in '../data/processed_document' into a vector database. You can skip this step if you have performed it before."
    )

    user_input = (
        input("Do you want to initialize the database knowledge base? [Y/n]: ")
        .strip()
        .lower()
    )
    if user_input == "y" or user_input == "":
        return True
    else:
        return False


if __name__ == "__main__":
    args = get_test_translate_args(method="cracksql")

    # STEP 1
    to_continue = confirm_continue_if_instance_exists()
    if not to_continue:
        logging.info("Terminated.")
        exit()

    # STEP 2
    pattern = re.compile(args.id_pattern)
    pairs = parse_sql_translation_pairs(
        args.input_file, filter_func=lambda p: re.match(pattern, p.dataset_id)
    )

    # STEP 3
    to_init = comfirm_init_knowledge_base()
    if to_init:
        logging.info("Proceeding with knowledge base initialization...")
        initialize_knowledge_base()
    else:
        logging.info("Skipping knowledge base initialization.")

    # STEP 4
    translated_pairs = []
    for pair in pairs:
        translated_pair = cracksql_translate_pair(pair)
        translated_pairs.append(translated_pair)
    save_sql_translation_pairs(args.output_file, translated_pairs)
