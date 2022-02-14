import scrapy
import scraper_helper as sh


base = "https://webql-redesign.cnbcfm.com/graphql?operationName=getAssetList&variables=%7B%22id%22%3A%22{}%22%2C%22offset%22%3A{}%2C%22pageSize%22%3A24%2C%22nonFilter%22%3Atrue%2C%22includeNative%22%3Afalse%2C%22include%22%3A%5B%5D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22202314eccd1b9d973b75758156268b4fe5181b60cc2e9d3b0b76c1c617604b60%22%7D%7D"


class IDs2URLsSpider(scrapy.Spider):
    name = 'IDs2URLs'
    with open("./ids/ids.txt", "r") as f:
        ids = f.readlines()
    start_urls = []
    for id in ids:
        for offset in range(500):
            start_urls.append(base.format(id, offset))
    custom_settings = {
        'LOG_LEVEL': 'WARN'
    }

    def parse(self, response):
        try:
            data = response.json()["data"]
            assets = data["assetList"]["assets"]
            for asset in assets:
                url = asset["url"]
                item = {
                    "urls": url
                }
                yield item
        except KeyError:
            pass


if __name__ == '__main__':
    sh.run_spider(IDs2URLsSpider)
