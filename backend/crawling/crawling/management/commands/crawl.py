import sys
import os
import scrapy
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..."))

#os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

#from django.conf import settings

# import django


# search_engine module
sys.path.append("D:/COMP SCI/repos/cse327.1.2/backend")

# scrapy config
sys.path.append("D:/COMP SCI/repos/cse327.1.2/backend/crawling")

# scrapy's setting
sys.path.append("D:/COMP SCI/repos/cse327.1.2/backend/crawling/crawling")

# fetchData
sys.path.append("D:/COMP SCI/repos/cse327.1.2/backend/crawling/crawling/spiders")




import django

# django.setup()

# import urllib.request
# sys.path.append("D:/COMP SCI/repos/cse327.1.2/backend/crawling/crawling")

# moduleName = input('Enter module name:')
# from spiders import fetchData
from fetchData import PDFClass
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from backend.search_engine.models import CrawlingQueue


configure_logging()
runner = CrawlerRunner()
runner.crawl(PDFClass)
# runner.crawl(MySpider2)
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run() # the script will block here until all crawling jobs are finished

# class Command(BaseCommand):
#     help = "Release the spiders"
#
#     def handle(self, *args, **options):
#         process = CrawlerProcess(get_project_settings())
#
#         process.crawl(Spider)
#         process.start()
#
#     objects_in_queue = CrawlingQueue.objects.all()
#     for obj in objects_in_queue:
#         handle()
