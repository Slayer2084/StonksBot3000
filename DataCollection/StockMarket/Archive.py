import asyncio
import alpaca_trade_api as trade_api
from alpaca_trade_api.rest import TimeFrameUnit, TimeFrame, URL
import pandas as pd
import sys
from enum import Enum
from alpaca_creds import CLIENT_ID, CLIENT_SECRET, API_KEY, API_SECRET
from alpaca_trade_api.rest_async import gather_with_concurrency, AsyncRest


base_url = "https://paper-api.alpaca.markets"


class StockArchive:
    def __init__(self, output_path):
        self.api = trade_api.REST(key_id=API_KEY, secret_key=API_SECRET, base_url=URL(base_url))
        self.async_rest = AsyncRest(key_id=API_KEY, secret_key=API_SECRET, data_url=URL(base_url))
        self.output_path = output_path

    async def _get_asset_list(self):
        asset_list = self.api.list_assets(status="active")
        ref_asset_list = []
        for asset in asset_list:
            if asset.easy_to_borrow:
                ref_asset_list.append(asset)
        return ref_asset_list[:200]

    async def _get_data(self, from_time, until_time, symbols, timeframe):
        if symbols is None:
            symbols = await self._get_asset_list()
        results = []
        stepsize = 1000
        for i in range(0, len(symbols), stepsize):
            tasks = []
            for symbol in symbols[i:i+stepsize]:
                args = [symbol, from_time, until_time, timeframe.value]
                tasks.append(self.async_rest.get_bars_async(*args))
            results.extend(await asyncio.gather(*tasks, return_exceptions=True))
        return results

    def get_data(self, from_time, until_time, symbols=None, timeframe=TimeFrame(1, TimeFrameUnit.Minute)):
        return asyncio.run(self._get_data(from_time, until_time, symbols, timeframe))


if __name__ == "__main__":
    Archive = StockArchive("output/bla.csv")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(Archive.get_data(1645710000, 1645711668)[0])
