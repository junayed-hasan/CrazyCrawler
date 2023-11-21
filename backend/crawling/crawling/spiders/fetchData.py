import io
import ssl
import urllib.request
from abc import ABC

import requests
import PyPDF2
import zope.interface
from scrapy.linkextractors import LinkExtractor
from docx2python import docx2python
import lxml.etree
import lxml.html
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess

# allowed extensions
from search_engine.models import CrawledQueue, CrawlingQueue
from ..pipelines import CrawlingPipeline
from ..items import CrawlingItem


# from ..settings import DepthLimit

class SpiderInterface(zope.interface.Interface):
    name = zope.interface.Attribute("")

    def parse(self, x):
        pass

    def method2(self):
        pass


# The zope.interface package provides an implementation of “object interfaces” for Python
# Implements spider for scraping pdf files
@zope.interface.implementer(SpiderInterface)
class PDFClass(CrawlSpider):
    name = "pdf_crawler"

    def parse(self, response):
        self.logger.info('Yippee! We have found: %s', response.url)
        # shows a message with response
        if hasattr(response, "text"):
            pass  # we disregard any HTML text
        else:
            # filtering out extensions that are in our ALLOWED_EXTENSIONS list from the list of returned urls
            extension = list(filter(lambda x: response.url.lower().endswith(x), ALLOWED_EXTENSIONS))[0]
            if extension:  # if extensions are found

                # writing the scraped URLs in the text file in append mode
                self.items['link'] = str(response.url)

                # bypassing ssl
                ssl._create_default_https_context = ssl._create_unverified_context

                # calling urllib to create a reader of the pdf url
                r = urllib.request.urlopen(response.url)
                reader = PyPDF2.pdf.PdfFileReader(io.BytesIO(r.read()))

                # creating data string by scanning pdf pages
                data = ""
                for datas in reader.pages:
                    data += datas.extractText()
                # print(data)  #prints content in terminal

                self.items['content'] = str(data)
                yield self.items


# Implements spider for scraping MS Word Documents
@zope.interface.implementer(SpiderInterface)
class DocumentClass(CrawlSpider):
    #name = "doc_crawler"

    # parse() processes response and returns scraped data
    def parse(self, response):
        self.logger.info('Yippy! We have found: %s', response.url)  # shows a message with response
        if hasattr(response, "text"):
            pass  # we disregard any HTML text
        else:
            # filtering out extensions that are in our ALLOWED_EXTENSIONS list from the list of returned urls
            extension = list(filter(lambda x: response.url.lower().endswith(x), ALLOWED_EXTENSIONS))[0]
            if extension:
                # writing the scraped URLs in the text file in append mode
                self.items['link'] = str(response.url)

                # bypassing ssl
                ssl._create_default_https_context = ssl._create_unverified_context

                # r = urllib.request.urlopen(response.url)
                # reader = docx2python(io.BytesIO(r.read()))
                reader = docx2python(response.url)

                # creating data string by scanning text from docx file
                data = reader[0]
                print(data)  # prints content in terminal

                self.items['content'] = str(data)
                yield self.items


# Implements spider for scraping .txt files
@zope.interface.implementer(SpiderInterface)
class TextClass(CrawlSpider):
    name = "txt_crawler"

    # parse() processes response and returns scraped data
    def parse(self, response):
        self.logger.info('Yippy! We have found: %s', response.url)  # shows a message with response
        if hasattr(response, "text"):
            pass  # we disregard any HTML text
        else:
            # filtering out extensions that are in our ALLOWED_EXTENSIONS list from the list of returned urls
            extension = list(filter(lambda x: response.url.lower().endswith(x), ALLOWED_EXTENSIONS))[0]
            if extension:
                # writing the scraped URLs in the text file in append mode
                self.items['link'] = str(response.url)

                # bypassing ssl
                ssl._create_default_https_context = ssl._create_unverified_context

                # read data from txt file
                response = requests.get(response.url)

                # creating data string by scanning text from txt file
                data = ""
                data += response.text

                print(data)  # prints content in terminal

                self.items['content'] = str(data)
                yield self.items


# Implements spider for scraping HTML content
@zope.interface.implementer(SpiderInterface)
class HTMLClass(CrawlSpider):
    name = "html_crawler"

    # parse() processes response and returns scraped data
    def parse(self, response):
        self.logger.info('Yippy! We have found: %s', response.url)  # shows a message with response
        if hasattr(response, "text"):
            # bypassing ssl
            ssl._create_default_https_context = ssl._create_unverified_context

            # read HTML
            reader = urllib.request(response.url)

            root = lxml.html.fromstring(response.body)

            lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

            # creating data string by read HTML tags
            data = ""
            data += lxml.html.tostring(root, method="text", encoding=str)

            print(data)  # prints content in terminal

            self.items['content'] = str(data)
            yield self.items

        else:
            pass


ALLOWED_EXTENSIONS = []


# Abstract Factory for creating strategy objects
class StrategyFactory():

    @staticmethod
    def set_extension(strategy):

        ALLOWED_EXTENSIONS.clear()

        if strategy == "PDF Files":
            ALLOWED_EXTENSIONS.append(".pdf")

        elif strategy == "doc":
            ALLOWED_EXTENSIONS.append(".docx")

        elif strategy == "txt":
            ALLOWED_EXTENSIONS.append(".txt")

    @staticmethod
    def create_strategy(strategy):

        # creating a list of strategy objects
        object_list = []

        StrategyFactory.set_extension(strategy)

        if strategy == "PDF Files":
            object_list.append(PDFClass())

        elif strategy == "doc":
            object_list.append(DocumentClass())

        elif strategy == "txt":
            object_list.append(TextClass())

        # after introducing new strategies append here:

        elif strategy == "All Content":
            object_list.append(HTMLClass())
            object_list.append(PDFClass())
            object_list.append(DocumentClass())
            object_list.append(TextClass())

        # after introducing new non-html strategies append here:

        elif strategy == "Non-HTML":
            object_list.append(PDFClass())
            object_list.append(DocumentClass())
            object_list.append(TextClass())

        return object_list


# StrategyLinkExtractor subclasses LinkExtractor
class StrategyLinkExtractor(LinkExtractor):
    def __init__(self, *args, **kwargs):
        super(StrategyLinkExtractor, self).__init__(*args, **kwargs)
        # leaving default values in "deny_extensions" other than the ones we want.
        self.deny_extensions = [ext for ext in self.deny_extensions if ext not in ALLOWED_EXTENSIONS]


start_urls = [""]


# Spider subclasses CrawlSpider
class Spider(CrawlSpider, ABC):
    name = "MainSpider"

    # start_urls = []

    # useful links for crawling:
    # 'https://www.imagescape.com/media/uploads/zinnia/2018/08/20/scrape_me.html',
    # book
    # https://codex.cs.yale.edu/avi/os-book/OSE2/index.html,
    # review ques
    # https://codex.cs.yale.edu/avi/os-book/OSE2/review-dir/index.html,
    # practice questions
    # https://codex.cs.yale.edu/avi//os-book/OS9/practice-exer-dir/index.html,
    # 311db -practice exercises
    # https://www.db-book.com/Practice-Exercises/index-solu.html,

    def __init__(self, *args, **kwargs):
        self.get_objects_in_queue()

        # Follows the rule set in StrategyLinkExtractor class
        # parse() method is used for parsing the data
        # CrawlSpider-based spiders have internal implementation, so we explicitly set callbacks for new requests to avoid unexpected behaviour
        self.rules = (
            Rule(StrategyLinkExtractor(), follow=True, callback="parse", process_links=None, process_request=None,
                 errback=None),)
        super(Spider, self).__init__(*args, **kwargs)

    strategy_list = []

    # custom settings for spider
    custom_settings = {
        'DOWNLOAD_DELAY': 0,  # default download_delay
        'DEPTH_LIMIT': 1,  # default depth_limit
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }

    # instantiating CrawlingItem to carry data to pipelines which then stores each item in each link_tb (database) row
    items = CrawlingItem()

    def set_urls(self, urltext):
        # cleaning urltext
        urls_list = urltext.split(",")
        for url in urls_list:
            url = url.strip()  # trims whitespace
            start_urls.append(url)  # each url is appended to start_urls list

    # sets depth in spider's custom settings
    def set_depth(self, depth):
        self.custom_settings.update({'DEPTH_LIMIT': depth})
        # updates the default depth limit

    def set_strategy(self, depth):
        self.custom_settings.update({'DEPTH_LIMIT': depth})

    def get_objects_in_queue(self):
        objects_in_queue = CrawlingQueue.objects.all()  # fetches all objects from DB table
        for object_in_queue in objects_in_queue:
            # attributes of the objects are passed to items
            self.items['clustername'] = object_in_queue.clusterName
            self.items['username'] = object_in_queue.userName

            # setting depth_limit using user input
            self.set_depth(object_in_queue.depth)

            # setting start_urls using user input
            self.set_urls(object_in_queue.url)

            # self.set_strategy(object_in_queue.url)

            self.strategy_list = StrategyFactory.create_strategy(object_in_queue.strategy)
            # gets list of strategy objects from StrategyFactory class
            # for each object representing a strategy class, its parse method is invoked
            # for obj in StrategyFactory.create_strategy(object_in_queue.strategy):
            #    obj.parse(self, response)

            # printing list of start_urls in terminal (for client developer)
            print(self.start_urls)

    def parse(self, response):
        for obj in self.strategy_list:
            obj.parse(self, response)


#process = CrawlerProcess()
#process.crawl(PDFClass)
#process.crawl(DocumentClass)
#process.start() # the script will block here until all crawling jobs are finished


class PDFClass(CrawlSpider):
    name = "pdf_crawler"

    start_urls = []

    objects_in_queue = CrawlingQueue.objects.all().filter(strategy='PDF Files', depth=2)

    crawled = []
    crawledQueueObjects = CrawledQueue.objects.all()

    for x in crawledQueueObjects:
        crawled.append(x.url)

    # instantiating CrawlingItem to carry data to pipelines which then stores each item in each link_tb (database) row

    
            # self.set_strategy(object_in_queue.url)
    ALLOWED_EXTENSIONS.append(".pdf")
            # self.strategy_list = StrategyFactory.create_strategy(object_in_queue.strategy)
            # gets list of strategy objects from StrategyFactory class
            # for each object representing a strategy class, its parse method is invoked
            # for obj in StrategyFactory.create_strategy(object_in_queue.strategy):
            #    obj.parse(self, response)

            # printing list of start_urls in terminal (for client developer)

    def __init__(self, *args, **kwargs):
        for object_in_queue in self.objects_in_queue:
            urltext = object_in_queue.url
            urls_list = urltext.split(",")
            for url in urls_list:
                url = url.strip()  # trims whitespace
                if url not in self.crawled:
                    self.start_urls.append(url)

                    x = CrawledQueue(url = url)
                    x.save()
                


        # Follows the rule set in StrategyLinkExtractor class
        # parse() method is used for parsing the data
        # CrawlSpider-based spiders have internal implementation, so we explicitly set callbacks for new requests to avoid unexpected behaviour
        self.rules = (
            Rule(StrategyLinkExtractor(), follow=True, callback="parse", process_links=None, process_request=None,
                 errback=None),)
        super(PDFClass, self).__init__(*args, **kwargs)

    def parse(self, response):
        self.logger.info('Yippee! We have found: %s', response.url)
        # shows a message with response
        if hasattr(response, "text"):
            pass  # we disregard any HTML text
        else:
            # filtering out extensions that are in our ALLOWED_EXTENSIONS list from the list of returned urls
            extension = list(filter(lambda x: response.url.lower().endswith(x), ALLOWED_EXTENSIONS))[0]
            if extension:  # if extensions are found
                items = CrawlingItem()
                
                print("Domain URL = ")
                print(response.request.url)

                items['username'] = 'Hehe'
                items['clustername'] = 'Hehe'

                # writing the scraped URLs in the text file in append mode
                items['link'] = str(response.url)

                # bypassing ssl
                ssl._create_default_https_context = ssl._create_unverified_context

                # calling urllib to create a reader of the pdf url
                r = urllib.request.urlopen(response.url)
                reader = PyPDF2.pdf.PdfFileReader(io.BytesIO(r.read()))

                # creating data string by scanning pdf pages
                data = ""
                for datas in reader.pages:
                    data += datas.extractText()
                # print(data)  #prints content in terminal

                items['content'] = str(data)
                yield items

class TextClass(CrawlSpider):
    name = "txt_crawler"

    start_urls = []

    objects_in_queue = CrawlingQueue.objects.all().filter(strategy='TEXT Files')
    # custom settings for spider
    custom_settings = {
        'DOWNLOAD_DELAY': 0,  # default download_delay
        'DEPTH_LIMIT': 1,  # default depth_limit
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }

    ALLOWED_EXTENSIONS.append(".txt")

    def __init__(self, *args, **kwargs):
        for object_in_queue in self.objects_in_queue:
            self.custom_settings.update({'DEPTH_LIMIT': object_in_queue.depth})
            urltext = object_in_queue.url
            urls_list = urltext.split(",")
            for url in urls_list:
                url = url.strip()  # trims whitespace
                if url not in self.start_urls:
                    self.start_urls.append(url)

        # Follows the rule set in StrategyLinkExtractor class
        # parse() method is used for parsing the data
        # CrawlSpider-based spiders have internal implementation, so we explicitly set callbacks for new requests to avoid unexpected behaviour
        self.rules = (
            Rule(StrategyLinkExtractor(), follow=True, callback="parse", process_links=None, process_request=None,
                 errback=None),)
        super(TextClass, self).__init__(*args, **kwargs)

    # parse() processes response and returns scraped data
    def parse(self, response):
        response.replace(url = 'https://www.gutenberg.org/files/10/10-0.txt')

        self.logger.info('Yippy! We have found: %s', response.url)  # shows a message with response
        if hasattr(response, "text"):
            pass  # we disregard any HTML text
        else:
            # filtering out extensions that are in our ALLOWED_EXTENSIONS list from the list of returned urls
            extension = list(filter(lambda x: response.url.lower().endswith(x), ALLOWED_EXTENSIONS))[0]
            if extension:
                items = CrawlingItem()
                for object_in_queue in self.objects_in_queue:
                    items['username'] = object_in_queue.userName
                    items['clustername'] = object_in_queue.clusterName

                # writing the scraped URLs in the text file in append mode
                items['link'] = str(response.url)

                # bypassing ssl
                ssl._create_default_https_context = ssl._create_unverified_context

                # read data from txt file
                response = requests.get(response.url)

                # creating data string by scanning text from txt file
                data = ""
                data += response.text

                items['content'] = str(data)
                yield items

class DocSpider(CrawlSpider):
    name = "doc_crawler"

    start_urls = []

    objects_in_queue = CrawlingQueue.objects.all().filter(strategy='DOC Files')

    crawled = []
    crawledQueueObjects = CrawledQueue.objects.all()

    for x in crawledQueueObjects:
        crawled.append(x.url)

    # custom settings for spider
    custom_settings = {
        'DOWNLOAD_DELAY': 0,  # default download_delay
        'DEPTH_LIMIT': 1,  # default depth_limit
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
    }

    ALLOWED_EXTENSIONS = [".docx"]

    def __init__(self, *args, **kwargs):
        for object_in_queue in self.objects_in_queue:
            self.custom_settings.update({'DEPTH_LIMIT': 2})
            urltext = object_in_queue.url
            urls_list = urltext.split(",")
            for url in urls_list:
                url = url.strip()  # trims whitespace

                self.start_urls.append(url)
                if url not in self.crawled:
                    self.start_urls.append(url)
                    
                    temp = CrawledQueue(url = url)
                    temp.save()

        # Follows the rule set in StrategyLinkExtractor class
        # parse() method is used for parsing the data
        # CrawlSpider-based spiders have internal implementation, so we explicitly set callbacks for new requests to avoid unexpected behaviour
        self.rules = (
            Rule(StrategyLinkExtractor(), follow=True, callback="parse", process_links=None, process_request=None,
                 errback=None),)
        super(DocSpider, self).__init__(*args, **kwargs)


    # parse() processes response and returns scraped data
    def parse(self, response):
        self.logger.info('Yippy! We have found: %s', response.url)  # shows a message with response
        if hasattr(response, "text"):
            pass  # we disregard any HTML text
        else:
            items = CrawlingItem()
            
            print("Current start url = ")
            print(response.request.url)

            # filtering out extensions that are in our ALLOWED_EXTENSIONS list from the list of returned urls
            extension = list(filter(lambda x: response.url.lower().endswith(x), ALLOWED_EXTENSIONS))[0]
            if extension:
                # writing the scraped URLs in the text file in append mode
                items['link'] = str(response.url)
                # bypassing ssl
                ssl._create_default_https_context = ssl._create_unverified_context
                #r = urllib.request.urlopen(response.url)
                #reader = docx2python(io.BytesIO(r.read()))
                reader = docx2python(response.url)

                # creating data string by scanning text from docx file
                data = reader[0]

                items['content'] = str(data)
                yield items