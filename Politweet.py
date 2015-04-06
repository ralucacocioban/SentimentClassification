from __future__ import unicode_literals
import re
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
import string

lmtzr = nltk.WordNetLemmatizer()
stop = nltk.corpus.stopwords.words('english')
stop += ["@", "#"]
punct = [',', '.', ':', ';', '``', '\'\'', 'POS']
skip = [
    '\'s', '\'ve', '\'d', '\'ll', '\'m', '\'re', '(', ')', '>', '<', 'http',
    'almost', '#tweetdebate', '#debate', '#current', '#debate08']


def get_tweets(filename, pickle="tweets.pickle"):
    """Retrieving the tweets from a file"""
    try:
        return pd.read_pickle("./datasets/tweets.pickle")
    except:
        df = pd.read_csv(
            filename,
            sep='\t',
            encoding='utf-8',
            index_col="tweet.id")
        return pre_processing(df)


def get_transcript(filename):
    return pd.read_csv(filename, encoding='utf-8')


def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None


def lemmatize(word, pos):
    try:
        return lmtzr.lemmatize(word, pos=penn_to_wn(pos))
    except:
        return lmtzr.lemmatize(word)


def tokenizer(tweet):
    # tokenize into sentences
    sentences = [sent for sent in nltk.sent_tokenize(tweet)]
    tokens = []
    # tokenize into words
    for sent in sentences:
        tokens += nltk.pos_tag(nltk.word_tokenize(sent.lower()))
    # lemmatize
    tokens = [
        (
            "".join(l for l in t if l not in string.punctuation),
            "".join(l for l in p if l not in string.punctuation)
        ) for t, p in tokens]

    tokens = [dict(token=t, pos=p, lemma=lemmatize(t, p)) for t, p in tokens]

    # do not treat # or @ as tokens
    length = len(tokens)
    for i, token in enumerate(tokens):
        if i + 1 < length:
            if token["lemma"] == "@":
                tokens[i + 1]["lemma"] = "@" + tokens[i + 1]["lemma"]
                tokens[i + 1]["token"] = "@" + tokens[i + 1]["token"]
            elif token["lemma"] == "#":
                tokens[i + 1]["lemma"] = "#" + tokens[i + 1]["lemma"]
                tokens[i + 1]["token"] = "#" + tokens[i + 1]["token"]

    # removing stopwords
    tokens = [token for token in tokens if token["lemma"] not in stop + skip]

    return tokens

tokenizer("keep it rolling")


def pre_processing(df):
    df["content"] = df["content"].apply(
        lambda x: re.sub(r'MCCAINs?', 'McCain', x, flags=re.IGNORECASE))
    df["content"] = df["content"].apply(
        lambda x: re.sub(r'Obama|Barack', 'Obama', x, flags=re.IGNORECASE))
    df["clean"] = df["content"].apply(tokenizer)
    df["tokens"] = df["clean"].apply(
        lambda tokens: [
            token["lemma"]
            for token in tokens
            if token["pos"] not in punct])
    return df


def df_setminus(d1, d2):
    """This does the set minus operations over the tweet ids"""
    index = d1.index.difference(d2.index)
    return d1.reindex(index)
