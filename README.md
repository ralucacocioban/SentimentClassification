# Politweet

- The visualization ([see here](http://ralucacocioban.github.io/SentimentClassification))
- The IPython notebooks explanation of code
  - [Exploring Candidate classification](http://nbviewer.ipython.org/github/ralucacocioban/SentimentClassification/blob/master/Exploring%20Candidate%20classification.ipynb) (Machine learning)
  - [Exploring Sentiment analysis](http://nbviewer.ipython.org/github/ralucacocioban/SentimentClassification/blob/master/Exploring%20Sentiment%20Analysis%20with%20ML.ipynb) (Machine learning)
  - [Visualizing Sentiment and Candidates](http://nbviewer.ipython.org/github/ralucacocioban/SentimentClassification/blob/master/Visualizing%20Sentiment%20and%20Candidates.ipynb)
  - [Exploring Topic modeling with Word2Vec](http://nbviewer.ipython.org/github/ralucacocioban/SentimentClassification/blob/master/Exploring%20Topic%20modeling.ipynb)
  - [Evaluating SentiWordNet Lexicon](http://nbviewer.ipython.org/github/ralucacocioban/SentimentClassification/blob/master/Evaluating%20SentiWordNet.ipynb)


## Our files

- `nn_matrix_factorization.py`: Matrix factorization for topic extraction in the debate
- `ratings.py`: Helpful utility for handling Amazon Mechanical Turks ratings
- `Politweet.py`: Main utilities for extracting tweets and debates. Contains pre-processing part
- `sentiment.py`: Sentiment classification with Rule-based system and ML techniques
- `candidates_class.py`: Candidate classification with Rule-based system and ML techniques
- `topic_extraction.py`: Word2Vec for topic extraction
- `transcript.py`: Cleaning the debate transcript with spell check and heuristics
- `static/`: Folder that contains our HTML visualization with AngularJS
- `SentiWordNet/`: Folder using our SentiWordNet implementations