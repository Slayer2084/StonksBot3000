from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals


class Streamer:
    def __init__(self, spider):
        self.spider = spider
        self.list = []

    def get_new_data(self, from_time: float, until_time: float):
        self.list = []
        dispatcher.connect(self.catch_item, signal=signals.item_passed)
        crawler = CrawlerProcess()
        crawler.crawl(self.spider, from_time=from_time, until_time=until_time)
        crawler.start()
        return self.list

    def catch_item(self, sender, item, **kwargs):
        self.list.append(item)


if __name__ == '__main__':
    from CNBC.CNBC import CNBCSpider
    nyt_streamer = Streamer(CNBCSpider)
    print(nyt_streamer.get_new_data(1645475501, 1645562082))
