from tsvfiles import tsvreader
import time
from postaggers import arktagger
from utilities import *
from features import features
from classifiers import SVM
import numpy as np
import regularization
from embeddings import GloveDictionary
import math
import sys
import os.path

def main(f):
	print "System training started"
	
        #load training dataset
	dataset_train = f
	ids,labels_train,messages_train=tsvreader.opentsv(dataset_train)
	print "Train data loaded"
	
	#labels for subjectivity detection (2 categories)
	temp_labels_train = [0 if x=="neutral" else 1 for x in labels_train]
	#labels for polarity detection (3 categories)
	labels_train = [0 if x=="neutral" else -1 if x =="negative" else 1 for x in labels_train]
	
	#convert labels to numpy arrays
	temp_labels_train=np.array(temp_labels_train)
	labels_train=np.array(labels_train)
	
	#load word clusters
	clusters = loadClusters()
	print "Clusters loaded"
	
	#load Lexicons
	negationList, slangDictionary, lexicons, mpqa_lexicons = loadLexicons()
	print "Lexicons loaded"

	#tokenize all messages
	tokens_train = tokenize(messages_train)
	print "Messages tokenized"

	#compute pos tags for all messages
	pos_tags_train = arktagger.pos_tag_list(messages_train)
	print "Pos tags computed"
	
	#compute pos tag bigrams
	pos_bigrams_train = getBigrams(pos_tags_train)
	#compute pos tag trigrams
	pos_trigrams_train = getTrigrams(pos_tags_train)

	#get the unique pos bigrams from training set
	unique_pos_tags = getPosTagsSet(pos_tags_train)
	unique_bigrams = getBigramsSet(pos_bigrams_train)
	unique_trigrams= getTrigramsSet(pos_trigrams_train)

	#compute POS tag scores
	pos_tags_scores_neutral = posTagsScore(unique_pos_tags,0,pos_tags_train,labels_train)
	pos_tags_scores_positive = posTagsScore(unique_pos_tags,1,pos_tags_train,labels_train)
	pos_tags_scores_negative = posTagsScore(unique_pos_tags,-1,pos_tags_train,labels_train)
	   
	pos_bigrams_scores_neutral = posBigramsScore(unique_bigrams,0,pos_bigrams_train,labels_train)
	pos_bigrams_scores_positive = posBigramsScore(unique_bigrams,1,pos_bigrams_train,labels_train)
	pos_bigrams_scores_negative = posBigramsScore(unique_bigrams,-1,pos_bigrams_train,labels_train)

	pos_trigrams_scores_neutral = posTrigramsScore(unique_trigrams,0,pos_trigrams_train,labels_train)
	pos_trigrams_scores_positive = posTrigramsScore(unique_trigrams,1,pos_trigrams_train,labels_train)
	pos_trigrams_scores_negative = posTrigramsScore(unique_trigrams,-1,pos_trigrams_train,labels_train)
	
	#compute mpqa scores
	mpqaScores = getScores(mpqa_lexicons,messages_train,labels_train,neutral=True)
	
	#save scores and other resources for future use
	savePosScores(pos_tags_scores_neutral, pos_tags_scores_positive,pos_tags_scores_negative,pos_bigrams_scores_neutral,pos_bigrams_scores_positive,pos_bigrams_scores_negative,pos_trigrams_scores_neutral,pos_trigrams_scores_positive,pos_trigrams_scores_negative,mpqaScores)
        #save lexicons
	saveLexicons(negationList,slangDictionary,lexicons,mpqa_lexicons)
        #save clusters
	saveClusters(clusters)
	
	#load Glove embeddings
	d = 25
	glove = GloveDictionary.Glove(d)

	#save Glove embeddings for future use
	saveGlove(glove)
	
	#Subjectivity Detection Features
	
	#SD1 features
	features_train_1 = features.getFeatures(messages_train,tokens_train,pos_tags_train,slangDictionary,lexicons,mpqa_lexicons,pos_bigrams_train,pos_trigrams_train,pos_bigrams_scores_negative,pos_bigrams_scores_positive,pos_trigrams_scores_negative,pos_trigrams_scores_positive,pos_tags_scores_negative,pos_tags_scores_positive,mpqaScores,negationList,clusters,pos_bigrams_scores_neutral,pos_trigrams_scores_neutral,pos_tags_scores_neutral)
	
	#SD2 features
	features_train_2 = []
	#for message in tokens_train :
	for i in range(0,len(messages_train)):
		features_train_2.append(glove.findCentroid(tokens_train[i]))
	features_train_2 = np.array(features_train_2)
	
	#regularize features
	features_train_1 = regularization.regularize(features_train_1)
	features_train_2 = regularization.regularizeHorizontally(features_train_2)
	
	#Penalty parameter C of the error term for every SD system
	C1=0.001953125
	C2=1.4068830572470667

	#get confidence scores
	train_confidence_1 = getConfidenceScores(features_train_1, temp_labels_train, C1)
	train_confidence_2 = getConfidenceScores(features_train_2, temp_labels_train, C2)
	
	#normalize confidence scores
	softmax = lambda x: 1 / (1. + math.exp(-x))
	train_confidence_1 = [softmax(conf) for conf in train_confidence_1]
	train_confidence_2 = [softmax(conf) for conf in train_confidence_2]
	
	train_confidence_1 = np.array(train_confidence_1)
	train_confidence_2 = np.array(train_confidence_2)

	#train SD classifiers
	sd1 = SVM.train(features_train_1,temp_labels_train,c=C1,k="linear")
	sd2 = SVM.train(features_train_2,temp_labels_train,c=C2,k="linear")
	
	#Sentiment Polarity Features (append confidence scores to SD features)
	
	#SP1 features
	features_train_1 = np.hstack((features_train_1,train_confidence_1.reshape(train_confidence_1.shape[0],1)))
	#SP1 features
	features_train_2 = np.hstack((features_train_2,train_confidence_2.reshape(train_confidence_2.shape[0],1)))

	#Penalty parameter C of the error term for every SP system
	C1=0.003410871889693192
	C2=7.396183688299606

	#train SP classifiers
	sp1 = SVM.train(features_train_1,labels_train,c=C1,k="linear")
	sp2 = SVM.train(features_train_2,labels_train,c=C2,k="linear")
	
	#save trained models
	saveModels(sd1,sd2,sp1,sp2)
	
	print "System training completed!"

if __name__ == "__main__":
	if len(sys.argv)==2:
		#check if dataset exists
		if os.path.exists(sys.argv[1]):
			main(sys.argv[1])
		else:
			print sys.argv[1] + " could not be found!"
	else:
		print "Usage : python train.py train_dataset_path"
		sys.exit(0)
