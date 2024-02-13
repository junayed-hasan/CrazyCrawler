# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from search_engine.models import CrawlingQueue

class CrawlingPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()
        #self.get_table()

    def create_connection(self):     # connecting to database
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'people'
        )
        self.curr = self.conn.cursor(buffered=True)

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS links_tb""")
        self.curr.execute("""create table links_tb(
            username longtext,
            clustername longtext,
            link longtext,
            content longtext
        )""")
        # self.curr.execute("""alter table links_tb add index(username, clustername, link, content)""")

    def get_user(self):    # fetch users from crawling_queue database table
        user = self.curr.execute("""SELECT userName FROM search_engine_crawlingqueue LIMIT 1;""")
        return user

    def get_cluster(self):  # fetch clusters from crawling_queue database table
        cluster = self.curr.execute("""SELECT clusterName FROM search_engine_crawlingqueue LIMIT 1;""")
        return cluster

    def get_url(self):      # fetch urls from crawling_queue database table
        urlsText = self.curr.execute("""SELECT url FROM search_engine_crawlingqueue LIMIT 1;""")
        return urlsText

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into links_tb values (%s, %s, %s, %s)""", (
            item['username'],
            item['clustername'],
            item['link'],
            item['content']
        ))
        self.conn.commit()
