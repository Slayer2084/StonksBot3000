import requests
import time
from DataCollection.News.Creds import API_KEY
import asyncio


class NewsListener:
    def __init__(self, loop):
        self.loop = loop
        self.callback = None
        self.cnbc_url = "https://api.queryly.com/cnbc/json.aspx?queryly_key=31a35d40a9a64ab3&query=cnbc&endindex=0&batchsize=100&timezoneoffset=-60&sort=date"
        self.nyt_url = "https://api.nytimes.com/svc/news/v3/content/all/world.json?api-key=" + API_KEY + "&limit=1"
        self.article = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) '
                          'Chrome/22.0.1207.1 Safari/537.1',
        }
        self.last_cnbc_id = self._get_latest_cnbc_id()
        self.last_nyt_id = self._get_latest_nyt_id()

    def _request_cnbc_api(self):
        return requests.get(url=self.cnbc_url, headers=self.headers).json()

    @staticmethod
    def _get_latest_cnbc_arcticle(response):
        return response["results"][0]

    def _get_latest_cnbc_id(self):
        response = self._request_cnbc_api()
        return self._get_latest_cnbc_arcticle(response=response)["@id"]

    @staticmethod
    def _parse_cnbc(url):
        print(url)
        return {}

    async def _cnbc_new_event(self):
        while 1:
            cnbc_api_latest_article = self._get_latest_cnbc_arcticle(self._request_cnbc_api())
            cnbc_latest_id = cnbc_api_latest_article["@id"]
            if cnbc_latest_id > self.last_cnbc_id:
                self.last_cnbc_id = cnbc_latest_id
                await self.callback(self._parse_cnbc(cnbc_api_latest_article["cn:liveURL"]))
            await asyncio.sleep(1)

    def _request_nyt_api(self):
        return requests.get(url=self.nyt_url, headers=self.headers).json()

    @staticmethod
    def _get_latest_nyt_arcticle(response):
        return response["results"][0]

    def _get_latest_nyt_id(self):
        response = self._request_nyt_api()
        return self._get_latest_nyt_arcticle(response=response)["slug_name"]

    @staticmethod
    def _parse_nyt(url):
        print(url)
        return {}

    async def _nyt_new_event(self):
        while 1:
            try:
                nyt_api_latest_article = self._get_latest_nyt_arcticle(self._request_nyt_api())
                nyt_latest_id = nyt_api_latest_article["slug_name"]
                if nyt_latest_id != self.last_nyt_id:
                    self.last_nyt_id = nyt_latest_id
                    await self.callback(self._parse_nyt(nyt_api_latest_article["web_url"]))
            except KeyError as e:
                print(e)
            await asyncio.sleep(6)

    def listen_for_new_event(self, callback):
        self.callback = callback
        tasks = asyncio.gather(self._cnbc_new_event(), self._nyt_new_event())
        self.loop.run_until_complete(tasks)


if __name__ == '__main__':

    async def callback(info):
        print(info)

    listener = NewsListener(asyncio.get_event_loop())
    listener.listen_for_new_event(callback)
