import re
import time
import ciso8601
import scraper_helper as sh
import scrapy
from DataCollection.News.CNBC.parse_article import parse_article

url = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query={}%22%20%22%20&endindex={" \
      "}&batchsize=100&callback=&showfaceted=false&timezoneoffset=-60&facetedfields=formats&facetedkey=formats%7C" \
      "&facetedvalue=!Press%20Release%7C&additionalindexes=4cd6f71fbf22424d,937d600b0d0d4e23,3bfbe40caee7443e," \
      "626fdfcd96444f28 "
url_stream = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query={}&endindex={" \
             "}&batchsize=100&callback=&showfaceted=false&timezoneoffset=-60&facetedfields=formats&facetedkey=formats" \
             "%7C&facetedvalue=!Press%20Release%7C&sort=date&additionalindexes=4cd6f71fbf22424d,937d600b0d0d4e23," \
             "3bfbe40caee7443e,626fdfcd96444f28 "


class CNBCArchiveSpider(scrapy.Spider):
    name = 'CNBCArchive'
    allowed_domains = ["api.queryly.com", "cnbc.com"]
    start_urls = []

    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1', 
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self, until_time, **kwargs):
        self.until_time = until_time
        super().__init__(**kwargs)

    def start_requests(self):
        queries = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                   'v', 'w', 'x', 'y', 'z']
        for query in queries:
            yield scrapy.Request(url.format(query, 0), callback=self.parse)

    def parse(self, response, **kwargs):
        metadata = response.json()["metadata"]
        total_pages = metadata["totalpage"]
        current_page = metadata["pagerequested"]

        if total_pages and current_page:
            if int(current_page) == 1:
                for i in range(100, (int(total_pages) + 1) * 100, 100):
                    yield scrapy.Request(url=url.format(re.search(r'query=(.*?)%22', response.url).group(1), i),
                                         callback=self.parse)

        for result in response.json()["results"]:
            if time.mktime(ciso8601.parse_datetime(result["datePublished"]).timetuple()) >= self.until_time:
                break
            if result["brand"] == "cnbc":
                if result["cn:type"] != "cnbcvideo":
                    yield scrapy.Request(result["cn:liveURL"], callback=parse_article)


class CNBCRecentSpider(scrapy.Spider):
    name = 'CNBCRecent'
    allowed_domains = ["api.queryly.com", "cnbc.com"]
    start_urls = []

    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'PROXY_POOL_ENABLED': True,
        'DOWNLOAD_DELAY': 3
    }

    def __init__(self, date, until_time, **kwargs):
        self.date = date
        self.until_time = until_time
        super().__init__(**kwargs)

    def start_requests(self):
        queries = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                   'v', 'w', 'x', 'y', 'z']
        for query in queries:
            yield scrapy.Request(url_stream.format(query, 0), callback=self.parse)

    def parse(self, response, **kwargs):
        current_page = response.json()["metadata"]["pagerequested"]
        last_date = time.mktime(ciso8601.parse_datetime(response.json()["results"][-1]["datePublished"]).timetuple())

        if current_page:
            if last_date > self.date:
                yield scrapy.Request(
                    url=url_stream.format(re.search(r'query=(.*?)&', response.url).group(1), current_page + 1),
                    callback=self.parse)

        for result in response.json()["results"]:
            if time.mktime(ciso8601.parse_datetime(result["datePublished"]).timetuple()) <= self.date:
                break
            if time.mktime(ciso8601.parse_datetime(result["datePublished"]).timetuple()) >= self.until_time:
                break
            if result["brand"] == "cnbc":
                if result["cn:type"] != "cnbcvideo":
                    yield scrapy.Request(result["cn:liveURL"], callback=parse_article)


if __name__ == '__main__':
    sh.run_spider(CNBCRecentSpider)
