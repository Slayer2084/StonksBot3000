# -------------------------------------------------------------------------------------------------------------------- #
# Imports                                                                                                              #
# -------------------------------------------------------------------------------------------------------------------- #

import time
from DataCollection.News.Archive import Archive
from DataCollection.News.Stream import Streamer
from DataCollection.News.CNBC.CNBC import CNBCArchiveSpider, CNBCRecentSpider
from DataCollection.News.NewYorkTimes.NYT import NYTArchiveSpider, NYTRecentSpider
from DataCollection.StockMarket.Archive import StockArchive
from DataCollection.StockMarket.Streamer import StockStreamer

# -------------------------------------------------------------------------------------------------------------------- #
# Get Archived Data                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
archiving_start_time = time.time()
#   Get CNBCArchive                                                                                                    #

cnbc_archiver = Archive(CNBCArchiveSpider, "/output/cnbc_archive.csv")
CNBC_Archive = cnbc_archiver.get_data(archiving_start_time)

#   Get NYTArchive                                                                                                     #

nyt_archiver = Archive(NYTArchiveSpider, "/output/nyt_archive.csv")
NYT_Archive = nyt_archiver.get_data(archiving_start_time)

#   Get ArchivedStockData                                                                                              #

stock_archiver = StockArchive("/output/stock_archive.csv")
Stock_Archive = stock_archiver.get_data(archiving_start_time)

# -------------------------------------------------------------------------------------------------------------------- #
# Preprocessing + DataCleaning                                                                                         #
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Generate Features                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Filter Important Features                                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Train Model + Slight HyperparameterOptimization                                                                      #
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Get LiveData                                                                                                         #
# -------------------------------------------------------------------------------------------------------------------- #
update_start_time = time.time()
#   Get new CNBC-Articles                                                                                              #

cnbc_streamer = Streamer(CNBCRecentSpider)
cnbc_newest_date = cnbc_archiver.get_newest_date()
new_cnbc_data = cnbc_streamer.get_new_data(date=cnbc_newest_date, until_time=update_start_time)

#   Get new NYT-Articles                                                                                               #

nyt_streamer = Streamer(NYTRecentSpider)
nyt_newest_date = nyt_archiver.get_newest_date()
new_nyt_data = nyt_streamer.get_new_data(date=nyt_newest_date, until_time=update_start_time)

#   Get new StockData                                                                                                  #

stock_streamer = StockStreamer()
stock_newest_date = stock_archiver.get_newest_date()
new_stock_data = stock_streamer.get_new_data(date=stock_newest_date, until_time=update_start_time)

# If Model isn't up-to-date:
#   Retrain Model with new Data
#   add new Data to Archive

# -------------------------------------------------------------------------------------------------------------------- #
# Model makes Prediction [Positive; Neutral; Negative]                                                                 #
# -------------------------------------------------------------------------------------------------------------------- #

# Depending on predict_proba and portfolio make buy orders
# -------------------------------------------------------------------------------------------------------------------- #
# Give orders to OrderHandler                                                                                          #
# -------------------------------------------------------------------------------------------------------------------- #
