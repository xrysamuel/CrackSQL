import argparse
from typing import NamedTuple, Optional

class Args(NamedTuple):
    input_file: str
    output_file: str
    id_pattern: str

def get_test_translate_args(method: str) -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="input file", default="test.json", type=str)
    parser.add_argument("-o", "--output_file", help="output file", default=f"./output/test_translated_{method}.json", type=str)
    parser.add_argument("-p", "--id_pattern", help="valid pattern of id in input file", default=".*", type=str)
    args = parser.parse_args()
    return args

def get_test_accuracy_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_file", help="input file", default="./output/test_translated_craksql.json", type=str)
    parser.add_argument("-p", "--id_pattern", help="valid pattern of id in input file", default=".*", type=str)
    args = parser.parse_args()
    return args