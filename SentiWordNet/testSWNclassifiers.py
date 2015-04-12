
import simpleSentiWordNetClassifier as simpleSWN
import AdjBasedSentiWordNet as adjSWN
import AvgBasedSentiWordNetClassifier as avgBasedSWN
import SummationBasedClassifier as sumBasedSWN

if __name__ == '__main__':

	s1 = 'McCain seems to start every sentence with "the point is that...." #tweetdebate #current';
	s2 = "@davidweiner You're playing that game?  I'm drinking everytime I hear #economy."; 
	s3 = "McCain -1 avoiding the question? wait, waht was the question exactly.. #tweetdebate	bluejack"
	s4 = "@current  Ah yes, the pot and the kettle are debating who is to blame for the proverbial heat in the kitchen."
	s5 = "#tweetdebate Obama right to focus on issues in deregulation, and McCain ignoring these issues";

	s7 = "There is a spectrum, it is not merely just awful-or-awesome!"
	s8 = "if ur oldest candidate in history, why start with i'm not feeling great .. makes u thing you re not looking great either #tweetdebate"
	s9 = "Obama: 1 , McCain 0 : McCain didn't answer the question #tweetdebate"
	s10 = "McCain is not answering the questions  #tweetdebate"
	s11 = "They won't even look at each other."
	s12 = "McCain: I don't mean to go back and forth???"


	TEST = s8;

	print "simple";
	simpleSWN.simpleSentiWordNetClasifier(TEST); 
	print "avg based";
	avgBasedSWN.avgBasedClassifier(TEST);	
	print "adj based";
	adjSWN.adjBasedSentiWordNetClassifier(TEST);	
	print "sum based";
	sumBasedSWN.sumBasedClassifier(TEST);	
	