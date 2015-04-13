
# coding: utf-8

# # Exploring Sentiment Analysis with ML

# In[125]:
from __future__ import unicode_literals
import re
import ratings
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfTransformer
pd.set_option('display.max_colwidth', 1200)


happy_regex = re.compile(".*([:;8=xX]-?[\)\]D]).*")
sad_regex = re.compile(".*([:;8=]'?-?[\(\[\|]).*")

plus_regex = re.compile(".*(\+[0-9]+).*")
minus_regex = re.compile(".*((^|[^0-9])\-[0-9]+).*")


def minus_df(df):
    """Extract all the tweets with -"""
    return df[df["content"].str.contains("(^|[^0-9])\-[0-9]+")]


def plus_df(df):
    """Extract all the tweets with +"""
    return df[df["content"].str.contains("\+[0-9]+")]


def happy_df(df):
    return df[df["content"].str.contains("[:;8=xX]-?[\)\]D]")]


def sad_df(df):
    return df[df["content"].str.contains("[:;8=]'?-?[\(\[\|]")]

# ## Choosing data for training
#
# For train and test, we only use the tweets that have been marked with the same rating by AMT.

# In[122]:

def prepare_sentiment_data(tweets):
    neg = [
        (t, 'neg')
        for i, t in ratings.all(tweets, ratings.NEGATIVE).iterrows()]

    pos = [
        (t, 'pos')
        for i, t in ratings.all(tweets, ratings.POSITIVE).iterrows()]

    other = [
        (t, 'other')
        for i, t in ratings.all(tweets, ratings.OTHER).iterrows()]

    train, test = train_test_split(
        pos + neg + other,
        test_size=.2,
        random_state=20)
    return train, test


# #### Make sure data is tokenized

# In[123]:

def featurize(tweet):
    tokens = [token['lemma'] for token in tweet['clean'] if token['lemma'] != '']
    return tokens


# #### Running a pipeline
# The strategy is to use the pipeline design pattern. The input is data and the out put is a trained classifier ready to predict

# In[111]:

def run_pipeline(train, test, clsfr):
    # fit the classifier with training data
    train_x, train_y = zip(*train)
    test_x, test_y = zip(*test)
    clsfr.fit(train_x, train_y)
    # get accuracy on the test
    scr = clsfr.score(test_x, test_y)
    return scr


# ## TF-IDF + Polarity rules classifier (pipeline)

# #### Rule Based features
# This matches +1, -1.. in tweets and adds a new entry polarity(+) or polarity(-) if encountred. Engineering this feature is going to help us to get 100% accuracy on twits that have this pattern.

# In[112]:

class RuleBasedSent(BaseEstimator, TransformerMixin):
    """Extract features from each document for DictVectorizer"""

    def fit(self, x, y=None):
        return self

    def featurize(self, document):
        features = {}
        # Positive/Negative polarity if contains a +/-
        features['polarity(+)'] = not not plus_regex.match(document["content"])
        features['polarity(-)'] = not not minus_regex.match(document["content"])
        return features

    def transform(self, docs):
        return [self.featurize(d) for d in docs]


# ## TF-IDF + (learned) MechTurks 
# 
# Since we already have the scores from AMT, we decided to learn on their labels and use as training set where they all agree

# In[114]:

class MechTurks(BaseEstimator, TransformerMixin):
    """Extract features from each document for DictVectorizer"""

    def fit(self, x, y=None):
        return self

    def rating_to_score(self, rating):
        if (rating == ratings.POSITIVE):
            return 1
        elif (rating == ratings.NEGATIVE):
            return -1
        else:
            return 0

    def featurize(self, document):
        features = {}
        features['rating(1)'] = self.rating_to_score(document["rating.1"])
        features['rating(2)'] = self.rating_to_score(document["rating.2"])
        features['rating(3)'] = self.rating_to_score(document["rating.2"])
        features['rating(4)'] = self.rating_to_score(document["rating.2"])
        return features

    def transform(self, docs):
        return [self.featurize(d) for d in docs]


# In[115]:

# pipeline_amazon = Pipeline([
#     ('features', FeatureUnion([
#         ('ngram_tf_idf', Pipeline([
#             ('counts', CountVectorizer(tokenizer = featurize, lowercase=False)),
#             ('tf_idf', TfidfTransformer())
#         ])),
#         ('mechturks_pipe', Pipeline([
#             ('mecturks', MechTurks()),  # returns a list of dicts
#             ('vect', DictVectorizer()),  # list of dicts -> feature matrix
#         ])),
#         ('rule_based_system', Pipeline([
#             ('match', RuleBasedSent()),  # returns a list of dicts
#             ('vect', DictVectorizer()),  # list of dicts -> feature matrix
#         ]))
#     ])),
#     ('classifier', LinearSVC())
# ])


def build_sent_classifier(tweets):
    vectorizer = FeatureUnion([
        ('counts', TfidfVectorizer(tokenizer = featurize, lowercase=False)),
        ('rule_based_system', Pipeline([
            ('match', RuleBasedSent()),  # returns a list of dicts
            ('vect', DictVectorizer()),  # list of dicts -> feature matrix
        ])),
    ])
    pipeline_tfidf = Pipeline([
        ('features', vectorizer),
        ('classifier', LinearSVC())
    ])

    train, test = prepare_sentiment_data(tweets)
    run_pipeline(train, test, pipeline_tfidf)
    # run_pipeline(train, test, pipeline_amazon)

    return pipeline_tfidf


def df_sentiment(tweets):
    pipeline = build_sent_classifier(tweets)
    tweets["sent_tfidf"] = pd.Series(pipeline.predict([t for i, t in tweets.iterrows()]), index=tweets.index)
    return tweets, pipeline
