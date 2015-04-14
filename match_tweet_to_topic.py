import gensim, sys, os, codecs
import pandas as pd

from nltk.corpus import brown
from Politweet import get_tweets


def train_word2vec_brown(output="datasets/brown_word2vec.model"):
    model = gensim.models.Word2Vec(brown.sents(), min_count=1)
    model.save(output)


def load_word2vec_model(model="datasets/brown_word2vec.model"):
    if os.path.isfile(model):
        return gensim.models.Word2Vec.load(model)
    sys.exit("Model does not exist.")


# Extract the highest score from the similarity dictionary
def extract_highest(sim_tweets_topics):
    topic = str()
    score = 0.0

    for t, s in sim_tweets_topics.items():
        if s > score:
            topic = t
            score = s

    return topic, score


def similarity(tweetNouns, topicFromTranscript, model):
    if model is None:
        sys.exit("Model is empty.")

    if tweetNouns is None:
        return None, 0

    # Similarity to each topic
    sim_tweets_topics = dict()

    for topic in topicFromTranscript:
        count = 0
        # If similarity between topic and noun is more than 0.5 then they are related if not ignore
        for noun in tweetNouns:
            try:
                if model.similarity(topic, noun) > 0.5:
                    # Count how many nouns are related
                    count += 1
            except:
                pass
        # Calculate the total percentage of nouns that are related to this topic
        try:
            sim = float(float(count) / float(len(tweetNouns)))
            sim_tweets_topics[topic] = sim
        except:
            sim_tweets_topics[topic] = 0

    return extract_highest(sim_tweets_topics)


# Check if noun is related to at leat one word in the bag-of-words
def filter_noun(noun, bow, model):
    for b in bow:
        try:
            if model.similarity(noun, b) > 0.5:
                return True
        except:
            pass
    return False


def classify_transcript(fname, model):
    if not os.path.isfile(fname):
        sys.exit("Transcript file does not exist")

# Load topics
def load_topics(fname_topics):
    topics = []
    with codecs.open(fname_topics, 'r', 'utf-8') as f:
        for line in f:
            topic_num, bow = line.strip().split(" : ")
            bow_list = bow.split(",")
            topics.append(bow_list)
    return topics


def get_topic(tweetTokens):
    # Load topics from transcript
    topics = load_topics("topics_mapping.txt")
    model = load_word2vec_model()
    topic = str()
    score = float(0.0)
    for x in range (0, len(topics)):
        t, s = similarity(tweetTokens, topics[x], model)
        if float(s) > float(score):
            topic = t
            score = float(s)
    return topic, score


if __name__ == "__main__":

    tweets = get_tweets("datasets/tweets.tsv")
    for i, tweet in tweets.iterrows():
        #print tweet["tokens"]
        topic, score = get_topic(tweet["tokens"])
        print "Topic:", topic, "Score:", score
    #print similarity(["economy", "money", "veteran", "peace", "oil", "war"], ["tax", "attack"], model)
    #print similarity(["tax", "money", "president", "company"], ["tax", "attack", "house", "stock"], model)
