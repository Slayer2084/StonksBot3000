# -------------------------------------------------------------------------------------------------------------------- #
# Imports                                                                                                              #
# -------------------------------------------------------------------------------------------------------------------- #

import numpy as np
import time
from DataCollection.Archive import Archive

# -------------------------------------------------------------------------------------------------------------------- #
# Get Archived Data                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

archive = Archive()
dfs = archive.get_df()

# -------------------------------------------------------------------------------------------------------------------- #
# Preprocessing and DataCleaning                                                                                       #
# -------------------------------------------------------------------------------------------------------------------- #

for df in dfs:

# -------------------------------------------------------------------------------------------------------------------- #
# Add Features Manually                                                                                                #
# -------------------------------------------------------------------------------------------------------------------- #

# Sentiment
# Adjectives : Negative, Positive Count
# Stocknames



# -------------------------------------------------------------------------------------------------------------------- #
# Add Features Automatically                                                                                           #
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Filter Important Features                                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Train Model + Slight HyperparameterOptimization n_trials = 100                                                       #
# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
# Get LiveData                                                                                                         #
# -------------------------------------------------------------------------------------------------------------------- #

archive.update()

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
