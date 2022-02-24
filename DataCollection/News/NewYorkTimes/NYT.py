import scrapy
import scraper_helper as sh
import datetime
from DataCollection.News.Creds import API_KEY
import ciso8601
import time
from DataCollection.News.NewYorkTimes.parse_article import parse_article


class NYTArchiveSpider(scrapy.Spider):
    name = 'NYTArchive'
    allowed_domains = ['api.nytimes.com', 'nytimes.com']
    custom_settings = {
        'LOG_LEVEL': "WARN",
        'DOWNLOAD_DELAY': 6
    }

    def __init__(self, until_time, **kwargs):
        self.until_time = until_time
        super().__init__(**kwargs)

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
            if time.mktime(ciso8601.parse_datetime(article["published_date"]).timetuple()) >= self.until_time:
                break
            yield scrapy.Request(article["web_url"], callback=parse_article)


class NYTRecentSpider(scrapy.Spider):
    name = 'NYTRecent'
    allow_domains = ['api.nytimes.com', 'nytimes.com']
    custom_settings = {
        'LOG_LEVEL': "WARN",
        'DOWNLOAD_DELAY': 6
    }

    def __init__(self, from_time, until_time, **kwargs):
        self.from_time = from_time
        self.until_time = until_time
        super().__init__(**kwargs)

    def start_requests(self):
        url_api = "https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=" + API_KEY + "&limit=500"
        yield scrapy.Request(url_api, callback=self.parse)

    def parse(self, response, **kwargs):
        data = response.json()
        if data["status"] != "OK":
            yield scrapy.Request(response.url)
        else:
            for article in data["results"]:
                if time.mktime(ciso8601.parse_datetime(article["published_date"]).timetuple()) <= self.from_time:
                    break
                if time.mktime(ciso8601.parse_datetime(article["published_date"]).timetuple()) >= self.until_time:
                    break
                yield scrapy.Request(article["url"], callback=parse_article)


if __name__ == '__main__':
    sh.run_spider(NYTRecentSpider)
