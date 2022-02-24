import os
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals


class StandardFileError(Exception):
    pass


class FileTypeError(Exception):
    pass


class Archive:
    def __init__(self, spider, std_file, sep=";"):
        if os.path.isfile(std_file):
            if os.path.splitext(std_file)[-1].lower() == ".csv":
                self.std_file = std_file
                self.exists = True
            else:
                raise FileTypeError("Passed path is not of type: .csv!")
        else:
            self.exists = False
        self.list = []
        self.sep = sep
        self.spider = spider

    def get_data(self, from_time: float, until_time: float, rerun=False):
        if not self.exists:
            rerun = True
            print("Automatically enabling rerun, because passed file doesn't exist.")
        if rerun:
            data = self._scrape(from_time, until_time)
        else:
            data = pd.read_csv(self.std_file, sep=self.sep)
        return data

    def scrape(self, from_time: float, until_time):
        data = self._scrape(from_time, until_time)
        self._to_csv(data)

    def get_newest_date(self):
        df = pd.read_csv(self.std_file, sep=self.sep)
        return df["Time"].max()  # Todo: Add conversion to timestamp

    def add_to_archive(self, data: list):
        df = pd.read_csv(self.std_file, sep=self.sep)
        df = df.append(data, ignore_index=True)
        self._to_csv(df)

    def _catch_item(self, sender, item, **kwargs):
        self.list.append(item)

    def _scrape(self, from_time, until_time):
        dispatcher.connect(self._catch_item, signal=signals.item_passed)
        crawler = CrawlerProcess()
        crawler.crawl(self.spider, from_time, until_time)
        crawler.start()
        return pd.DataFrame(self.list)

    def _to_csv(self, df):
        df.to_csv(path_or_buf=self.std_file, sep=self.sep)


if __name__ == '__main__':
    from NewYorkTimes.NYT import NYTArchiveSpider

    nyt_archiver = Archive(NYTArchiveSpider, "/output/nyt_archive.csv")
    nyt_archiver.get_data()
