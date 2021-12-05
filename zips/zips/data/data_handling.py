import os
from pathlib import Path
from typing import Iterable, List, Tuple
import configparser

import pandas as pd
from pandas.core.frame import DataFrame

#config
config = configparser.ConfigParser()
config.read(str(Path(__file__).parents[3]) + '/' + 'config.ini')
OUT_FILE = config.get('conf', 'OUTPUT_FILE')
SOURCE_FILE = config.get('conf', 'SOURCE_FILE')
ADDRESS_COLUMN = config.get('conf', 'ADDRESS_COLUMN')
ZIP_COLUMN = config.get('conf', 'ZIP_CODE_COLUMN')


BASE_URL = "https://www.google.com/search?client=firefox-b-1-d&q={search}"

source_file = str(Path(__file__).parents[3]) + "/" + SOURCE_FILE
output_file = str(Path(__file__).parents[3]) + "/" + OUT_FILE


source_df = pd.read_csv(source_file, header=1)
if ADDRESS_COLUMN not in source_df.columns or ZIP_COLUMN not in source_df.columns:
    source_df = pd.read_csv(source_file)

if os.path.exists(output_file):
    output_df = pd.read_csv(output_file)
else:
    output_df = None


def get_url(address: str) -> str:
    formatted_address = address.replace(" ", "+")
    return BASE_URL.format(search=formatted_address)


def get_urls_and_index(df: DataFrame, rows: Iterable) -> List[Tuple[int, str]]:

    urls = []
    for row in rows:
        try:
            url = get_url(df.iloc[row - 3][ADDRESS_COLUMN])
            urls.append((row, url))
        except:
            pass
    return urls


def get_rows(source_df, output_df=None) -> List[int]:
    rows = set(range(3, len(source_df) + 4))
    if output_df is None:
        return list(rows)

    for _, row in output_df.iterrows():
        try:
            rows.remove(int(row["index"]))
        except:
            pass
    return list(rows)

def delete_duplicate_headers():
    """Deletes column names as index when spider run multiple times"""
    df = pd.read_csv(output_file)
    df.drop(df[(df.name == 'name') | (df['zip_code'] == 'zip_code')].index, inplace=True)
    df.to_csv(output_file, index=False)


missing_rows = get_rows(source_df, output_df)
indexed_urls = get_urls_and_index(df=source_df, rows=missing_rows)
