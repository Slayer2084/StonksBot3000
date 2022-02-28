import os
import pandas as pd
import time
from CombineDatasets import combine_subframes
import asyncio
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from DataCollection.News.CNBC.CNBC import CNBCSpider
from scrapy import signals
from DataCollection.News.NewYorkTimes.NYT import NYTArchiveSpider
from DataCollection.StockMarket.alpaca_creds import API_KEY, API_SECRET
from alpaca_trade_api.rest_async import AsyncRest
from alpaca_trade_api.rest import TimeFrame, URL, TimeFrameUnit
import alpaca_trade_api as tradeapi


class Archive:
    def __init__(self):
        self.sep = ";"
        self.path = "./archive.csv"
        self.news_path = "./news.csv"
        self.stock_path = "./stock.csv"
        self.index_col = "index"
        self.min_time = 946684800

    def update_archive(self):
        min_time = self.get_max_date()
        max_time = time.time()
        news, stock = self._scrape_data(min_time, max_time)
        new_df = combine_subframes(news, stock)
        df = pd.read_csv(filepath_or_buffer=self.path, sep=self.sep, index_col=self.index_col)
        return pd.concat(df, new_df)

    def get_subframes(self):
        if not os.path.exists(self.news_path) and not os.path.exists(self.stock_path):
            news, stocks = self._scrape_data(self.min_time, time.time())
            self._create_csv(df=news, path=self.news_path)
            self._create_csv(df=stocks, path=self.stock_path)
        return pd.read_csv(filepath_or_buffer=self.news_path, sep=self.sep, index_col=self.index_col), pd.read_csv(filepath_or_buffer=self.stock_path, sep=self.sep, index_col=self.index_col)

    def get_df(self):
        if not os.path.exists(self.path):
            news, stocks = self._scrape_data(self.min_time, time.time())
            df = combine_subframes(news, stocks)
            self._create_csv(df=df, path=self.path)
        return pd.read_csv(filepath_or_buffer=self.path, sep=self.sep, index_col=self.index_col)

    def get_max_date(self):
        return self.get_df()["Time"].max(axis=1)

    def get_min_date(self):
        return self.get_df()["Time"].min(axis=1)

    def _create_csv(self, df: pd.Dataframe, path: str):
        df.to_csv(path_or_buf=path, sep=self.sep, index_label=self.index_col)

    def _scrape_data(self, min_time, max_time):
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
