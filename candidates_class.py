
# coding: utf-8

# # Exploring Candidate Classification with ML

# In[23]:

from __future__ import unicode_literals
import re
import ratings
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfTransformer
from Politweet import df_setminus
pd.set_option('display.max_colwidth', 1200)


# ## Choosing data for training
# 
# For train and test, we only use the tweets that have been marked with the same rating by AMT.

# In[24]:

def prepare_sentiment_data(tweets):
    obama = tweets[tweets["content"].str.contains('obama', flags=re.IGNORECASE)]
    mccain = tweets[tweets["content"].str.contains('mccain', flags=re.IGNORECASE)]
    oba_and_mccain = tweets.reindex(obama.index & mccain.index)
    oba_or_mccain = tweets.reindex(obama.index | mccain.index)
    none = tweets[~(tweets["content"].str.contains('obama|mccain', flags=re.IGNORECASE))]
    other = ratings.all(tweets, ratings.OTHER)

    only_mccain = df_setminus(mccain, oba_and_mccain)
    only_obama = df_setminus(obama, oba_and_mccain)
    other_none = df_setminus(df_setminus(other, oba_or_mccain), oba_and_mccain)

    oba = [
        (t, 'oba')
        for i, t in only_obama.iterrows()]

    mcc = [
        (t, 'mcc')
        for i, t in only_mccain.iterrows()]

    both = [
        (t, 'both')
        for i, t in oba_and_mccain.iterrows()]

    other = [
        (t, 'none')
        for i, t in other_none.iterrows()]

    train, test = train_test_split(
        oba + mcc + both + other,
        test_size=.2,
        random_state=20)

    return train, test


# #### Make sure data is tokenized

# In[16]:

def featurize(tweet):
    tokens = [token['lemma'] for token in tweet['clean'] if token['lemma'] != '']
    return tokens


# #### Running a pipeline
# The strategy is to use the pipeline design pattern. The input is data and the out put is a trained classifier ready to predict

# In[17]:

def run_pipeline(train, test, clsfr):
    # fit the classifier with training data
    train_x, train_y = zip(*train)
    test_x, test_y = zip(*test)
    clsfr.fit(train_x, train_y)
    # get accuracy on the test
    scr = clsfr.score(test_x, test_y)
    return scr


# ## TF-IDF + Candidate rules classifier (pipeline)

# #### Rule Based features
# This matches +1, -1.. in tweets and adds a new entry polarity(+) or polarity(-) if encountred. Engineering this feature is going to help us to get 100% accuracy on twits that have this pattern.

# In[18]:

obama_regex = re.compile(".*(obama|barack).*")
mccain_regex = re.compile(".*(mccain|mcpain|).*")

class RuleBasedCandidate(BaseEstimator, TransformerMixin):
    """Extract features from each document for DictVectorizer"""

    def fit(self, x, y=None):
        return self

    def featurize(self, document):
        document_words = set(document["tokens"])

        features = {}
        features['candidate(obama)'] = not not obama_regex.match(document["content"])
        features['candidate(mccain)'] = not not mccain_regex.match(document["content"])

        return features

    def transform(self, docs):
        return [self.featurize(d) for d in docs]


# In[19]:

pipeline_candidates = Pipeline([
    ('features', FeatureUnion([
        ('ngram_tf_id', Pipeline([
            ('count', CountVectorizer(tokenizer = featurize, lowercase=False)),
            ('tf_id', TfidfTransformer())
        ])),
        ('rule_based_syste', Pipeline([
                ('match', RuleBasedCandidate()),  # returns a list of dicts
                ('vect', DictVectorizer()),  # list of dicts -> feature matrix
            ]))
    ])),
    ('classifier', LinearSVC())
])


# ## Annotate tweets with sentiment

# In[22]:

def df_candidates(tweets):
    train, test = prepare_sentiment_data(tweets)
    run_pipeline(train, test, pipeline_candidates)
    tweets["candidate"] = pd.Series(pipeline_candidates.predict([t for i,t in tweets.iterrows()]), index=tweets.index)
    return tweets
