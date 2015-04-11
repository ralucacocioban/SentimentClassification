
import simpleSentiWordNetClassifier as simpleSWN
import AdjBasedSentiWordNet as adjSWN
import AvgBasedSentiWordNetClassifier as avgBasedSWN
import SummationBasedClassifier as sumBasedSWN
from AvgBasedScoreSWN import avgBased
from SumBasedScoreSWN import sumBased
from nltk.corpus import sentiwordnet as swn
import ratings
import Politweet as ptweet

if __name__ == '__main__':
	s8 = "if ur oldest candidate in history, why start with i'm not feeling great .. makes u thing you re not looking great either #tweetdebate"
	

	TEST = s8;

	
	# tweets = ptweet.get_tweets('./datasets/tweets.tsv');

	# pos = ratings.all(tweets, ratings.POSITIVE)
	# neg = ratings.all(tweets, ratings.NEGATIVE)

	# print simpleSWN.simpleSentiWordNetClasifier(TEST); 
	# print "adj based";
	# print adjSWN.adjBasedSentiWordNetClassifier(TEST);
	
	print "sum based";
	print sumBased(TEST);		
	print "avg based";
	print avgBased(TEST);	
