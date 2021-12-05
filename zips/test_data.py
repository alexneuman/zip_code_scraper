
from pathlib import Path
from itertools import starmap
import os

import pandas as pd
import pytest
from zips.data.data_handling import (
    get_url,
    get_urls_and_index,
    get_rows,
)

BASE_URL = "https://www.google.com/search?client=firefox-b-1-d&q={search}"


@pytest.fixture
def source_df():
    source_file = str(Path(__file__).parents[0]) + "/" + "test_source.csv"
    return pd.read_csv(source_file, header=1)


@pytest.fixture
def output_df():
    output_file = str(Path(__file__).parents[0]) + "/" + "test_output.csv"
    return pd.read_csv(output_file)

def test_get_url(source_df):
    assert (
        get_url("123 Main St")
        == "https://www.google.com/search?client=firefox-b-1-d&q=123+Main+St"
    )

    urls = [get_url(address) for address in source_df.Address]
    assert len(urls) > 3000

    address = "425 E 20th St Long Beach CA"
    assert (
        get_url(address)
        == "https://www.google.com/search?client=firefox-b-1-d&q=425+E+20th+St+Long+Beach+CA"
    )


def test_get_urls_and_index(source_df):
    url = get_url(address="425 E 20th St Long Beach CA")
    url_2 = get_url(address="540 Olive Ave Long Beach CA")
    assert get_urls_and_index(source_df, rows=[3]) == [(3, url)]
    assert get_urls_and_index(source_df, rows=[3, 5]) == [(3, url), (5, url_2)]
    url_3 = get_urls_and_index(source_df, rows=[3294])


def test_get_missing_rows(source_df, output_df):
    rows = get_rows(source_df, output_df)
    assert rows[0] == 5
    assert rows[1] == 79
    rows = get_rows(source_df)
    assert rows[0] == 3
    assert rows[-1] == 3295

