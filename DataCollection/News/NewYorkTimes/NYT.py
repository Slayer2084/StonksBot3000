import scrapy
import scraper_helper as sh
import datetime
from DataCollection.News.Creds import API_KEY
import ciso8601
import time
from parse_article import parse_article


class NYTArchiveSpider(scrapy.Spider):
    name = 'NYTArchive'
    allowed_domains = ['api.nytimes.com', 'nytimes.com']
    custom_settings = {
        'LOG_LEVEL': "WARN",
        'DOWNLOAD_DELAY': 6
    }

    def start_requests(self):
        url_api = "https://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key=" + API_KEY
        date_now = datetime.datetime.now().date()
        year_now = int(date_now.strftime("%Y"))
        for year in range(1851, year_now):
            for month in range(1, 13):
                yield scrapy.Request(url_api.format(year, month))
        for _month in range(1, int(date_now.strftime("%m"))+1):
            yield scrapy.Request(url_api.format(year_now, _month))

    def parse(self, response, **kwargs):
        data = response.json()
        articles = data["response"]["docs"]
        for article in articles:
            yield scrapy.Request(article["web_url"], callback=parse_article)


class NYTRecentSpider(scrapy.Spider):
    def __init__(self, date, **kwargs):
        self.date = date
        super().__init__(**kwargs)

    name = 'NYTRecent'
    allow_domains = ['api.nytimes.com', 'nytimes.com']
    custom_settings = {
        'LOG_LEVEL': "WARN",
        'DOWNLOAD_DELAY': 6
    }

    def start_requests(self):
        url_api = "https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=" + API_KEY + "&limit=500"
        yield scrapy.Request(url_api, callback=self.parse)

    def parse(self, response, **kwargs):
        print(".")
        data = response.json()
        if data["status"] != "OK":
            yield scrapy.Request(response.url)
        else:
            for article in data["results"]:
                if time.mktime(ciso8601.parse_datetime(article["published_date"]).timetuple()) > self.date:
                    yield scrapy.Request(article["url"], callback=parse_article)


if __name__ == '__main__':
    sh.run_spider(NYTRecentSpider)
