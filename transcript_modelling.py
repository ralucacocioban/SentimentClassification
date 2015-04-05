import nltk
import datetime
import os
import re
from nltk.corpus import brown, stopwords
from gensim.models import Word2Vec
import string

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

def tokenize(speech):
	return nltk.word_tokenize(speech)

def normalise_word(word):
	#word = word.lower()
	#word = stemmer.stem_word(word) not impressed with this tool.
	word = lemmatizer.lemmatize(word)
	return word

# we assume the nouns are the most important information, and can represent topics

def get_nouns(speech):

	nouns = []

	tags = nltk.pos_tag(speech)
	grammar = "NP : {<NN>*<NNP>*}"

	cp = nltk.RegexpParser(grammar)
	result = cp.parse(tags)
	for subtree in result.subtrees():
		if subtree.label() == 'NP':
			leaves = subtree.leaves()
			for item in leaves:
				nouns.append(item[0])

	return nouns

def freq_dist(speech):
	fdist = nltk.FreqDist(speech)
	for key in fdist:
		print fdist[key], key

def get_speeches():
	transcript_file = open('datasets/transcript.csv')
	data = transcript_file.read().split('\n')
	transcript_file.close()
	return data


#some sentences have word1.word2, just simple replace of full stop
def clean_up_speech(speech):
	speech = speech.replace('.', ' ')
	return speech


#returns a list containing a triple (name, date, bag of nounds)
def get_name_person_bow():
	speeches = get_speeches()

	nouns_from_speeches = list()

	for row in speeches:

		pattern = re.compile(',')
		index = [m.start() for m in pattern.finditer(row)]

		if index:
			#will use this data after to assign topics to these times and whom was speacking at that particular time
			date = row[0: index[0]]
			person = row[index[0]+1: index[1]]
			quote = clean_up_speech(row[index[1]+1:])

			# print date, person

			normalised = [normalise_word(word.lower()) for word in nltk.word_tokenize(quote) if normalise_word(word.lower()) not in stopwords.words('english') and normalise_word(word.lower()) not in string.punctuation]
			tokenized = tokenize(" ".join(normalised))

			nouns = get_nouns(tokenized)

			if nouns:
				nouns_from_speeches.append((person, date, nouns))
			else:
				nouns_from_speeches.append((person, date, []))

	return nouns_from_speeches

def gensim_modelling():

	googlenewsfilepath = os.path.join('/Users/Manal/Downloads', 'GoogleNews-vectors-negative300.bin')

	model = Word2Vec.load_word2vec_format(googlenewsfilepath, binary=True)

	data = get_name_person_bow()
	for row in data:
		print row[2]
		print 'doesn\'t match'
		print model.doesnt_match(row[2].split())
		print 'similarities'
		print model.similarity(row[2].split())
		print '#######\n\n'

gensim_modelling()
