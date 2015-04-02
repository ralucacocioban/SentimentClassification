import re
import pandas as pd
import nltk
import ratings

# regular expressions to match - and +
plus_regex = re.compile(".*(\+[0-9]+).*")
minus_regex = re.compile(".*([^0-9]\-[0-9]+).*")


def get_tweets(filename):
    """Retrieving the tweets from a file"""
    return pd.read_csv(
        filename,
        sep='\t',
        encoding='utf-8',
        index_col="tweet.id")


def get_transcript(filename):
    return pd.read_csv(filename, encoding='utf-8')


def pre_processing(df):
    df["content"] = df["content"].apply(
        lambda x: re.sub(r'MCCAINs?', 'McCain', x, flags=re.IGNORECASE))
    df["content"] = df["content"].apply(
        lambda x: re.sub(r'Obama|Barack', 'Obama', x, flags=re.IGNORECASE))
    df["tokens"] = df["content"].apply(
        lambda x: nltk.tokenize.word_tokenize(x))
    return df


def df_setminus(d1, d2):
    """This does the set minus operations over the tweet ids"""
    index = d1.index.difference(d2.index)
    return d1.reindex(index)
