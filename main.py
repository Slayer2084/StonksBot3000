# -------------------------------------------------------------------------------------------------------------------- #
# Imports                                                                                                              #
# -------------------------------------------------------------------------------------------------------------------- #

from DataCollection.Archive import Archive
from Listener import NewsListener
from nlp_utils import get_sentiment

import asyncio
import pandas as pd
import numpy as np
import time
import spacy

# -------------------------------------------------------------------------------------------------------------------- #
# Get Archived Data                                                                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

archive = Archive()
dfs = archive.get_df()

# -------------------------------------------------------------------------------------------------------------------- #
# Preprocessing and DataCleaning                                                                                       #
# -------------------------------------------------------------------------------------------------------------------- #

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: add preprocessing function for cleaning dataset
    return df

# -------------------------------------------------------------------------------------------------------------------- #
# Add Features Manually                                                                                                #
# -------------------------------------------------------------------------------------------------------------------- #

# Sentiment

def add_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    df["Sentiment"] = df["Content"].apply(lambda x: get_sentiment(x))
    return df

# Adjectives : Negative, Positive Count

def add_counts_to_df(df: pd.DataFrame, ner: spacy.lang.en.English) -> pd.DataFrame:
    df["verb_count"] = df["Content"].apply(
        lambda text: len([token for token in ner(text) if token.pos_ == 'VERB']))
    df["noun_count"] = df["Content"].apply(
        lambda text: len([token for token in ner(text) if token.pos_ == 'NOUN']))
    df["adj_count"] = df["Content"].apply(
        lambda text: len([token for token in ner(text) if token.pos_ == 'ADJ']))
    df["sent_count"] = df["Content"].apply(lambda text: len([[token.text for token in sent]
                                                             for sent in ner(text).sents]))
    df["word_count"] = df["Content"].apply(
        lambda text: len([token for token in ner(text)]))
    df["char_count"] = df["Content"].apply(lambda text: len(text))
    # TODO: add new counts
    # TODO: finish neg/pos_adj_count
    df["neg_adj_count"] = df["Content"].apply(lambda text:)
    df["pos_adj_count"] = df["Content"].apply(lambda text:)
    return df

# Last 30/60/90... day avg

def add_future_n_day_avgs(df: pd.DataFrame, n_days: tuple = (3, 5, 10, 30, 60, 90)) -> pd.DataFrame:
    # TODO: add future_avgs column to dataframe
    return df

# Politicians trade

def add_last_n_days_pol_trades(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: add recent trades of politicians
    return df

# -------------------------------------------------------------------------------------------------------------------- #
# Add Features Automatically                                                                                           #
# -------------------------------------------------------------------------------------------------------------------- #

# TODO: add automated feature generation

# -------------------------------------------------------------------------------------------------------------------- #
# Filter Important Features                                                                                            #
# -------------------------------------------------------------------------------------------------------------------- #

def filter_important_features(df: pd.DataFrame, n: int) -> pd.DataFrame:
    # TODO: add automated feature filtering
    return df

# -------------------------------------------------------------------------------------------------------------------- #
# Restructure into Classification                                                                                      #
# -------------------------------------------------------------------------------------------------------------------- #

def add_classification(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: map classification to df
    df["label"] = df.map()
    return df

# -------------------------------------------------------------------------------------------------------------------- #
# Train Model + Slight HyperparameterOptimization n_trials = 100                                                       #
# -------------------------------------------------------------------------------------------------------------------- #

def get_optimized_model(df: pd.DataFrame, n_trials: int = 100):
    # TODO: create optimization function
    pass

# -------------------------------------------------------------------------------------------------------------------- #
# Get LiveData                                                                                                         #
# -------------------------------------------------------------------------------------------------------------------- #

listener = NewsListener(loop=asyncio.get_event_loop())

# -------------------------------------------------------------------------------------------------------------------- #
# Retrain Model with new Data
# -------------------------------------------------------------------------------------------------------------------- #

def retrain_model(model, data: pd.DataFrame):
    model.partial_fit(data)
    return model

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

# -------------------------------------------------------------------------------------------------------------------- #
# Start main-loop                                                                                                      #
# -------------------------------------------------------------------------------------------------------------------- #

def on_event(article: dict) -> None:
    df = pd.DataFrame(article)
    # TODO: add on_event functionality
    pass

listener.listen_for_new_event(callback=on_event)
