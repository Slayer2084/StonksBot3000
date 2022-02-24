import pandas as pd


def combine_subframes(news, stock):
    combined = pd.concat([news, stock], ignore_index=True)
    return combined
