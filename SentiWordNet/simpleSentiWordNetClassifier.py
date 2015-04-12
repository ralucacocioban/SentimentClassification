#! /usr/bin/python

import nltk
import math
import sentiWordNet
import Politweet
from ratings import NEGATIVE, POSITIVE, MIXED, OTHER

# simple clasifier that only takes into account how many times a word#sence is more positive than negative
def simpleSWNClasifier(sentence):
	count_vector = [0] * 5

	sentence = Politweet.tokenizer(sentence)
	for elem in sentence:
		sentiWordNet_pos = sentiWordNet.getSentiWordPOS(elem['pos'])

		if(sentiWordNet_pos != ''):
			synsets = sentiWordNet.get_samePOSsynsets(elem['lemma'],sentiWordNet_pos)
			if(synsets != None):
				count_vector[getSentiWordScore(synsets)] += 1	

	if(count_vector[NEGATIVE] == count_vector[POSITIVE] and count_vector[NEGATIVE] != 0):
		return MIXED
	elif(count_vector[NEGATIVE] != 0 and count_vector[NEGATIVE] > count_vector[POSITIVE]):
		return NEGATIVE	
	elif(count_vector.index(max(count_vector)) == 0):
		return OTHER;
	else:
		return (count_vector.index(max(count_vector)))


def getSentiWordScore(sentiwordList):

	pos_gt_neg = 0
	neg_gt_pos = 0
	obj_entries = 0

	for sentiword in sentiwordList:
		if(sentiword.pos_score() > sentiword.neg_score()):
			pos_gt_neg += 1
		elif(sentiword.neg_score() > sentiword.pos_score()):
			neg_gt_pos += 1
		elif(sentiword.pos_score() == sentiword.neg_score()):
			obj_entries += 1		
		elif(sentiword.obj_score() > 0):
			obj_entries += 1	


	if(pos_gt_neg > neg_gt_pos and math.fabs(pos_gt_neg - obj_entries) < 5):
		return POSITIVE
	elif(neg_gt_pos > pos_gt_neg):
		return NEGATIVE
	elif(neg_gt_pos == pos_gt_neg and neg_gt_pos != 0 and (math.fabs(neg_gt_pos - obj_entries) <= 3)): 
		return MIXED	
	else:
		return OTHER		
