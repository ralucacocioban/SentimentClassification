import gensim, sys, os

from nltk.corpus import brown


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
        sim_tweets_topics[topic] = 0
        # If similarity between topic and noun is more than 0.5 then they are related if not ignore
        for noun in tweetNouns:
            if model.similarity(topic, noun) > float(0.5):
                # Count how many nouns are related
                sim_tweets_topics[topic] += 1
        # Calculate the total percentage of nouns that are related to this topic
        sim_tweets_topics[topic] /= len(tweetNouns)

    return extract_highest(sim_tweets_topics)




if __name__ == "__main__":
    train_word2vec_brown()

    model = load_word2vec_model()
