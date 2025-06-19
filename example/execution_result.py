import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Tuple, Iterable, List
from functools import cached_property
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def _dataframe_to_strings(df: pd.DataFrame, name: str) -> List[str]:
    parts = []
    parts.append(f"Table: {name}")
    parts.append(df.head(5).to_string(index=False))  # Display first 5 rows, no index
    if len(df) > 5:
        parts.append(f"(... {len(df) - 5} more rows not shown)")
    parts.append("")  # Add an empty line for spacing
    return parts


def _set_diff_strings(
    a: Iterable, b: Iterable, a_name: str, b_name: str
) -> Tuple[List[str], set]:
    parts = []
    a_set = set(a)
    b_set = set(b)

    unique_to_a = a_set - b_set
    unique_to_b = b_set - a_set
    common = a_set.intersection(b_set)

    if unique_to_a:
        sorted_unique_to_a = sorted(list(unique_to_a))
        display_a = list(map(lambda ele: str(ele), sorted_unique_to_a[:10]))
        if len(sorted_unique_to_a) > 10:
            parts.append(
                f"Unique to {a_name}: {', '.join(display_a)}, ... ({len(sorted_unique_to_a)} in total)"
            )
        else:
            parts.append(f"Unique to {a_name}: {', '.join(display_a)}")
    if unique_to_b:
        sorted_unique_to_b = sorted(list(unique_to_b))
        display_b = list(map(lambda ele: str(ele), sorted_unique_to_b[:10]))
        if len(sorted_unique_to_b) > 10:
            parts.append(
                f"Unique to {b_name}: {', '.join(display_b)}, ... ({len(sorted_unique_to_b)} in total)"
            )
        else:
            parts.append(f"Unique to {b_name}: {', '.join(display_b)}")
    return parts, common


def _normalize_tables(tables: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    normalized_tables = {}
    for name, table in tables.items():
        table.columns = [col.lower() for col in table.columns]
        normalized_table = table.sort_values(by=table.columns[0]).reset_index(
            drop=True
        )
        normalized_tables[name.lower()] = normalized_table
    return dict(sorted(normalized_tables.items()))


def _compare_dataframes(
    a: pd.DataFrame,
    b: pd.DataFrame,
    a_name: pd.DataFrame,
    b_name: pd.DataFrame,
    table_name: str,
) -> list[str]:
    """Helper function to compare two DataFrames and return a list of differences."""
    parts = []

    # Check for index equality
    if not a.index.equals(b.index):
        parts.append(f"Table '{table_name}': Indexes are different.")
        index_diff_strings, _ = _set_diff_strings(
            a.index.tolist(), b.index.tolist(), f"{a_name} index", f"{b_name} index"
        )
        parts.extend(index_diff_strings)

    # Check for column equality
    if not a.columns.equals(b.columns):
        parts.append(f"Table '{table_name}': Columns are different.")
        columns_diff_strings, _ = _set_diff_strings(
            a.columns.tolist(),
            b.columns.tolist(),
            f"{a_name} columns",
            f"{b_name} columns",
        )
        parts.extend(columns_diff_strings)

    # Only compare if both index and columns are identical
    if a.index.equals(b.index) and a.columns.equals(b.columns):
        if not a.equals(b):
            count = 0
            parts.append(f"Differences in table '{table_name}':")
            for row in a.index:
                for col in a.columns:
                    if count >= 10:
                        parts.append("...")
                        return parts
                    val1 = a.loc[row, col]
                    val2 = b.loc[row, col]
                    if pd.isna(val1) or pd.isna(val2) or val1 == val2:
                        continue
                    parts.append(f"@ (row: {row}, col: {col}): {a_name}: {val1}, {b_name}: {val2}")
                    count += 1

    if len(parts) == 0:
        parts.append(f"{table_name}: No differences between {a_name} and {b_name}")
    return parts


@dataclass
class ExecutionResult:
    database_tables: Dict[str, pd.DataFrame] = field(default_factory=dict)
    result_tables: Dict[str, pd.DataFrame] = field(default_factory=dict)
    error_message: Optional[str] = None

    @cached_property
    def normalized_database_tables(self) -> Dict[str, pd.DataFrame]:
        return _normalize_tables(self.database_tables)

    @cached_property
    def normalized_result_tables(self) -> Dict[str, pd.DataFrame]:
        return _normalize_tables(self.result_tables)

    def __eq__(self, other):
        if not isinstance(other, ExecutionResult):
            return NotImplemented
        if self.result_equals(other) and self.database_equals(other):
            return True
        return False

    def result_equals(self, other):
        if not isinstance(other, ExecutionResult):
            return NotImplemented
        if self.error_message is not None or other.error_message is not None:
            return False
        if (
            self.normalized_result_tables.keys()
            != other.normalized_result_tables.keys()
        ):
            return False
        for key in self.normalized_result_tables:
            if not self.normalized_result_tables[key].equals(
                other.normalized_result_tables[key]
            ):
                return False
        return True

    def database_equals(self, other):
        if not isinstance(other, ExecutionResult):
            return NotImplemented
        if self.error_message is not None or other.error_message is not None:
            return False
        if (
            self.normalized_database_tables.keys()
            != other.normalized_database_tables.keys()
        ):
            return False
        for key in self.normalized_database_tables:
            if not self.normalized_database_tables[key].equals(
                other.normalized_database_tables[key]
            ):
                return False
        return True

    def compare(self, other) -> str:
        if not isinstance(other, ExecutionResult):
            return "Cannot compare: 'other' is not an instance of ExecutionResult."

        parts = []

        # Compare database tables
        parts.append("--- Database Table Comparison ---")

        db_diff, common_db_keys = _set_diff_strings(
            self.normalized_database_tables.keys(),
            other.normalized_database_tables.keys(),
            "self",
            "other",
        )
        parts.extend(db_diff)

        for key in sorted(common_db_keys):
            df_self = self.normalized_database_tables[key]
            df_other = other.normalized_database_tables[key]
            parts.extend(_compare_dataframes(df_self, df_other, "self", "other", key))
        parts.append("")

        parts.append("--- Result Table Comparison ---")

        res_diff, common_res_keys = _set_diff_strings(
            self.normalized_result_tables.keys(),
            other.normalized_result_tables.keys(),
            "self",
            "other",
        )
        parts.extend(res_diff)

        for key in sorted(common_res_keys):
            df_self = self.normalized_result_tables[key]
            df_other = other.normalized_result_tables[key]
            parts.extend(_compare_dataframes(df_self, df_other, "self", "other", key))
        parts.append("")

        return "\n".join(parts)

    def __str__(self) -> str:
        parts = []

        if self.database_tables:
            parts.append("--- Database Tables ---")
            for name, df in self.normalized_database_tables.items():
                parts.extend(_dataframe_to_strings(df, name))

        if self.result_tables:
            parts.append("--- Result Tables ---")
            for name, df in self.normalized_result_tables.items():
                parts.extend(_dataframe_to_strings(df, name))

        if self.error_message:
            parts.append("--- Error Message ---")
            parts.append(self.error_message)

        if not parts:
            return "ExecutionResult: No data or error message."

        return "\n".join(parts)
