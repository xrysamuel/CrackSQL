import json
import os
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Callable
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class Dialect(Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"

NAME_TO_DIALECT = {
    "postgresql": Dialect.POSTGRESQL,
    "mysql": Dialect.MYSQL,
    "sqlite": Dialect.SQLITE
}

@dataclass
class SQLTranslationPair:
    index: int
    src_dialect: Dialect
    tgt_dialect: Dialect
    src_sql: str
    tgt_sql: Optional[str] = None
    dataset_id: str = ""
    additional_info: dict = field(default_factory=dict)

def save_sql_translation_pairs(
    json_file_path: str, pairs: list[SQLTranslationPair]
):
    """
    Saves a list of SQLTranslationPair objects to a JSON file.

    The pairs are sorted by their index before saving.
    Each pair is transformed into a dictionary with src_dialect, tgt_dialect,
    id, and additional_info fields.

    Args:
        json_file_path: The path to the JSON file where the data will be saved.
        pairs: A list of SQLTranslationPair objects to save.
    """
    # Sort pairs by index
    sorted_pairs = sorted(pairs, key=lambda p: p.index)

    # Transform each pair into the desired dictionary format
    data_to_save = []
    for pair in sorted_pairs:
        item = {
            pair.src_dialect.value: pair.src_sql,
            pair.tgt_dialect.value: pair.tgt_sql,
            "id": pair.dataset_id
        }
        if pair.additional_info:
            item["additional_info"] = pair.additional_info
        data_to_save.append(item)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    # Save the data to the JSON file, overwriting if it exists
    try:
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        logger.info(f"Successfully saved {len(pairs)} SQL translation pairs to {json_file_path}")
    except IOError as e:
        logger.error(f"Error saving SQL translation pairs to {json_file_path}: {e}")



def parse_sql_translation_pairs(
    json_file_path: str, filter_func: Callable[[SQLTranslationPair], bool]
) -> list[SQLTranslationPair]:
    """
    Parses a JSON file containing SQL data into a list of SQLTranslationPair objects.

    Args:
        json_file_path: The path to the JSON file.

    Returns:
        A list of SQLTranslationPair objects.
    """
    sql_data_items = []
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data):
        # Determine source dialect, SQL, target dialect, and target SQL
        src_dialect = None
        src_sql = None
        tgt_dialect = None
        tgt_sql = None

        # Iterate through the keys to find the source dialect and SQL
        for key, value in item.items():
            if key in NAME_TO_DIALECT:
                src_dialect = key
                src_sql = value
                break  # Assuming only one source SQL per item

        # Determine target dialect and SQL
        for key, value in item.items():
            if key in NAME_TO_DIALECT and key != src_dialect:
                tgt_dialect = key
                tgt_sql = value
                break

        # Determine dataset id
        dataset_id = item.get("id", None)

        # Check if item is valid
        if src_dialect and src_sql and tgt_dialect and tgt_sql and dataset_id:
            pair = SQLTranslationPair(
                index=i,
                src_dialect=NAME_TO_DIALECT[src_dialect],
                tgt_dialect=NAME_TO_DIALECT[tgt_dialect],
                src_sql=src_sql,
                tgt_sql=tgt_sql,
                dataset_id=dataset_id,
            )
            if filter_func(pair):
                sql_data_items.append(pair)
            else:
                logger.warning(f"Skipping item at index {i}.")
        else:
            logger.warning(f"Invalid item at index {i}. Skipping.")

    return sql_data_items
