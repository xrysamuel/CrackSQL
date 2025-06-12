import json
from dataclasses import dataclass
from typing import Optional
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class SQLTranslationPair:
    index: int
    src_dialect: str
    tgt_dialect: str
    src_sql: str
    tgt_sql: Optional[str] = None
    dataset_id: str = ""


def parse_sql_translation_pairs(json_file_path: str) -> list[SQLTranslationPair]:
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
            if key != "id" and value != "to be translated":
                src_dialect = key
                src_sql = value
                break  # Assuming only one source SQL per item

        # Determine target dialect and SQL
        for key, value in item.items():
            if value == "to be translated":
                tgt_dialect = key
                tgt_sql = None
                break

        # Determine dataset id
        dataset_id = item.get("id", None)

        # Check if item is valid
        if src_dialect and src_sql and tgt_dialect and dataset_id:
            sql_data_items.append(
                SQLTranslationPair(
                    index=i,
                    src_dialect=src_dialect,
                    tgt_dialect=tgt_dialect,
                    src_sql=src_sql,
                    tgt_sql=tgt_sql,
                    dataset_id=dataset_id,
                )
            )
        else:
            logger.warning(
                f"Invalid item at index {i}. Skipping."
            )

    return sql_data_items
