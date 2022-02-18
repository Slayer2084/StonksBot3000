def parse_article(response):
    print(".")
    yield {
        'Title': response.css().get(),
        'Category': response.css().get(),
        'Author': response.css().get(),
        'Content': response.css().get(),
        'Description': response.css().getall(),
        'Time': response.css().get(),
        'Link': response.url
    }
