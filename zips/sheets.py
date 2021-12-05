import csv
import time
import configparser
from pathlib import Path

import pandas as pd
import gspread

config = configparser.ConfigParser()
config_path = str(Path(__file__).parents[1])
config.read(config_path + '/' + 'config.ini')

AUTH_TOKEN_FILE = config.get('conf', 'AUTH_TOKEN_FILE')
TOKEN_PATH  = config_path + '/' + AUTH_TOKEN_FILE

OUTPUT_NAME = config.get('conf', 'OUTPUT_FILE')
OUTPUT_FILE = config_path + '/' + OUTPUT_NAME

SHEET_NAME = config.get('conf', 'SHEET_NAME')

ADDRESS_COL = config.get('conf', 'SHEETS_ADDRESS_COLUMN')
ZIP_CODE_COL = config.get('conf', 'SHEETS_ZIP_CODE_COLUMN')

gc = gspread.service_account(filename=TOKEN_PATH)

# google sheets
wks = gc.open(SHEET_NAME).sheet1


def write_to_row(index, value, col=ZIP_CODE_COL):
    wks.update(f"{col}{index}", value)
    print(f'Added {value} to {col}{index}!')
    time.sleep(0.8)