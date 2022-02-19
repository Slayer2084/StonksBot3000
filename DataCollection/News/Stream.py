from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals


class Streamer:
    def __init__(self, spider):
        self.spider = spider
        self.list = []

    def get_new_data(self, date: int):
        self.list = []
        dispatcher.connect(self.catch_item, signal=signals.item_passed)
        crawler = CrawlerProcess()
        crawler.crawl(self.spider, date=date)
        crawler.start()
        return self.list

    def catch_item(self, sender, item, **kwargs):
        self.list.append(item)


if __name__ == '__main__':
    from CNBC.CNBC import CNBCRecentSpider
    nyt_streamer = Streamer(CNBCRecentSpider)
    print(nyt_streamer.get_new_data(1645188211))
