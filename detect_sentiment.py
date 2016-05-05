import pickle
import time
from postaggers import arktagger
from utilities import *
from features import features
from classifiers import SVM
import numpy as np
import regularization
import math
import sys

def main(messages_test):
        #tokenize all messages
	tokens_test = tokenize(messages_test)
	#compute pos tags for all messages
	pos_tags_test = arktagger.pos_tag_list(messages_test)
	#compute pos tag bigrams
	pos_bigrams_test = getBigrams(pos_tags_test)
	#compute pos tag trigrams
	pos_trigrams_test = getTrigrams(pos_tags_test)

	now = time.time()

	#load scores
	pos_tags_scores_neutral, pos_tags_scores_positive, pos_tags_scores_negative, pos_bigrams_scores_neutral, pos_bigrams_scores_positive, pos_bigrams_scores_negative, pos_trigrams_scores_neutral, pos_trigrams_scores_positive, pos_trigrams_scores_negative, mpqaScores = loadScores()
	
	#load lexicons
	negationList, slangDictionary, lexicons, mpqa_lexicons = loadLexiconsFromFile()
	
	#load clusters
	clusters = loadClustersFromFile()
		
	print "Resources loaded"
	
	#load Glove embeddings
	d = 200
	glove = loadGlove(d)
		
	#Subjectivity Detection Features
	
	#SD1 features
	features_test_1 = features.getFeatures(messages_test,tokens_test,pos_tags_test,slangDictionary,lexicons,mpqa_lexicons,pos_bigrams_test,pos_trigrams_test,pos_bigrams_scores_negative,pos_bigrams_scores_positive,pos_trigrams_scores_negative,pos_trigrams_scores_positive,pos_tags_scores_negative,pos_tags_scores_positive,mpqaScores,negationList,clusters,pos_bigrams_scores_neutral,pos_trigrams_scores_neutral,pos_tags_scores_neutral)
	
	#SD2 features
	features_test_2=[]
	for i in range(0,len(messages_test)):
		features_test_2.append(glove.findCentroid(tokens_test[i]))

	features_test_2 = np.array(features_test_2)

	#regularize features
	features_test_1=regularization.regularize(features_test_1)
	features_test_2 = regularization.regularizeHorizontally(features_test_2)
	
	#load SD classifiers
	with open('resources/sd_models.pkl', 'rb') as input:
		sd1 = pickle.load(input)
		sd2 = pickle.load(input)
		
	#get confidence scores
	test_confidence_1 = sd1.decision_function(features_test_1)
	test_confidence_2 = sd2.decision_function(features_test_2)

	#normalize confidence scores
	softmax = lambda x: 1 / (1. + math.exp(-x))
	test_confidence_1 = [softmax(conf) for conf in test_confidence_1]
	test_confidence_2 = [softmax(conf) for conf in test_confidence_2]
	
	test_confidence_1 = np.array(test_confidence_1)
	test_confidence_2 = np.array(test_confidence_2)

	#Sentiment Polarity Features (append confidence scores to SD features)
	
	#SP1 features
	features_test_1 = np.hstack((features_test_1,test_confidence_1.reshape(test_confidence_1.shape[0],1)))
	#SP2 features
	features_test_2 = np.hstack((features_test_2,test_confidence_2.reshape(test_confidence_2.shape[0],1)))

	#load SP classifiers
	with open('resources/sp_models.pkl', 'rb') as input:
		sp1 = pickle.load(input)
		sp2 = pickle.load(input)
		
	#get confidence scores of every system
	confidence1 = sp1.decision_function(features_test_1)
	confidence2 = sp2.decision_function(features_test_2)

	for i in range(0,confidence1.shape[0]):
		for j in range(0,confidence1.shape[1]):
			confidence1[i][j] = softmax(confidence1[i][j])

	for i in range(0,confidence2.shape[0]):
		for j in range(0,confidence2.shape[1]):
			confidence2[i][j] = softmax(confidence2[i][j])

	#ensemble confidence scores with weight W
	W=0.66

	confidence = confidence1*W + confidence2*(1-W)

	#get final prediction
	prediction = [np.argmax(x)-1 for x in confidence]
	prediction = np.array(prediction)

	print "Prediction\n"
	for i in range(0, prediction.shape[0]):
		if prediction[i] == -1:
			pol = "Negative"
		elif prediction[i] == 0:
			pol = "Neutral"
		else:
			pol = "Positive"
                print "Message : " + messages_test[i]+"Polarity : "+pol+"\n"
		

if __name__ == "__main__":
	if len(sys.argv)<=1:
		print "Usage : python detect_sentiment.py \"message1\" \"message2\" ..."
		sys.exit(0)
	else:
		user_input = sys.argv[1:]
		for i in range(0,len(user_input)):
			try:
				user_input[i] = user_input[i].decode('utf8')
			except:
                                user_input[i] = unicode(user_input[i], errors='replace')               

	messages_test = []
	for message in user_input:
		if message.strip() != '' :
		   messages_test.append(message.strip()+"\n")

	if len(messages_test) == 0:
		print "Usage : python detect_sentiment.py \"message1\" \"message2\" ..."
                sys.exit(0)
		
	main(messages_test)
