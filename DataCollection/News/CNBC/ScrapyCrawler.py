import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scraper_helper as sh


class CNBCSpider(CrawlSpider):
    name = 'CNBC-Extractor'
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    allowed_domains = ['cnbc.com']
    start_urls = ['https://cnbc.com/investing/']
    custom_settings = {
        'LOG_LEVEL': 'WARN',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
    }

    card_title_le = LinkExtractor(restrict_css=".Card-title")
    load_more_le = LinkExtractor(restrict_css=".LoadMoreButton-loadMore")
    categories_le = LinkExtractor(restrict_css=".nav-menu-button")

    card_title_rule = Rule(card_title_le, callback='parse_item', follow=False)
    load_more_rule = Rule(load_more_le, follow=True)
    categories_rule = Rule(categories_le, follow=True)

    rules = (
        card_title_rule,
        load_more_rule,
        categories_rule

    )

    def parse_item(self, response):
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
