#! /usr/bin/python

import nltk
import math
import sentiWordNet
import Politweet
from Politweet import get_tweets


def extractTopics(tweet):
	topics = [];

	sentence = Politweet.tokenizer(tweet);
	for elem in sentence:
		if(elem['pos'] in ['NN', 'NNS', 'NNP', 'NNPS']):
			topics.append(elem['lemma']);

	# print tweet;		
	# print topics;		
	return topics;	

def filterNouns(tweet_topics):
	for tweet in tweet_topics:
		nouns = tweet['topics'];
		#here write the excluding function with similarity with relevantTopics.txt
		print nouns

if __name__ == '__main__':
	tweets = get_tweets('./datasets/tweets.tsv')

	tweet_topics = [];

	for i,t in tweets.iterrows():
		topics = extractTopics(t['content'])
		if(topics != []):
			tweet_topics.append({'tweet': t['content'], 'topics' : topics});
	
	filterNouns(tweet_topics)	


