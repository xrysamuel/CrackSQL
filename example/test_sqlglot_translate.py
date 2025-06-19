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
    Dialect.POSTGRESQL: (PGSQLDatabaseSystem, "postgresql_knowledge", "postgresql"),
    Dialect.SQLITE: (None, "sqlite_knowledge", "sqlite")
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

def sqlglot_translate_pair(pair: SQLTranslationPair) -> SQLTranslationPair:
    if not pair.tgt_dialect in DIALECT_MAPPING:
        logging.error(f"Target dialect '{pair.tgt_dialect}' is not supported.")
        return pair
    if not pair.src_dialect in DIALECT_MAPPING:
        logging.error(f"Source dialect '{pair.src_dialect}' is not supported.")
        return pair
    tgt_db_system, tgt_kb_name, tgt_dialect = DIALECT_MAPPING[pair.tgt_dialect]
    src_db_system, src_kb_name, src_dialect = DIALECT_MAPPING[pair.src_dialect]

    logging.info("Starting SQL translation...")
    translated_sql, model_ans_list, used_pieces, lift_histories = translate(
        model_name=None,
        src_sql=pair.src_sql,
        src_dialect=src_dialect,
        tgt_dialect=tgt_dialect,
        target_db_config=None,
        vector_config=None,
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

if __name__ == "__main__":
    args = get_test_translate_args(method="sqlglot")

    pattern = re.compile(args.id_pattern)
    pairs = parse_sql_translation_pairs(
        args.input_file, filter_func=lambda p: re.match(pattern, p.dataset_id)
    )

    translated_pairs = []
    for pair in pairs:
        translated_pair = sqlglot_translate_pair(pair)
        translated_pairs.append(translated_pair)
    save_sql_translation_pairs(args.output_file, translated_pairs)
