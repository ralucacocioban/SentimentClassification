#! /usr/bin/python

import nltk
import math
import sentiWordNet
import Politweet
import os
import sys
import codecs
from Politweet import get_tweets
from match_tweet_to_topic import load_word2vec_model, similarity, filter_noun


def extractTopics(tweet):
	topics = [];

	sentence = Politweet.tokenizer(tweet);
	for elem in sentence:
		if(elem['pos'] in ['NN', 'NNS', 'NNP', 'NNPS']):
			topics.append(elem['lemma']);

	# print tweet;
	# print topics;
	return topics;

def read_relevant_topics(fname):
	if not os.path.isfile(fname):
		sys.exit("File does not exist.")
	relevant_topics = []

	with codecs.open(fname, 'r', 'utf-8') as f:
		for line in f:
			word = line.strip()
			relevant_topics.append(word)
	return relevant_topics

def filterNouns(tweet_topics):
	relevant_topics = read_relevant_topics("relevantTopics.txt")
	model = load_word2vec_model("datasets/brown_word2vec.model")
	ignore_list = []
	for tweet in tweet_topics:
		nouns = tweet['topics'];
		#here write the excluding function with similarity with relevantTopics.txt
		filtered_nouns = [noun for noun in nouns if filter_noun(noun, relevant_topics, model) == True]
		#print filtered_nouns
		topic, score = similarity(filtered_nouns, relevant_topics, model)
		print """{0}:""".format(topic), score, "\n"
		#print nouns

if __name__ == '__main__':
	tweets = get_tweets('./datasets/tweets.tsv')

	tweet_topics = [];

	for i,t in tweets.iterrows():
		topics = extractTopics(t['content'])
		if(topics != []):
			tweet_topics.append({'tweet': t['content'], 'topics' : topics});

	filterNouns(tweet_topics)
