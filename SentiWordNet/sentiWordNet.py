#! /usr/bin/python

from nltk.corpus import sentiwordnet as swn
from ratings import NEGATIVE, POSITIVE, MIXED, OTHER

def printClass(string):
	if(string == NEGATIVE): print "NEGATIVE";
	elif(string == POSITIVE): print "POSITIVE";
	elif(string == MIXED): print "MIXED";
	else: print "OTHER";



# in SentiWordNet notation: 
# n - NOUN 
# v - VERB 
# a - ADJECTIVE 
# s - ADJECTIVE SATELLITE 
# r - ADVERB 
def getSentiWordPOS(nltk_pos):

	if(nltk_pos in ['RB', 'RBR', 'RBS']):
		return 'r';
	elif(nltk_pos in ['JJ', 'JJR', 'JJS']):
		return 'a';
	elif(nltk_pos in ['NN', 'NNS', 'NNP', 'NNPS']):
		return 'n';
	elif(nltk_pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
		return 'v';
	else:
		return '';

# used for the adjective based algorithm
# it doesn't return anything for nouns
def getSentiWordPOS_adj(nltk_pos):
	if(nltk_pos in ['RB', 'RBR', 'RBS']):
		return 'r';
	elif(nltk_pos in ['JJ', 'JJR', 'JJS']):
		return 'a';
	elif(nltk_pos in ['NN', 'NNS', 'NNP', 'NNPS']):
		return '';
	elif(nltk_pos in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
		return 'v';
	else:
		return '';


# based on a sentiword and a part of speech (pos), get a list with all the sentiwords for that particular pos
def get_samePOSsynsets(sentiword, pos):
	
	listSynsets = swn.senti_synsets(sentiword, pos);
	if(listSynsets):
		return listSynsets;
	else:
		return None;	