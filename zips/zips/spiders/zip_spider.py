import time
from pathlib import Path
import configparser

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zips.zips.data.data_handling import indexed_urls


config = configparser.ConfigParser()
config.read(str(Path(__file__).parents[3]) + '/' + 'config.ini')
try:
    TOKEN = config.get('conf', 'AUTH_TOKEN_FILE')
except:
    TOKEN = None

class ZipSpider(scrapy.Spider):
    name = "zip_spider"
    allowed_domains = ["google.com"]

    def start_requests(self):
        for index, url in indexed_urls:
            yield scrapy.Request(
                url=url, callback=self.parse, cb_kwargs={"index": index}
            )

    def parse(self, response, index):
        time.sleep(1.9)
        try:
            zip_code = int(
                response.xpath(
                    './/span[contains(text(), ", CA ")]/text()').get()[-5:]
            )
        except TypeError:
            zip_code = int(response.xpath('.//div[contains(text(), "Postal code in ")]/../../span/h3/div/text()').get()[-5:])
        try:
            name = response.xpath(
                './/h4[contains(text(), "At this address")]/text()/../..//h5/text()'
            ).get()
        except:
            name = None

        yield {"index": index, "name": name, "zip_code": zip_code}
