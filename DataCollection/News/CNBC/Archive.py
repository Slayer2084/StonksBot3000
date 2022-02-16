import os
import pandas as pd


class ArchivePathError(Exception):
    pass


class FileTypeError(Exception):
    pass


STANDARD_FILE = "Archive.csv"
SEPARATOR = ";"


class CNBCArchive:
    def __init__(self, archive_path=None):
        if archive_path:
            if os.path.isfile(archive_path):
                if os.path.splitext(archive_path)[-1].lower() == ".csv":
                    self.archive_path = archive_path
                else:
                    raise FileTypeError("Passed File is not of type: .csv!")
            else:
                raise ArchivePathError("File", archive_path, " doesn't exist.")

    def get_data(self, rerun=False):
        if rerun:
            data = # Todo: add Scrapy Functionality
        else:
            if self.archive_path:
                data = pd.read_csv(self.archive_path, sep=SEPARATOR)
            else:
                data = pd.read_csv(STANDARD_FILE, sep=SEPARATOR)
        return data

    def scrape(self):
        data = pd.DataFrame()# Todo: add Scrapy Functionality
        if self.archive_path:
            data.to_csv(path_or_buf=self.archive_path, sep=SEPARATOR)
        else:
            data.to_csv(path_or_buf=STANDARD_FILE, sep=SEPARATOR)

