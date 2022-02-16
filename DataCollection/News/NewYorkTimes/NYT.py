import scrapy
from scrapy import FormRequest
import scraper_helper as sh
import datetime
from Creds import API_KEY

"https://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key={}"


class NYTSpider(scrapy.Spider):
    name = 'NYT'
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

    def parse(self, response):
        data = response.json()
        articles = data["response"]["docs"]
        for article in articles:
            yield scrapy.Request(article["web_url"], callback=self.parse_article)

    def parse_article(self, response):
        pass


if __name__ == '__main__':
    sh.run_spider(NYTSpider)
