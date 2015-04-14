import os
import sys
import codecs

from os import listdir
from os.path import isfile, join
from match_tweet_to_topic import load_word2vec_model, similarity, filter_noun


def get_all_topics(fname="matrix_factorization_topics.txt"):
    if not os.path.isfile(fname):
        sys.exit("File does not exist.")

    topics = []
    with codecs.open(fname, 'r', 'utf-8') as f:
        for line in f:
            words = line.strip().split(": ")[1].split(" ")
            for word in words:
                topics.append(word)
    return topics


def score_transcript(speech_files, topics, model):
    for speech in speech_files:
        if speech == "datasets/speech/.DS_Store":
            continue
        print "File:", speech
        with codecs.open(speech, 'r', 'utf-8') as f:
            for line in f:
                nouns = line.strip().split(" ")
                filtered_nouns = [noun for noun in nouns if filter_noun(noun, topics, model) == True]
                topic, score = similarity(filtered_nouns, topics, model)
                print """File: {0} - {1}:{2}""".format(speech, topic, score)


def get_speech_files(directory):
    if not os.path.isdir(directory):
        sys.exit("Directory does not exist.")

    return [ join(directory, f) for f in listdir(directory) if isfile(join(directory,f)) ]


if __name__ == "__main__":
    speech_files = get_speech_files("datasets/speech")
    topics = get_all_topics()
    model = load_word2vec_model()

    score_transcript(speech_files, topics, model)
