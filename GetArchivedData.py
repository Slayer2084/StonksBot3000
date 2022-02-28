import asyncio
import pandas as pd
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from DataCollection.News.CNBC.CNBC import CNBCSpider
from scrapy import signals
from DataCollection.News.NewYorkTimes.NYT import NYTArchiveSpider
from DataCollection.StockMarket.alpaca_creds import API_KEY, API_SECRET
from alpaca_trade_api.rest_async import AsyncRest
from alpaca_trade_api.rest import TimeFrame, URL, TimeFrameUnit
import alpaca_trade_api as tradeapi


def get_archived_data(min_time, max_time):
    news_list = []
    stocks_list = []
    base_url = "https://paper-api.alpaca.markets"

    def catch_item(sender, item, **kwargs):
        news_list.append(item)

    async def get_news():
        dispatcher.connect(catch_item, signal=signals.item_passed)
        process = CrawlerProcess()
        process.crawl(CNBCSpider, from_time=min_time, until_time=max_time)
        process.crawl(NYTArchiveSpider, from_time=min_time, until_time=max_time)
        await process.start()

    async def get_stocks():
        rest = AsyncRest(key_id=API_KEY,
                         secret_key=API_SECRET,
                         data_url=URL(base_url))
        api = tradeapi.REST(key_id=API_KEY,
                            secret_key=API_SECRET,
                            base_url=URL(base_url))
        symbols = api.list_assets(status="active")
        ref_symbols = []
        for symbol in symbols:
            if symbol.easy_to_borrow:
                ref_symbols.append(symbol)
        stepsize = 1000
        for i in range(0, len(symbols), stepsize):
            tasks = []
            for symbol in symbols[i:i + stepsize]:
                args = [symbol, min_time, max_time, TimeFrame(1, TimeFrameUnit.Minute).value]
                tasks.append(rest.get_bars_async(*args))
            stocks_list.extend(await asyncio.gather(*tasks, return_exceptions=True))

    tasks = asyncio.gather(get_news(), get_stocks())
    asyncio.get_event_loop().run_until_complete(tasks)
    news_df = pd.DataFrame(news_list)
    stocks_df = pd.DataFrame(stocks_list)
    return news_df, stocks_df


if __name__ == "__main__":
    print(get_archived_data())
