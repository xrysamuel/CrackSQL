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
from test_args import get_test_accuracy_args

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DIALECT_MAPPING: Dict[str, Tuple[DatabaseSystem, str, str]] = {
    Dialect.MYSQL: (MySQLDatabaseSystem, "mysql", "mysql_knowledge"),
    Dialect.POSTGRESQL: (PGSQLDatabaseSystem, "postgresql", "postgresql_knowledge")
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

def get_accuracy_result(pair: SQLTranslationPair) -> Tuple[ExecutionResult, ExecutionResult]:
    if not pair.tgt_dialect in DIALECT_MAPPING:
        logging.error(f"Target dialect '{pair.tgt_dialect}' is not supported.")
        return (ExecutionResult(), ExecutionResult())
    if not pair.src_dialect in DIALECT_MAPPING:
        logging.error(f"Source dialect '{pair.src_dialect}' is not supported.")
        return (ExecutionResult(), ExecutionResult())
    tgt_db_system, tgt_kb_name, tgt_dialect = DIALECT_MAPPING[pair.tgt_dialect]
    src_db_system, src_kb_name, src_dialect = DIALECT_MAPPING[pair.src_dialect]

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
        return (ExecutionResult(), ExecutionResult())
    
    src_db_system.config["db_name"] = db_name
    tgt_db_system.config["db_name"] = db_name
    logging.info(f"Source SQL: {pair.src_sql}")
    logging.info(f"Target SQL: {pair.tgt_sql}")
    src_result = src_db_system.execute(pair.src_sql, src_db_system.config)
    tgt_result = tgt_db_system.execute(pair.tgt_sql, tgt_db_system.config)
    return src_result, tgt_result

if __name__ == "__main__":
    args = get_test_accuracy_args()

    pattern = re.compile(args.id_pattern)
    pairs = parse_sql_translation_pairs(
        args.input_file, filter_func=lambda p: re.match(pattern, p.dataset_id) and p.tgt_sql != "Cannot translate!"
    )

    translated_pairs = []
    print(f"# Comparison Result of '{args.input_file}'")
    for pair in pairs:
        print(f"\n## Comparison result of sample {pair.index}")
        src_result, tgt_result = get_accuracy_result(pair)

        print("\n### Execution result of source SQL statement")
        print(f"\n```{pair.src_dialect.value}\n{pair.src_sql}\n```\n")
        print(src_result)

        print("\n### Execution result of Target SQL statement")
        print(f"\n```{pair.tgt_dialect.value}\n{pair.tgt_sql}\n```\n")
        print(tgt_result)

        print("\n### Equivalence of the two execution results")
        database_equivalence = src_result.database_equals(tgt_result)
        result_equivalence = src_result.result_equals(tgt_result)
        no_error = tgt_result.error_message is None
        print("- Consistency of data in the database after execution (@1):", database_equivalence)
        print("- Consistency of query results (@2):", result_equivalence)
        print("- Execution without errors (@3):", no_error)
        print("- All correct (@4):", database_equivalence and result_equivalence and no_error)
        print()
        print(src_result.compare(tgt_result))
        

