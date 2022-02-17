import os
import pandas as pd
from scrapy.crawler import CrawlerProcess
from CNBC import CNBCSpider
from scrapy.signalmanager import dispatcher
from scrapy import signals


class StandardFileError(Exception):
    pass


class ArchivePathError(Exception):
    pass


class FileTypeError(Exception):
    pass


STANDARD_FILE = "Archive.csv"


class CNBCArchive:
    def __init__(self, archive_path=None, sep=";"):
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
        self.archive_path = None

    def get_data(self, rerun=False):
        if rerun:
            data = self._scrape()
        else:
            if self.archive_path is not None:
                data = pd.read_csv(self.archive_path, sep=self.sep)
            else:
                if not os.path.isfile(STANDARD_FILE):
                    raise StandardFileError("Rerun needed")
                data = pd.read_csv(STANDARD_FILE, sep=self.sep)
        return data

    def scrape(self):
        data = self._scrape()
        if self.archive_path is not None:
            data.to_csv(path_or_buf=self.archive_path, sep=self.sep)
        else:
            data.to_csv(path_or_buf=STANDARD_FILE, sep=self.sep)

    def _scrape(self):
        dispatcher.connect(self.catch_item, signal=signals.item_passed)
        crawler = CrawlerProcess()
        crawler.crawl(CNBCSpider)
        crawler.start()
        return pd.DataFrame(self.list)

    def catch_item(self, sender, item, **kwargs):
        self.list.append(item)


if __name__ == '__main__':
    cnbc_archiver = CNBCArchive()
    cnbc_archiver.get_data(rerun=True)
