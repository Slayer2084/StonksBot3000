# -------------------------------------------------------------------------------------------------------------------- #
# Imports                                                                                                              #
# -------------------------------------------------------------------------------------------------------------------- #

from DataCollection.News.Archive import Archive
from DataCollection.News.Stream import Streamer
from DataCollection.News.NewYorkTimes.NYT import NYTArchiveSpider, NYTRecentSpider
from DataCollection.News.CNBC.CNBC import CNBCArchiveSpider, CNBCRecentSpider

# -------------------------------------------------------------------------------------------------------------------- #
# Get Archived Data                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
#   Get CNBCArchive                                                                                                    #

cnbc_archiver = Archive(CNBCArchiveSpider, "/output/cnbc_archive.csv")
CNBC_Archive = cnbc_archiver.get_data()

#   Get NYTArchive                                                                                                     #

nyt_archiver = Archive(NYTArchiveSpider, "/output/nyt_archive.csv")
NYT_Archive = nyt_archiver.get_data()

#   Get ArchivedStockData                                                                                              #

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
#   Get new CNBC-Articles                                                                                              #

cnbc_streamer = Streamer(CNBCRecentSpider)
cnbc_newest_date = cnbc_archiver.get_newest_date()
new_cnbc_data = cnbc_streamer.get_new_data(date=cnbc_newest_date)

#   Get new NYT-Articles                                                                                               #

nyt_streamer = Streamer(NYTRecentSpider)
nyt_newest_date = nyt_archiver.get_newest_date()
new_nyt_data = nyt_streamer.get_new_data(date=nyt_newest_date)

#   Get new StockData                                                                                                  #
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
