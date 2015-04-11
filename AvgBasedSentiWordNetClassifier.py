#! /usr/bin/python

import nltk
import sentiWordNet as swnet
import Politweet as ptweet
from nltk.corpus import sentiwordnet as swn


# Uses an average approach to calculate the score of the tweet.
# For each term in the tweet, it calculate its average pos, neg and obj score
# then the overall tweet score is again calculated as the average of all terms scores (one for pos, one for neg and one for obj)

OBJ_THRESHOLD = 0.85;

# declare the three classes of classification
NEGATIVE = 1
POSITIVE = 2
MIXED = 3
OTHER = 4

def avgBasedClassifier(tweet):
	tokens = ptweet.tokenizer(tweet);

	overall_sum = { 'pos' : 0, 'neg' : 0, 'obj' : 0};
	overall_avg = { 'pos' : 0, 'neg' : 0, 'obj' : 0};
	term_count = 0;

	for token in tokens:
		sentiWordNet_pos = swnet.getSentiWordPOS(token['pos']);
		if(sentiWordNet_pos != ''):
			synsets = swnet.get_samePOSsynsets(token['lemma'],sentiWordNet_pos);
			if(synsets != None and getTermScores(synsets) != None):
				term_count += 1;
				overall_sum['pos'] += getTermScores(synsets)['pos'];
				overall_sum['neg'] += getTermScores(synsets)['neg'];
				overall_sum['obj'] += getTermScores(synsets)['obj'];

	if(term_count > 0):
		overall_avg['pos'] = overall_sum['pos'] / term_count;
		overall_avg['neg'] = overall_sum['neg'] / term_count;
		overall_avg['obj'] = overall_sum['obj'] / term_count;
											
	clasifyTweet(overall_avg)			


def clasifyTweet(overall_avg):
	if(overall_avg['pos'] > overall_avg['neg']):
		print POSITIVE;
	elif(overall_avg['neg'] > overall_avg['pos']):
		print NEGATIVE;	
	elif(overall_avg['neg'] == overall_avg['pos'] and overall_avg['neg'] != 0):
		print MIXED;
	else:
		print OTHER;		


def getTermScores(sentiWords):

	sum = {'pos' : 0, 'neg' : 0, 'obj' : 0};
	avg_scores = {'pos' : 0, 'neg' : 0, 'obj' : 0};

	sentiword_count = len(sentiWords);

	for word in sentiWords:
		if(excludeTerm(word) == False):
			sum['pos'] += word.pos_score()
			sum['neg'] += word.neg_score()
			sum['obj'] += word.obj_score()
		else:
			sentiword_count -= 1;	
				
	if(sentiword_count == 0):
		return None;

	avg_scores['pos'] = sum['pos'] / sentiword_count;
	avg_scores['neg'] = sum['neg'] / sentiword_count;
	avg_scores['obj'] = sum['obj'] / sentiword_count;
	
	#print "avg scores for: ", sentiWords[0] , "  " ,avg_scores;
	return avg_scores;


def excludeTerm(sentiword):
	if(sentiword.obj_score() > OBJ_THRESHOLD):
		return True;
	else:
		return False;	