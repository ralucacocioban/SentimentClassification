import os
import sys
import string
from Politweet import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from gensim.models import Word2Vec

stemmer = SnowballStemmer("english")

def remove_stopwords(tokens):
    # Remove stopwords, punctuations and numbers
    temp = [token for token in tokens if token not in stopwords.words('english') and token not in string.punctuation and not token.isdigit()]
    regex = re.compile("//www.\S+.\S+/")
    no_links = [token for token in temp if token != "http" or token not in regex.findall(token)]
    return no_links


if __name__ == "__main__":
    filename = "debate08_sentiment_tweets.tsv"
    if not os.path.isfile(filename):
        sys.exit("Missing file.")

    print """Extracting tweets from file '{}'""".format(filename)
    print "Display tweets"
    tweets = pre_processing(get_tweets(filename))
    tweets["clean"] = tweets["tokens"].apply(remove_stopwords)
    print tweets["clean"]
