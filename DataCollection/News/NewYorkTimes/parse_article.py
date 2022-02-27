def parse_article(response):
    print("-")  # Todo: Add NYT workaround to access article data
    yield {
        'Title': response,
        'Category': response,
        'Author': response,
        'Content': response,
        'Description': response,
        'Time': response,
        'Section': response,
        'Link': response.url,
        'Origin': "NYT",
    }
