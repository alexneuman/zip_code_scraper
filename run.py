import os
from time import sleep

from zips.zips.spiders.zip_spider import ZipSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from zips.zips.data.data_handling import delete_duplicate_headers


os.environ['SCRAPY_SETTINGS_MODULE'] = 'zips.zips.settings'
process = CrawlerProcess(get_project_settings())
for _ in range(3):
    process.crawl(ZipSpider)
    process.start()
    sleep(3)
    delete_duplicate_headers()