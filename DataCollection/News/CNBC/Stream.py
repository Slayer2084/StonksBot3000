from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from CNBC import CNBCRecentSpider


class CNBCStreamer:
    def __init__(self):
        self.list = []

    def get_new_data(self, max_pages):
        self.list = []
        dispatcher.connect(self.catch_item, signal=signals.item_passed)
        crawler = CrawlerProcess()
        crawler.crawl(CNBCRecentSpider, max_pages=max_pages)
        crawler.start()
        return self.list

    def catch_item(self, sender, item, **kwargs):
        self.list.append(item)


if __name__ == '__main__':
    streamer = CNBCStreamer()
    print(streamer.get_new_data(1))
