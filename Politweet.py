import re
import pandas as pd
pd.set_option('display.max_colwidth', 1200)
import numpy as np
from IPython.display import display
import nltk
from __future__ import unicode_literals
from spacy.en import English
nlp = English()


# Retrieving the tweets from a file
def get_tweets(filename):
    df = pd.read_csv(filename, sep='\t', encoding='utf-8', index_col="tweet.id")
    return df


# Function to nicely print out the tweets
def list_content(df):
    for i, row in enumerate(zip(df["author.name"].values, df["content"].values)):
        print i, row


def pre_processing(df):
    df["content"] = df["content"].apply(lambda x: re.sub(r'MCCAINs?', 'McCain', x, flags=re.IGNORECASE))
    df["content"] = df["content"].apply(lambda x: re.sub(r'Obama|Barack', 'Obama', x, flags=re.IGNORECASE))
    df["tokens"] = df["content"].apply(lambda x: nltk.tokenize.word_tokenize(x))
    return df

# This static class will help us to filter for Rating.NEGATIVE, etc.
class Rating:
    NEGATIVE = 1
    POSITIVE = 2
    MIXED = 3
    OTHER = 4

# At least one of thar rating
def some_rating(df, rating):
    return df[
        (df["rating.1"]==rating) |
        (df["rating.2"]==rating) |
        (df["rating.3"]==rating) |
        (df["rating.4"]==rating) |
        (df["rating.5"]==rating) |
        (df["rating.6"]==rating) |
        (df["rating.7"]==rating) |
        (df["rating.8"]==rating)
    ]

# Everyone with the same rating
def all_rating(df, rating):
    return df[
        ((df["rating.1"]==rating) | (df["rating.1"] != df["rating.1"])) &
        ((df["rating.2"]==rating) | (df["rating.2"] != df["rating.2"])) &
        ((df["rating.3"]==rating) | (df["rating.3"] != df["rating.3"])) &
        ((df["rating.4"]==rating) | (df["rating.4"] != df["rating.4"])) &
        ((df["rating.5"]==rating) | (df["rating.5"] != df["rating.5"])) &
        ((df["rating.6"]==rating) | (df["rating.6"] != df["rating.6"])) &
        ((df["rating.7"]==rating) | (df["rating.7"] != df["rating.7"])) &
        ((df["rating.8"]==rating) | (df["rating.8"] != df["rating.8"]))
    ]

# regular expressions to match - and +
plus_regex = re.compile(".*(\+[0-9]+).*")
minus_regex = re.compile(".*([^0-9]\-[0-9]+).*")


# Extract all the tweets with -
def minus_df(df):
    return df[df["content"].str.contains("[^0-9]\-[0-9]+")]


# Extract all the tweets with +
def plus_df(df):
    return df[df["content"].str.contains("\+[0-9]+")]


# Extract features of a document
def document_features(document):
    document_words = set(document["tokens"])
    document_words_l = (d.lower() for d in set(document["tokens"]))
    features = {}
    # Positive/Negative polarity if contains a +/-
    features['polarity(+)'] = plus_regex.match(document["content"]) != None
    features['polarity(-)'] = minus_regex.match(document["content"]) != None
    # Point out that contains the word Obama/McCain
    features['contains(obama)'] = "obama" in document_words_l
    features['contains(mccain)'] = "mccain" in document_words_l
    return features


# splits the data in train, dev using the factor
def split_dataset(dataset, factor):
    limit = int(len(dataset)*factor)
    return dataset[:limit], dataset[limit:]


# This does the set minus operations over the tweet ids
def df_setminus(d1, d2):
    index = d1.index.difference(d2.index)
    return d1.reindex(index)
