import os
import numpy as np
import sklearn.feature_extraction.text as text
from sklearn import decomposition

CORPUS_PATH = os.path.join('transcriptoutput', 'transcript')

filenames = sorted([os.path.join(CORPUS_PATH,fn) for fn in os.listdir(CORPUS_PATH)])

vectorizer = text.CountVectorizer(input='filename', stop_words='english', min_df=10)

dtm = vectorizer.fit_transform(filenames).toarray()

num_topics = 10
num_top_words = 10

vocab = np.array(vectorizer.get_feature_names())

clf = decomposition.NMF(n_components=num_topics, random_state=1)

doctopic = clf.fit_transform(dtm)

topic_words = []

for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][0:num_top_words]
    topic_words.append([vocab[i] for i in word_idx])


f = open('matrix_factorization_topics.txt', 'w')
for r in range(len(topic_words)):
    f.write("Topic {}: {}".format(r, ' '.join(topic_words[r][:15])))
    f.write("\n")
f.close()
