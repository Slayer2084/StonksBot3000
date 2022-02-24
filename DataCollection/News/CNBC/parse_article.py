def parse_article(response):
    print(".")
    content = "".join(response.css(".ArticleBody-subtitle , .group p").css("::text").getall())
    yield {
        'Title': response.css(".ArticleHeader-headline ::text").get(),
        'Category': response.css(".ArticleHeader-eyebrow ::text").get(),
        'Author': response.css(".Author-authorName ::text").get(),
        'Content': content,
        'Description': response.css("#RegularArticle-KeyPoints-4 li").css("::text").getall(),
        'Time': response.css(".ArticleHeader-timeHidden > time").css('::attr(datetime)').get(),
        'Link': response.url,
        'Origin': "CNBC",
    }
