import scrapy
import scraper_helper as sh
import datetime
from DataCollection.News.Creds import API_KEY
import ciso8601
import time
from DataCollection.News.NewYorkTimes.parse_article import parse_article


class NYTSpider(scrapy.Spider):
    name = 'NYT'
    allowed_domains = ['api.nytimes.com', 'nytimes.com']
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 '
                      'Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 6,
        'JOBDIR': './job',
    }

    def __init__(self, from_time, until_time, **kwargs):
        self.from_time = from_time
        self.until_time = until_time
        if time.time() - self.until_time <= 86400:
            self.recent = True
        else:
            self.recent = False
        super().__init__(**kwargs)

    def start_requests(self):
        if not self.recent:
            url_api = "https://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key=" + API_KEY
            year_min = int(datetime.datetime.fromtimestamp(self.from_time).strftime('%Y'))
            date_max = datetime.datetime.fromtimestamp(self.until_time)
            year_max = int(date_max.strftime('%Y'))
            month_max = int(date_max.strftime('%m'))

            for year in range(year_min, year_max):
                for month in range(1, 13):
                    yield scrapy.Request(url_api.format(year, month))
            for _month in range(1, month_max + 1):
                yield scrapy.Request(url_api.format(year_max, _month))
        else:
            url_api = "https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key=" + API_KEY + "&limit=500"
            yield scrapy.Request(url_api, callback=self.parse)

    def parse(self, response, **kwargs):
        data = response.json()
        if not self.recent:
            articles = data["response"]["docs"]
        else:
            articles = data["results"]
        for article in articles:
            if not self.recent:
                pub_date = article["pub_date"]
            else:
                pub_date = article["published_date"]
            pub_date = time.mktime(ciso8601.parse_datetime(pub_date).timetuple())
            if pub_date <= self.from_time:
                break
            if pub_date >= self.until_time:
                break
            if not self.recent:
                url = article["web_url"]
            else:
                url = article["url"]
            yield scrapy.Request(url=url, callback=parse_article)


if __name__ == '__main__':
    sh.run_spider(NYTSpider)
