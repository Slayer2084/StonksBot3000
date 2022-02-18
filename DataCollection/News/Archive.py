import os
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals


class StandardFileError(Exception):
    pass


class ArchivePathError(Exception):
    pass


class FileTypeError(Exception):
    pass


class Archive:
    def __init__(self, spider, std_file, archive_path=None, sep=";"):
        self.archive_path = None
        if archive_path is not None:
            if os.path.isfile(archive_path):
                if os.path.splitext(archive_path)[-1].lower() == ".csv":
                    self.archive_path = archive_path
                else:
                    raise FileTypeError("Passed File is not of type: .csv!")
            else:
                raise ArchivePathError("File " + archive_path + " doesn't exist.")
        self.list = []
        self.sep = sep
        self.spider = spider
        self.std_file = std_file

    def get_data(self, rerun=False):
        if rerun:
            data = self._scrape()
        else:
            if self.archive_path is not None:
                data = pd.read_csv(self.archive_path, sep=self.sep)
            else:
                if not os.path.isfile(self.std_file):
                    raise StandardFileError("Rerun needed")
                data = pd.read_csv(self.std_file, sep=self.sep)
        return data

    def scrape(self):
        data = self._scrape()
        self._to_csv(data)

    def get_newest_date(self):
        if self._check_archive():
            df = pd.read_csv(self.archive_path, sep=self.sep)
        else:
            df = pd.read_csv(self.std_file, sep=self.sep)
        df.sort_values("Time", axis=1, descending=False, inplace=True)
        return df["Time"].tolist()[0]

    def add_to_archive(self, data: list):
        if self._check_archive():
            df = pd.read_csv(self.archive_path, sep=self.sep)
        else:
            df = pd.read_csv(self.std_file, sep=self.sep)
        df = df.append(data, ignore_index=True)
        self._to_csv(df)

    def _catch_item(self, sender, item, **kwargs):
        self.list.append(item)

    def _scrape(self):
        dispatcher.connect(self._catch_item, signal=signals.item_passed)
        crawler = CrawlerProcess()
        crawler.crawl(self.spider)
        crawler.start()
        return pd.DataFrame(self.list)

    def _check_archive(self):
        if self.archive_path is not None:
            return True
        else:
            return False

    def _to_csv(self, df):
        if self._check_archive():
            df.to_csv(path_or_buf=self.archive_path, sep=self.sep)
        else:
            df.to_csv(path_or_buf=self.std_file, sep=self.sep)


if __name__ == '__main__':
    from NewYorkTimes.NYT import NYTArchiveSpider
    nyt_archiver = Archive(NYTArchiveSpider, "/output/nyt_archive.csv")
    nyt_archiver.get_data(rerun=True)
