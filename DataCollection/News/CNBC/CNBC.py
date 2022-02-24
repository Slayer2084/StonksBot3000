import time
import ciso8601
import scraper_helper as sh
import scrapy
from DataCollection.News.CNBC.parse_article import parse_article

url_stream = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query={}&endindex={" \
             "}&batchsize=100&callback=&showfaceted=false&timezoneoffset=-60&facetedfields=formats&facetedkey=formats" \
             "%7C&facetedvalue=!Press%20Release%7C&sort=date&additionalindexes=4cd6f71fbf22424d,937d600b0d0d4e23," \
             "3bfbe40caee7443e,626fdfcd96444f28"


class CNBCSpider(scrapy.Spider):
    name = 'CNBC'
    allowed_domains = ["api.queryly.com", "cnbc.com"]
    start_urls = []

    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 0.5
    }

    def __init__(self, from_time, until_time, **kwargs):
        self.from_time = from_time
        self.until_time = until_time
        super().__init__(**kwargs)

    def start_requests(self):
        queries = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                   'v', 'w', 'x', 'y', 'z']
        for query in queries:
            yield scrapy.Request(url_stream.format(query, 0), callback=self.parse, cb_kwargs=dict(query=query))

    def parse(self, response, query, **kwargs):
        data = response.json()
        metadata = data["metadata"]
        total_pages = metadata["totalpage"]
        current_page = metadata["pagerequested"]
        last_date = time.mktime(ciso8601.parse_datetime(data["results"][-1]["datePublished"]).timetuple())

        if current_page:
            if current_page <= total_pages:
                if last_date > self.from_time:
                    yield scrapy.Request(
                        url=url_stream.format(query, (current_page+1) * 100),
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
    sh.run_spider(CNBCSpider)
