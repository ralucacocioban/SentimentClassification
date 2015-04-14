import nltk
import datetime
import os
import re
from nltk.corpus import brown, stopwords
from gensim.models import Word2Vec
import string
from nltk.corpus import brown
from nltk.stem.snowball import SnowballStemmer
from gensim.similarities import Similarity

lemmatizer = nltk.WordNetLemmatizer()
#stemmer = nltk.stem.porter.PorterStemmer()

stemmer = SnowballStemmer("english")

def tokenize(speech):
	speech = nltk.sent_tokenize(speech)
	speech = [nltk.word_tokenize(sent) for sent in speech]
	speech = [nltk.pos_tag(sent) for sent in speech]
	return speech

def normalise_word(word):
	word = word.lower()
	#word = stemmer.stem(word)
	word = lemmatizer.lemmatize(word)
	return word

# we assume the nouns are the most important information, and can represent topics

def get_nouns(tags):

	nouns = []

	for sent in tags:
		grammar = """NP : {<NN>*<NNP>*}
		{<DT><NN>|<DT><NNP>}
		"""

		cp = nltk.RegexpParser(grammar)
		result = cp.parse(sent)
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

			#normalised = [normalise_word(word.lower()) for word in nltk.word_tokenize(quote) if normalise_word(word.lower()) not in stopwords.words('english') and normalise_word(word.lower()) not in string.punctuation]
			tokenized = tokenize(quote)

			nouns = get_nouns(tokenized)

			if nouns and len(nouns)>=3:
				#print nouns

				nouns_from_speeches.append((person, date, nouns))
			#else:
			#	nouns_from_speeches.append((person, date, []))

	return nouns_from_speeches

# method to remove nouns to get better suited topics as they are redundant
def clean_nouns(speech):

	speech = [word.lower() for word in speech]
	remove = ['senator', 'mccain', 'obama', 'president', 'sen']

	new_speech = [el for el in speech if not any(ignore in el for ignore in remove)]
	
	return new_speech

def get_transcript_speech():
	speeches = []
	data = get_speeches()
	for row in data:

		pattern = re.compile(',')
		index = [m.start() for m in pattern.finditer(row)]

		if index:
			quote = clean_up_speech(row[index[1]+1:])
			speeches.append(quote)
	return speeches


def create_corpus():
	data = get_name_person_bow()
	count = 0
	for row in data:
		speech = row[2]
		speech = clean_nouns(row[2])
		speech = " ".join(speech)
		f = open('transcriptoutput/' + str(count)+".txt", 'w')
		f.write(speech)
		f.close()
		count+=1

def create_transcript_corpus():
	speeches = get_transcript_speech()
	count = 0
	for speech in speeches:
		tokens = nltk.word_tokenize(speech)
		tokens = [token for token in tokens if token not in stopwords.words('english') and token not in string.punctuation and not token.isdigit()]
		tokens = clean_nouns(tokens)
		tokens = " ".join(tokens)
		print tokens
		f = open('transcriptoutput/transcript/'+ str(count)+".txt", 'w')
		f.write(speech)
		f.close()
		count+=1


def gensim_modelling():

	model = Word2Vec(brown.sents())
	data = get_name_person_bow()

	#model = Word2Vec([x[2] for x in data], min_count=2)

	for row in data:
		if row[2]:
			'do nothing'
			print row[2]
			print 'doesn\'t match'
			print model.doesnt_match(row[2])

#create_corpus()
create_transcript_corpus()			

