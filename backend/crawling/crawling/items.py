# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..."))
sys.path.append("D:/COMP SCI/repos/cse327.1.2/backend/search_engine")

sys.path.append("C:/Users/USER PC/AppData/Local/Programs/Python/Python39/Lib/site-packages/PyPDF2")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')



import scrapy
#from backend.search_engine.models import CrawlingQueue
from scrapy_djangoitem import DjangoItem


# class CrawlerQueue(DjangoItem):
#     django_model = CrawlingQueue


class CrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    username = scrapy.Field()
    clustername = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
