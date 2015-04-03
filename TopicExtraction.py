import os
import sys
import string
from Politweet import *
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from argparse import ArgumentParser

stemmer = SnowballStemmer("english")

def remove_stopwords(tokens):
    # Remove stopwords, punctuations and numbers
    temp = [token for token in tokens if token not in stopwords.words('english') and token not in string.punctuation and not token.isdigit()]
    regex = re.compile("//www.\S+.\S+/")
    no_links = [token for token in temp if token != "http" or token not in regex.findall(token)]
    return no_links

# Get the file from this link: https://code.google.com/p/word2vec/
def load_word2vec_model(c_bin):
    if not os.path.isfile(c_bin):
        sys.exit("""File '{0}' does not exist.""".format(c_bin))

    model = Word2Vec.load_word2vec_format(c_bin, binary=True)

    return model

def input_check(tweets, word2vec):
    if not os.path.isfile(tweets):
        print """File path for tweets '{0}' does not exist.""".format(tweets)
        return False

    if not os.path.isfile(word2vec):
        print """File path for word2vec model '{0}' does not exist.""".format(word2vec)
        return False

    return True


def main():
    """
    Instruction how to use this tool.
    python TopicExtraction.py --tweets [tweet dataset path] --word2vec [word2vec model path]
    """
    
    parser = ArgumentParser(description='Extract topics from tweeter dataset.')
    parser.add_argument('--tweets', '-t', help='File path of the tweets dataset.', required=True)
    parser.add_argument('--word2vec', '-w2v', help='File path of the word2vec model.', required=True)
    args = parser.parse_args()

    print "Tweet file location:", args.tweets
    print "Word2Vec file location:", args.word2vec

    if not input_check(args.tweets, args.word2vec):
        sys.exit(-1)

    print "Preprocessing tweets..."
    tweets = pre_processing(get_tweets(args.tweets))
    print "Done preprocessing tweets."

    print "Removing stopwords, punctuations etc."
    tweets["clean"] = tweets["tokens"].apply(remove_stopwords)
    print "Done removing stopwords, punctuations etc."

    print "Loading word2vec model..."
    word2vec_model = load_word2vec_model(args.word2vec)
    print "Done loading word2vec model."



if __name__ == "__main__":
    main()
