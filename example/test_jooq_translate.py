import requests
import re
import logging
from typing import Dict

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

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DIALECT_MAPPING: Dict[str, str] = {
    Dialect.MYSQL: "MYSQL",
    Dialect.POSTGRESQL: "POSTGRES",
    Dialect.SQLITE: "SQLITE"
}

def jooq_translate_pair(pair: SQLTranslationPair) -> SQLTranslationPair:
    if not pair.tgt_dialect in DIALECT_MAPPING:
        logging.error(f"Target dialect '{pair.tgt_dialect}' is not supported.")
        return pair
    if not pair.src_dialect in DIALECT_MAPPING:
        logging.error(f"Source dialect '{pair.src_dialect}' is not supported.")
        return pair
    tgt_dialect = DIALECT_MAPPING[pair.tgt_dialect]
    src_dialect = DIALECT_MAPPING[pair.src_dialect]

    url = "https://www.jooq.org/translate/translate"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.jooq.org",
        "Referer": "https://www.jooq.org/translate/",
        "Sec-Ch-Ua": '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
    }

    data = {
        "from-dialect": src_dialect,
        "from-search-path": "PUBLIC",
        "from-unknown-functions": "true",
        "from-date-format": "YYYY-MM-DD",
        "from-timestamp-format": "YYYY-MM-DD HH24:MI:SS.FF",
        "from-retain-comments-between-queries": "false",
        "from-ignore-comments": "true",
        "from-ignore-comment-start": "[jooq ignore start]",
        "from-ignore-comment-stop": "[jooq ignore stop]",
        "to-dialect": tgt_dialect,
        "to-keywords": "LOWER",
        "to-name-case": "AS_IS",
        "to-name-quoted": "EXPLICIT_DEFAULT_QUOTED",
        "to-param-type": "NAMED",
        "to-patterns": "OFF",
        "to-join-style": "DEFAULT",
        "to-qualify": "WHEN_NEEDED",
        "to-rownum": "WHEN_NEEDED",
        "to-inline-cte": "WHEN_NEEDED",
        "to-group-by-column-index": "WHEN_NEEDED",
        "to-unnecessary-arithmetic": "INTERNAL",
        "to-field-as": "DEFAULT",
        "to-table-as": "DEFAULT",
        "to-inner-keyword": "DEFAULT",
        "to-outer-keyword": "DEFAULT",
        "schema": "",
        "sql": pair.src_sql
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        pair.tgt_sql = response.text
        return pair

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        logging.error(f"Response: {response.text}")
        return pair
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return pair

# 示例用法
if __name__ == "__main__":
    args = get_test_translate_args(method="jooq")

    pattern = re.compile(args.id_pattern)
    pairs = parse_sql_translation_pairs(
        args.input_file, filter_func=lambda p: re.match(pattern, p.dataset_id)
    )

    translated_pairs = []
    for i, pair in enumerate(pairs):
        translated_pair = jooq_translate_pair(pair)
        translated_pairs.append(translated_pair)
        logging.info(f"{i + 1} completed.")
    save_sql_translation_pairs(args.output_file, translated_pairs)