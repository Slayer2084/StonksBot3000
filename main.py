# -------------------------------------------------------------------------------------------------------------------- #
# Imports                                                                                                              #
# -------------------------------------------------------------------------------------------------------------------- #

from DataCollection.News.CNBC.Archive import CNBCArchive
from DataCollection.News.NewYorkTimes.Archive import NYTArchive

# -------------------------------------------------------------------------------------------------------------------- #
# Get Archived Data                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
#   Get CNBCArchive                                                                                                    #

cnbc_archiver = CNBCArchive()
CNBC_Archive = cnbc_archiver.get_data(rerun=True)

#   Get NYTArchive                                                                                                     #

nyt_archiver = NYTArchive()
NYT_Archive = nyt_archiver.get_data(rerun=True)

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
#   Get new CNBC-Articles
#   Get new NYT-Articles
#   Get new StockData
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