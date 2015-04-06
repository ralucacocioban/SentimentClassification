#! /usr/bin/python

import nltk
import math
import sentiWordNet
import Politweet


# declare the three classes of classification
NEGATIVE = 1
POSITIVE = 2
MIXED = 3
OTHER = 4


# simple clasifier that only takes into account how many times a word#sence is more positive than negative
def simpleSentiWordNetClasifier(sentence):
	print sentence;
	count_vector = [0] * 5;

	sentence = Politweet.tokenizer(sentence);
	for elem in sentence:
		sentiWordNet_pos = sentiWordNet.getSentiWordPOS(elem['pos']);

		if(sentiWordNet_pos != ''):
			synsets = sentiWordNet.get_samePOSsynsets(elem['lemma'],sentiWordNet_pos);
			if(synsets != None):
				count_vector[getSentiWordScore(synsets)] += 1;	

	if(count_vector[NEGATIVE] == count_vector[POSITIVE] and count_vector[NEGATIVE] != 0):
		sentiWordNet.printClass(MIXED);
	elif(count_vector[NEGATIVE] != 0 and count_vector[NEGATIVE] > count_vector[POSITIVE]):
		sentiWordNet.printClass(NEGATIVE);
	# elif(count_vector[POSITIVE] != 0 and count_vector[POSITIVE] > count_vector[NEGATIVE]):
	# 	sentiWordNet.printClass(POSITIVE);		
	else:
		sentiWordNet.printClass(count_vector.index(max(count_vector)));



def getSentiWordScore(sentiwordList):

	pos_gt_neg = 0;
	neg_gt_pos = 0;
	obj_entries = 0;

	for sentiword in sentiwordList:
		# print sentiword.pos_score();
		# print sentiword.neg_score();
		# print sentiword.obj_score();
		if(sentiword.pos_score() > sentiword.neg_score()):
			pos_gt_neg += 1;
		elif(sentiword.neg_score() > sentiword.pos_score()):
			neg_gt_pos += 1;
		elif(sentiword.pos_score() == sentiword.neg_score()):
			obj_entries += 1;		
		elif(sentiword.obj_score() > 0):
			obj_entries += 1;	
	
	# print "pos_gt_neg", pos_gt_neg
	# print "neg_gt_pos", neg_gt_pos
	# print "obj entries", obj_entries

	if(pos_gt_neg > neg_gt_pos and math.fabs(pos_gt_neg - obj_entries) < 5):
		return POSITIVE;
	elif(neg_gt_pos > pos_gt_neg):
		return NEGATIVE;
	elif(neg_gt_pos == pos_gt_neg and neg_gt_pos != 0 and (math.fabs(neg_gt_pos - obj_entries) <= 3)): 
		return MIXED;	
	else:
		return OTHER;	


if __name__ == '__main__':

	#x = Politweet.get_tweets('/Users/ralucamelon/Documents/UCL3/IR_DataMining/SentimentClassification/datasets/tweets.tsv', pickle="tweets.pickle");
	#print x["content"];
	s1 = 'McCain seems to start every sentence with "the point is that...." #tweetdebate #current';
	s2 = "@davidweiner You're playing that game?  I'm drinking everytime I hear #economy."; 
	s3 = "McCain -1 avoiding the question? wait, waht was the question exactly.. #tweetdebate	bluejack"
	s4 = "@current  Ah yes, the pot and the kettle are debating who is to blame for the proverbial heat in the kitchen."
	s5 = "#tweetdebate Obama right to focus on issues in deregulation, and McCain ignoring these issues";

	simpleSentiWordNetClasifier(s3);	
