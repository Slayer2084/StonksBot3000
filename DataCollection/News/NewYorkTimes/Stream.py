from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals
from NYT import NYTRecentSpider


class NYTStreamer:
    def __init__(self):
        self.list = []

    def get_new_data(self, date):
        self.list = []
        dispatcher.connect(self.catch_item, signal=signals.item_passed)
        crawler = CrawlerProcess()
        crawler.crawl(NYTRecentSpider, date=date)
        crawler.start()
        return self.list

    def catch_item(self, sender, item, **kwargs):
        self.list.append(item)


if __name__ == '__main__':
    streamer = NYTStreamer()
    print(streamer.get_new_data("2022-02-16T10:49:53-05:00"))
