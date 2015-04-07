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
	print tweet
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
				print "takes into consideration: ", token
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
		swnet.printClass(POSITIVE);
	elif(overall_avg['neg'] > overall_avg['pos']):
		swnet.printClass(NEGATIVE);	
	elif(overall_avg['neg'] == overall_avg['pos'] and overall_avg['neg'] != 0):
		swnet.printClass(MIXED);
	else:
		swnet.printClass(OTHER);		


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


if __name__ == '__main__':

	#x = Politweet.get_tweets('/Users/ralucamelon/Documents/UCL3/IR_DataMining/SentimentClassification/datasets/tweets.tsv', pickle="tweets.pickle");
	#print x["content"];
	s1 = 'McCain seems to start every sentence with "the point is that...." #tweetdebate #current';
	s2 = "@davidweiner You're playing that game?  I'm drinking everytime I hear #economy."; 
	s3 = "McCain -1 avoiding the question? wait, waht was the question exactly.. #tweetdebate	bluejack"
	s4 = "@current  Ah yes, the pot and the kettle are debating who is to blame for the proverbial heat in the kitchen."
	s5 = "#tweetdebate Obama right to focus on issues in deregulation, and McCain ignoring these issues";

	avgBasedClassifier(s5);		 
