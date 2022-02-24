# -------------------------------------------------------------------------------------------------------------------- #
# Imports                                                                                                              #
# -------------------------------------------------------------------------------------------------------------------- #

import numpy as np
import time
from GetArchivedData import get_archived_data
from DataCollection.News.Archive import Archive
from DataCollection.News.Stream import Streamer
from DataCollection.News.CNBC.CNBC import CNBCSpider
from DataCollection.News.NewYorkTimes.NYT import NYTArchiveSpider, NYTRecentSpider
from DataCollection.StockMarket.Archive import StockArchive
from DataCollection.StockMarket.Streamer import StockStreamer
from CombineDatasets import combine_subframes

# -------------------------------------------------------------------------------------------------------------------- #
# Get Archived Data Sync Step 1                                                                                        #
# -------------------------------------------------------------------------------------------------------------------- #

archive = get_archived_data()

# -------------------------------------------------------------------------------------------------------------------- #
# Preprocessing and DataCleaning                                                                                       #
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

cnbc_streamer = Streamer(CNBCSpider)
cnbc_newest_date = CNBC_Archive["Time"].max()
new_cnbc_data = cnbc_streamer.get_new_data(from_time=cnbc_newest_date, until_time=update_start_time)

#   Get new NYT-Articles                                                                                               #

nyt_streamer = Streamer(NYTRecentSpider)
nyt_newest_date = NYT_Archive["Time"].max()
new_nyt_data = nyt_streamer.get_new_data(from_time=nyt_newest_date, until_time=update_start_time)

#   Get new StockData                                                                                                  #

stock_streamer = StockStreamer()
stock_newest_date = Stock_Archive["Time"].max()
new_stock_data = stock_streamer.get_new_data(from_time=stock_newest_date, until_time=update_start_time)

# -------------------------------------------------------------------------------------------------------------------- #
# Retrain Model with new Data
# -------------------------------------------------------------------------------------------------------------------- #

model.partial_fit()

# -------------------------------------------------------------------------------------------------------------------- #
# Add new Data to Archive
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Model makes Prediction [Positive; Neutral; Negative]                                                                 #
# -------------------------------------------------------------------------------------------------------------------- #

# Depending on predict_proba and portfolio make buy orders
# -------------------------------------------------------------------------------------------------------------------- #
# Give orders to OrderHandler                                                                                          #
# -------------------------------------------------------------------------------------------------------------------- #
