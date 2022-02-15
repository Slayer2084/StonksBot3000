import scrapy
import scraper_helper as sh
import re

url = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query={}%22%20%22%20&endindex={}&batchsize=100&callback=&showfaceted=false&timezoneoffset=-60&facetedfields=formats&facetedkey=formats%7C&facetedvalue=!Press%20Release%7C&additionalindexes=4cd6f71fbf22424d,937d600b0d0d4e23,3bfbe40caee7443e,626fdfcd96444f28"


class CNBCSpider(scrapy.Spider):
    name = 'CNBC'
    allowed_domains = ["api.queryly.com", "cnbc.com"]
    start_urls = []

    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
        'ROBOTSTXT_OBEY': False,
        # 'PROXY_POOL_ENABLED': True,
        # 'DOWNLOADER_MIDDLEWARES': {
        #     'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
        #     'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
        # }
    }

    def start_requests(self):
        queries = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                   'v', 'w', 'x', 'y', 'z']
        for query in queries:
            yield scrapy.Request(url.format(query, 0), callback=self.parse)

    def parse(self, response):
        metadata = response.json()["metadata"]
        total_pages = metadata["totalpage"]
        current_page = metadata["pagerequested"]

        # print(re.search(r'query=(.*?)%22', response.url).group(1) + ": " + str(current_page))

        if total_pages and current_page:
            if int(current_page) == 1:
                for i in range(100, (int(total_pages)+1)*100, 100):
                    yield scrapy.Request(url=url.format(re.search(r'query=(.*?)%22', response.url).group(1), i), callback=self.parse)

        for result in response.json()["results"]:
            if result["brand"] == "cnbc":
                if result["cn:type"] != "cnbcvideo":
                    yield scrapy.Request(result["cn:liveURL"], callback=self.parse_articles)

    def parse_articles(self, response):
        # print(".", flush=False, end="")
        yield {
            'Title': response.css(".ArticleHeader-headline ::text").get(),
            'Category': response.css(".ArticleHeader-eyebrow ::text").get(),
            'Author': response.css(".Author-authorName ::text").get(),
            'Content': response.css(".ArticleBody-subtitle , .group p").css("::text").getall(),
            'Description': response.css("#RegularArticle-KeyPoints-4 li").css("::text").getall(),
            'Time': response.css(".ArticleHeader-timeHidden > time").css('::attr(datetime)').get(),
            'Link': response.url
        }


if __name__ == '__main__':
    sh.run_spider(CNBCSpider)
