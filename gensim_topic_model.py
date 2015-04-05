import os, sys, codecs
from gensim.models.ldamulticore import LdaMulticore
from gensim.models.ldamodel import LdaModel
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
from Politweet import get_tweets, pre_processing
from TopicExtraction import remove_stopwords


# Write tweets into a file for gensim to process
def tweets_to_file(tweets, output):
    with codecs.open(output, 'w', 'utf-8') as f:
        corpus = []
        for tweet in tweets:
            doc = " ".join(tweet)
            corpus.append(doc)
        f.write("\n".join(corpus))
    return True


# Multicore implementation of Lda Model
def train_model(fname, output, workers=1):
    if not os.path.isfile(fname):
        sys.exit("""File '{0}' does not exist.""".format(fname))

    tweets = pre_processing(get_tweets(fname))
    tweets_file = output + "/" + fname + ".txt"

    # Remove Stopwords
    tweets["clean"] = tweets["tokens"].apply(remove_stopwords)

    # Write tweets content to file
    if not tweets_to_file(tweets["clean"], tweets_file):
        sys.exit("Failed to write tweets to text file.")

    print "Processing corpus..."
    background_corpus = TextCorpus(tweets_file)
    background_corpus.dictionary.save(output+"/background_corpus.dict")
    MmCorpus.serialize(output+"/background_corpus.mm", background_corpus)

    bow_corpus = MmCorpus(output+"/background_corpus.mm")
    # Load a dictionary
    dictionary = Dictionary.load(output+"/background_corpus.dict")
    print "Training Lda Model..."
    lda = LdaMulticore(corpus=background_corpus, id2word=dictionary, workers=workers)
    lda.save(output + "/tweets.model")
    return True


def load_ldamodel(fname):
    if not os.path.isfile(fname):
        sys.exit("""Lda model not found at '{0}'""".format(fname))

    lda = LdaModel.load(fname)
    return lda

# Tutorial how to use gensim can be found here:
# http://www.williamjohnbert.com/2012/05/relatively-quick-and-easy-gensim-example-code/
if __name__ == "__main__":
    fname = "debate08_sentiment_tweets.tsv"
    output = "output"

    if not os.path.isfile(fname):
        sys.exit("""File '{0}' does not exist.""".format(fname))

    if not os.path.isdir(output):
        os.makedirs(output)
        print """Create folder '{0}'.""".format(output)

    if not train_model(fname, output):
        sys.exit("Failed to train Lda Model.")
    else:
        print "Successfully trained Lda Model."

    # load Lda model
    lda = load_ldamodel(output+"/tweets.model")
    if lda is None:
        sys.exist("Failed to load Lda model.")

    # Show top 10 topics
    for n, topics in enumerate(lda.show_topics()):
        print "Topic", n, ":", topics
