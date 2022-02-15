import scrapy
from scrapy import FormRequest
import scraper_helper as sh
import json

url = "https://samizdat-graphql.nytimes.com/graphql/v2"


class NYTSpider(scrapy.Spider):
    name = 'NYT'
    start_urls = ['']

    def start_requests(self):
        headers = {
            'authority': 'samizdat-graphql.nytimes.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'nyt-token': 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs+/oUCTBmD/cLdmcecrnBMHiU/pxQCn2DDyaPKUOXxi4p0uUSZQzsuq1pJ1m5z1i0YGPd1U1OeGHAChWtqoxC7bFMCXcwnE1oyui9G1uobgpm1GdhtwkR7ta7akVTcsF8zxiXx7DNXIPd2nIJFH83rmkZueKrC4JVaNzjvD+Z03piLn5bHWU6+w+rA+kyJtGgZNTXKyPh6EC6o5N+rknNMG5+CdTq35p8f99WjFawSvYgP9V64kgckbTbtdJ6YhVP58TnuYgr12urtwnIqWP9KSJ1e5vmgf3tunMqWNm6+AnsqNj8mCLdCuc5cEB74CwUeQcP2HQQmbCddBy2y0mEwIDAQAB',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
            'nyt-app-type': 'project-vi',
            'content-type': 'application/json',
            'accept': '*/*',
            'nyt-app-version': '0.0.5',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'https://www.nytimes.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.nytimes.com/',
            'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'nyt-a=Btqw4F1JfqZtpLTsVSkW7R; nyt-gdpr=1; nyt-geo=DE; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; edu_cig_opt=%7B%22isEduUser%22%3Afalse%7D; _gcl_au=1.1.1901416451.1644951795; walley=GA1.2.1635182678.1644951795; walley_gid=GA1.2.2007430354.1644951795; FPC=id=c4c4a816-b787-434b-a01c-0de1ace143f2; WTPERSIST=; LPVID=Q5MGNjYzBiNzg4MzE5Yzgz; LPSID-17743901=w_9GUHCjR-6nteWyWuuD2g; purr-pref-agent=<Gi; __gads=ID=e49e3ec16d6c38be:T=1644951802:S=ALNI_MYyb3aVm44ErGRuqmlOfS__guKUTw; purr-cache=<K0<r<C_<G_<S0; iter_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI2MjBiZjhmZDRlMmNkMzAwMDEyYmEzNTkiLCJjb21wYW55X2lkIjoiNWMwOThiM2QxNjU0YzEwMDAxMmM2OGY5IiwiaWF0IjoxNjQ0OTUxODA1fQ.r1yGml7WDkpk6qZ5fruXsz3Jwfda8SKVdZ42R17HL28; nyt-purr=cfhhcnohhukn; _gcl_aw=GCL.1644951806.Cj0KCQiAu62QBhC7ARIsALXijXTA15LXHdOI5by5sDlDqZ0EeZzSlxaM6f4C-qHkWZJBVbKr5b1HGN8aAqtGEALw_wcB; _gcl_dc=GCL.1644951806.Cj0KCQiAu62QBhC7ARIsALXijXTA15LXHdOI5by5sDlDqZ0EeZzSlxaM6f4C-qHkWZJBVbKr5b1HGN8aAqtGEALw_wcB; _gac_UA-58630905-1=1.1644951806.Cj0KCQiAu62QBhC7ARIsALXijXTA15LXHdOI5by5sDlDqZ0EeZzSlxaM6f4C-qHkWZJBVbKr5b1HGN8aAqtGEALw_wcB; _scid=3ea4486f-ed2c-4d2b-bd3e-ea8ecdc8167c; nyt-b3-traceid=8e098faaccdd47e39aa02af3d0194d30; nyt-m=948E7207F852EE230B45007ADA68A247&t=i.1&pr=l.4.0.0.0.0&iue=i.0&ier=i.0&iub=i.0&e=i.1646125200&vp=i.0&ft=i.0&ira=i.0&rc=i.0&ica=i.0&iga=i.0&n=i.2&cav=i.0&ifv=i.0&igd=i.0&vr=l.4.0.0.0.0&igu=i.1&imv=i.0&iru=i.1&v=i.0&g=i.0&imu=i.1&iir=i.0&s=s.core&er=i.1644951871&fv=i.0&prt=i.0&igf=i.0&ird=i.0&uuid=s.b7db4f94-fc35-4377-b54d-e81750df50cf; nyt-jkidd=uid=0&lastRequest=1644951871712&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%5D&adv=1&a7dv=1&a14dv=1&a21dv=1&lastKnownType=anon; nyt-cmots=eyJmcmVxdWVuY3kiOnsiMjg2NTI1OTkzIjp7ImlubGluZVVuaXQiOnsiZiI6MSwicyI6MSwiZmMiOjE2NDQ5NTE4NzIsInNjIjoxNjQ0OTUxODcyLCJjYSI6MTY0NDk1MTg3Mn19fX0=; datadome=ogFJvcjM_bxiZETfZlETLnZ2FLJHRNyCU-8tyCpHAmEPdeKfDd2ATRGeM1fWzlQ62_3X.SUcT~VYbkIvesW~mm8UyR_hHkfMp5JbvYZh0kE667q8hUCow.UvpeNkkuG; nyt-a=4CkqZyYPWymyNHC4bHinr_; nyt-b3-traceid=10d03a1740b54edeb19ab76428ae6692; nyt-gdpr=1; nyt-purr=cfhspnahhudn; SIDNY="CA8SHxCIlLCQBhoSMS0RHW0Y8JRH-3orKnWjTSzFILzhwVcaQMxalD8I0EriwBJWNxfvB95CJs_JRd8cAY5fmksJMN-lR0sYpvSHrclD-icanjufx2EeXkwhDowICR_l_msqVQ8="'
        }
        queries = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                   'v', 'w', 'x', 'y', 'z']
        for query in queries:
            payload = json.dumps({
                "operationName": "SearchRootQuery",
                "variables": {
                    "first": 10,
                    "sort": "best",
                    "text": query,
                    "filterQuery": "",
                    "sectionFacetFilterQuery": "",
                    "typeFacetFilterQuery": "",
                    "sectionFacetActive": False,
                    "typeFacetActive": False,
                    "cursor": "YXJyYXljb25uZWN0aW9uOjIx"
                },
                "extensions": {
                    "persistedQuery": {
                        "version": 1,
                        "sha256Hash": "36625f535a2f15be8e7bf7165fbc1de88f02a9f7466472360cd0b91480a6c23b"
                    }
                }
            })
            yield scrapy.Request(url.format(query, 0), callback=self.parse)

    def parse(self, response):
        data = {
            'task': 'search',
            'RadioGroup1': 'HCI Name',
            'name': '',
            'clinicType': 'all'
        }
        yield FormRequest.from_response(response, formdata=data, callback=self.parse_page)

    def parse_page(self, response):
        for r in response.xpath('//*[@class="result_container"]'):
            item = {
                'Name': r.xpath('normalize-space(./*[@class="col1"]//a/text())').get(),
                'Phones': ', '.join([t.replace('\xa0', ' ') for t in r.xpath('normalize-space(./*[@class="col1"]//*[@class="tel"])').getall()]),
                'Address': r.xpath('normalize-space(./*[@class="col2"]//*[@class="add"])').get(),
                'Timing': r.xpath('normalize-space(./*[@class="col3"])').get()
            }
            yield item

        current_page = int(response.css('#targetPageNo ::attr(value)').get())
        total_page = int(response.css('#totalPage ::attr(value)').get())
        if current_page < total_page:
            data = {
                'task': 'search',
                'RadioGroup1': 'HCI Name',
                'name': '',
                'clinicType': 'all',
                'targetPageNo': str(current_page+1),
                'totalPage': str(total_page),
            }
            yield FormRequest.from_response(response, formdata=data, callback=self.parse_page)


if __name__ == '__main__':
    sh.run_spider(NYTSpider)