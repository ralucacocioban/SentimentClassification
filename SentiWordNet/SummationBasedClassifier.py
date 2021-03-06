#! /usr/bin/python

import nltk
import math
import sentiWordNet as swnet
import Politweet as ptweet
from nltk.corpus import sentiwordnet as swn

from ratings import NEGATIVE, POSITIVE, MIXED, OTHER

# uses a treshold value of 0 to ignore the words with 0 pos score and 0 neg score 
# calculates 3 overall scores: pos, neg and obj for each tweet 
# as a sum of pos, neg, obj scores of each term in the tweet that passes the threshold
# the sentiment polarity of the tweet is then determined by the maximum overall score  

THRESHOLD = 0;

def sumBasedClassifier(tweet):

	tokens = ptweet.tokenizer(tweet);
	overall_scores = { 'pos' : 0, 'neg' : 0, 'obj' : 0};

	for token in tokens:
		sentiWordNet_pos = swnet.getSentiWordPOS(token['pos']);
		if(sentiWordNet_pos != ''):
			synsets = swnet.get_samePOSsynsets(token['lemma'],sentiWordNet_pos);
			if(synsets != None):
				overall_scores['neg'] += getTermScores(synsets)['neg'];
				overall_scores['pos'] += getTermScores(synsets)['pos'];
				overall_scores['obj'] += getTermScores(synsets)['obj'];
						
	return clasifyTweet(overall_scores)			


def clasifyTweet(overall_scores):
	if(overall_scores['pos'] > overall_scores['neg']):
		return POSITIVE;
	elif(overall_scores['neg'] > overall_scores['pos']):
		return NEGATIVE;	
	elif(overall_scores['neg'] == overall_scores['pos']):
		return MIXED;
	else:
		return OTHER;		


def getTermScores(sentiWords):

	scores = { 'pos' : 0, 'neg' : 0, 'obj' : 0};

	for word in sentiWords:
		if(word.pos_score() > THRESHOLD and word.neg_score() > THRESHOLD):
			scores['pos'] += word.pos_score();
			scores['neg'] += word.neg_score();
			scores['obj'] += word.obj_score();

	return scores;	 