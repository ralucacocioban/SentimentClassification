from Politweet import get_tweets
from nltk import word_tokenize, pos_tag, sent_tokenize


def findAdjective(tokens, negation):
	sentencepos = pos_tag(tokens)
	adjnegdistance = 5
	adj = None
	adjIndex = None
	for i, (token, pos) in enumerate(sentencepos):
		if pos == 'JJ' and abs(i - negation['index']) < adjnegdistance:
			adjnegdistance = abs(i - negation['index'])
			adj = token
			adjIndex = i
	return (adjIndex, adj)

def isNegation(word):
	negations = ["n't", "not"]
	if word in negations:
		return True

def findNegation(tokens):
	negations = []
	for i, token in enumerate(tokens):
		if isNegation(token):
			negations.append({"index" : i, "token" : token})
	return negations


def findNegationAndAdjective(sentence):
	sentenceTokens = word_tokenize(sentence)
	negations = findNegation(sentenceTokens)
	if len(negations) == 0:
		return None
	for neg in negations:
		index, adjective = findAdjective(sentenceTokens, neg)
		neg["adjectiveIndex"] = index
		neg["adjectiveToken"] = adjective
	return negations

tweets = get_tweets("./datasets/tweets.tsv")
for i in range(len(tweets)):
	tweetsentences = sent_tokenize(tweets.iloc[i].content)
	for sentence in tweetsentences:
		negations = findNegationAndAdjective(sentence)
		if negations != None:
			print sentence
			for neg in negations:
				if(neg['adjectiveIndex'] != None):
					print negations
