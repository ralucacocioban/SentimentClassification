from __future__ import unicode_literals
import classifiers
import re
import nltk
from politweet import get_tweets, get_transcript, pre_processing
import ratings


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


def featurize(document):
    document_words = set(document["tokens"])
    document_words_l = set(d.lower() for d in set(document["tokens"]))
    features = {}
    # Positive/Negative polarity if contains a +/-
    features['polarity(+)'] = not plus_regex.match(document["content"])
    features['polarity(-)'] = not minus_regex.match(document["content"])
    # Point out that contains the word Obama/McCain
    features['topic(obama)'] = "obama" in document_words_l
    features['topic(mccain)'] = "mccain" in document_words_l
    return features


def polarity_featurize(document):
    document_words = set(document["tokens"])
    document_words_l = (d.lower() for d in set(document["tokens"]))
    features = {}
    # Positive/Negative polarity if contains a +/-
    features['polarity(+)'] = not plus_regex.match(document["content"])
    features['polarity(-)'] = not minus_regex.match(document["content"])
    return features

def featurize(tweet):
    # tokenize into words
    tokens = [word for sent in sent_tokenize(tweet) for word in word_tokenize(sent)]

    # remove stopwords
    stop = stopwords.words('english')
    tokens = [token for token in tokens if token not in stop]

    # remove words less than three letters
    tokens = [word for word in tokens if len(word) >= 3]

    # lower capitalization
    tokens = [word.lower() for word in tokens]

    # lemmatize
    lmtzr = WordNetLemmatizer()
    tokens = [lmtzr.lemmatize(word) for word in tokens]

    return tokens


def polarity_filter(df):
    df[df["content"].str.contains("[^0-9][\-[0-9]+")]


def polarity_train(df, test=None):

    all_negative = ratings.all(df, ratings.NEGATIVE)
    all_positive = ratings.all(df, ratings.POSITIVE)

    # get what matches minus rule
    minus_rule = minus_df(all_negative)
    plus_rule = plus_df(all_positive)

    pos = [(polarity_featurize(d), "pos") for i, d in plus_rule.iterrows()]
    neg = [(polarity_featurize(d), "neg") for i, d in minus_rule.iterrows()]

    # split the datasets
    pos_train, pos_test = classifiers.split_dataset(pos, 0.8)
    neg_train, neg_test = classifiers.split_dataset(neg, 0.8)

    # join the train and the test
    train_set = pos_train + neg_train

    # run the classifier
    nb = nltk.NaiveBayesClassifier.train(train_set)

    if test:
        test_set = pos_test + neg_test
        print(nltk.classify.accuracy(nb, test_set))
        nb.show_most_informative_features(5)

    return nb


def classify(df, classifier, featurize_f=polarity_featurize):
    return [(i, classifier.classify(featurize_f(d))) for i, d in df.iterrows()]


def prob_classify(df, classifier, featurize_f=polarity_featurize):
    return [(i, classifier.prob_classify(featurize_f(d))) for i, d in df.iterrows()]

if __name__ == "__main__":
    data = get_tweets("./datasets/tweets.tsv")
    transcript = get_transcript("./datasets/transcript.csv")
    tweets = pre_processing(data)

    polarity = polarity_train(tweets)

    todo = set(tweets.index)
    # happy tweets
    polarity_minus = set(i for i,_ in classify(minus_df(tweets), polarity))
    polarity_plus = set(i for i,_ in classify(plus_df(tweets), polarity))
    others = set(ratings.all(tweets, ratings.OTHER).index)

    print len(polarity_minus | polarity_plus), "- polarity"
    todo -= (polarity_minus | polarity_plus)
    print len(others), "- marked as OTHERS"
    todo -= others

    print len(todo), "- untagged"

    ratings.all(tweets, ratings.OTHER)