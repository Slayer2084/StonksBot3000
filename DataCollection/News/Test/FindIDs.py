import scrapy
import scraper_helper as sh
import re

base = "https://webql-redesign.cnbcfm.com/graphql?operationName=getAssetList&variables=%7B%22id%22%3A%22{}%22%2C%22offset%22%3A1%2C%22pageSize%22%3A24%2C%22nonFilter%22%3Atrue%2C%22includeNative%22%3Afalse%2C%22include%22%3A%5B%5D%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%22202314eccd1b9d973b75758156268b4fe5181b60cc2e9d3b0b76c1c617604b60%22%7D%7D"


class ID_Spider(scrapy.Spider):
    name = 'ID'
    rate = 5
    start_urls = [base.format(1)]
    custom_settings = {
        'LOG_LEVEL': 'WARN'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.download_delay = 1 / float(self.rate)

    def start_requests(self):
        urls = []
        for i in range(2_500_000_000):
            urls.append(base.format(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.json()
        if data["data"]["assetList"] is not None:
            if data["data"]["assetList"]["assets"] is not None:
                if len(data["data"]["assetList"]["assets"]) > 0:
                    data = response.json()
                    id = data["data"]["assetList"]["id"]
                    print("- ", id)
                    with open('ids/ids.txt', "a") as f:
                        f.write(str(id) + "\n")
                else:
                    print(re.search("id%22%3A%22(.*?)%22%2C", response.url).group(1))
            else:
                print(re.search("id%22%3A%22(.*?)%22%2C", response.url).group(1))
        else:
            print(re.search("id%22%3A%22(.*?)%22%2C", response.url).group(1))


if __name__ == '__main__':
    sh.run_spider(ID_Spider)
