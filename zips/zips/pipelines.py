import csv

import configparser
from os import write
from pathlib import Path

from itemadapter import ItemAdapter


class ZipsPipeline:
    def __init__(self):
        config = configparser.ConfigParser()
        config_path = str(Path(__file__).parents[2])
        config.read(config_path + '/' + 'config.ini')
        
        try:
            AUTH_TOKEN_FILE = config.get('conf', 'AUTH_TOKEN_FILE')
            self.token = True
            from sheets import write_to_row
            self.write_to_row = write_to_row
        except:
            self.token = False

        output_file = config.get('conf', 'OUTPUT_FILE')
        self.file = open(config_path + '/' + output_file, 'a', newline='')
        fieldnames = ['index', 'name', 'zip_code']
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()

        
    def process_item(self, item, spider):
        if self.token:
            index = item['index']
            zip_code = item['zip_code']
            try:
                self.write_to_row(index=int(index), value=int(zip_code))
            except:
                pass
        self.writer.writerow({'index': item['index'], 'name': item['name'], 'zip_code': item['zip_code']})
        return item
