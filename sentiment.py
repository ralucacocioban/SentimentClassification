import classifier
import ratings
import re
import nltk
plus_regex = re.compile(".*(\+[0-9]+).*")
minus_regex = re.compile(".*([^0-9]\-[0-9]+).*")


def minus_df(df):
    """Extract all the tweets with -"""
    return df[df["content"].str.contains("[^0-9]\-[0-9]+")]


def plus_df(df):
    """Extract all the tweets with +"""
    return df[df["content"].str.contains("\+[0-9]+")]


def happy_df(df):
    return df[df["content"].str.contains("[:;8=xX]-?[\)\]D]")]


def sad_df(df):
    return df[df["content"].str.contains("[:;8=]'?-?[\(\[\|]")]


def featurize(document):
    document_words = set(document["tokens"])
    document_words_l = (d.lower() for d in set(document["tokens"]))
    features = {}
    # Positive/Negative polarity if contains a +/-
    features['polarity(+)'] = not plus_regex.match(document["content"])
    features['polarity(-)'] = not minus_regex.match(document["content"])
    # Point out that contains the word Obama/McCain
    features['topic(obama)'] = "obama" in document_words_l
    features['topic(mccain)'] = "mccain" in document_words_l

    return features


def polarity_classifier(tweets, test=None):
    all_negative = ratings.all(tweets, ratings.NEGATIVE)
    all_positive = ratings.all(tweets, ratings.POSITIVE)

    # get what matches minus rule
    minus_rule = minus_df(all_negative)
    plus_rule = plus_df(all_positive)

    pos = [(featurize(d), "pos") for i, d in plus_rule.iterrows()]
    neg = [(featurize(d), "neg") for i, d in minus_rule.iterrows()]

    # split the datasets
    pos_train, pos_test = classifier.split_dataset(pos, 0.8)
    neg_train, neg_test = classifier.split_dataset(neg, 0.8)

    # join the train and the test
    train_set = pos_train + neg_train

    # run the classifier
    nb = nltk.NaiveBayesClassifier.train(train_set)

    if test:
        test_set = pos_test + neg_test
        print(nltk.classify.accuracy(classifier, test_set))
        nb.show_most_informative_features(5)

    return nb
