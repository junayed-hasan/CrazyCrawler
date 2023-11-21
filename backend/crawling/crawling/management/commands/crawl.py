import sys
sys.path.append("C:/Users/Junayed/Desktop/_/Study/Fall 21/327 Project/backend")
sys.path.append("C:/Users/Junayed/Desktop/_/Study/Fall 21/327 Project/backend/crawling")
sys.path.append("C:/Users/Junayed/Desktop/_/Study/Fall 21/327 Project/backend/crawling/crawling")
sys.path.append("C:/Users/Junayed/Desktop/_/Study/Fall 21/327 Project/backend/crawling/crawling/spiders")

# moduleName = input('Enter module name:')
import fetchData
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from backend.search_engine.models import CrawlingQueue

configurelogging()
runner = CrawlerRunner()
runner.crawl(PDFClass)
# runner.crawl(MySpider2)
d = runner.join()
d.addBoth(lambda : reactor.stop())

reactor.run() # the script will block here until all crawling jobs are finished