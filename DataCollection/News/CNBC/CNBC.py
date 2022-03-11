import time
import ciso8601
import scrapy
from DataCollection.News.CNBC.parse_article import parse_article

url_stream = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query=cnbc&endindex={" \
             "}&batchsize=100&timezoneoffset=-60&sort=date"
url_new_article_spider = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query=cnbc&endindex" \
                         "=0&batchsize=100&timezoneoffset=-60&sort=date "


class CNBCNewArticleSpider(scrapy.Spider):
    name = 'CNBCNewArticleSpider'
    allowed_domains = ["api.queryly.com", "cnbc.com"]
    start_urls = []
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
    }

    def __init__(self, **kwargs):
        self.last_id = 0
        super().__init__(**kwargs)

    def last_id_setter(self, response):
        newest_result = response.json()["results"][0]
        self.last_id = newest_result["@id"]

    def start_requests(self):
        yield scrapy.Request(url_new_article_spider, callback=self.last_id_setter)
        yield scrapy.Request(url_new_article_spider, callback=self.parse)

    def parse(self, response, **kwargs):
        newest_result = response.json()["results"][0]
        id = newest_result["@id"]
        if id > self.last_id:
            yield scrapy.Request(newest_result["cn:liveURL"], callback=parse_article)
            self.last_id = id
        yield scrapy.Request(response.url(), callback=self.parse)


class CNBCSpider(scrapy.Spider):
    name = 'CNBC'

    allowed_domains = ["api.queryly.com", "cnbc.com"]
    start_urls = []
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.5,
        'JOBDIR': './job',
    }

    def __init__(self, from_time, until_time, **kwargs):
        self.from_time = from_time
        self.until_time = until_time
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url_stream.format(0), callback=self.parse)

    def parse(self, response, **kwargs):
        data = response.json()
        metadata = data["metadata"]
        total_pages = metadata["totalpage"]
        current_page = metadata["pagerequested"]
        print(current_page)
        last_date = time.mktime(ciso8601.parse_datetime(data["results"][-1]["datePublished"]).timetuple())

        if current_page:
            if current_page <= total_pages:
                if last_date > self.from_time:
                    yield scrapy.Request(
                        url=url_stream.format((current_page+1) * 100),
                        callback=self.parse)

        for result in data["results"]:
            if time.mktime(ciso8601.parse_datetime(result["datePublished"]).timetuple()) <= self.from_time:
                break
            if time.mktime(ciso8601.parse_datetime(result["datePublished"]).timetuple()) >= self.until_time:
                break
            if result["brand"] == "cnbc":
                if result["cn:type"] != "cnbcvideo":
                    yield scrapy.Request(result["cn:liveURL"], callback=parse_article)


if __name__ == '__main__':
    from scrapy.signalmanager import dispatcher
    from scrapy.crawler import CrawlerProcess
    from scrapy import signals

    def catch_item(item):
        pass

    dispatcher.connect(catch_item, signal=signals.item_passed)
    process = CrawlerProcess()
    process.crawl(CNBCSpider, from_time=943920000, until_time=946598400)
    process.start()
