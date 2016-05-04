from nltk import bigrams
from nltk import trigrams
from tokenizers import twokenize
from classifiers import SVM
import numpy as np
from sklearn import svm,linear_model
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import classification_report
import time
from embeddings import GloveDictionary
import pickle
import os.path
from clusters import Clusters
from lexicons import negations,Slang,SocalLexicon,MinqingHuLexicon,afinn,NRCLexicon,MPQALexicon,SentiWordNetLexicon
from lexicons.afinn import Afinn
from sklearn.cross_validation import KFold

#keep the pos tags whose label is c
def subList(pos_tags,labels,c):
    sub=[]
    for i in range(0,len(pos_tags)):
        if labels[i]==c:
            sub.append(pos_tags[i])

    return sub

#keep messages which label is positive or negative
def polaritySubList(subjList,labels):
    polList=[]
    for i in range(0,len(subjList)):
        if labels[i]!="neutral":
            polList.append(subjList[i])
            
    return polList

#tokenize a message
def tokenize(l):
    tokens=[]

    for item in l:
        tokens.append(twokenize.simpleTokenize(item))

    return tokens
	
#caclulate F1 and Precision scores of a message
def getLexiconF1andPrecision(l, messages, labels):
    #initialize dictionaries (exactly the same for positive-negative messages)
    precision_obj = {}
    f1_obj = {}
    precision_sub = {}
    f1_sub = {}

    #get all words from lexicon
    words = l.lexicon

    #number of messages that are objective
    x1 = len([x for x in labels if x==0])
    #number of messages that are subjective
    x2 = len([x for x in labels if x==1])

    for word in words:
        #number of messages that contain "word" and are objective
        x3 = 0
        #number of messages that contain "word" and are subjective
        x4 = 0
        #number of messages that contain the "word"
        x5 = 0

        for i in range(0,len(messages)):
            if (word in messages[i]):
                x5+=1

                if(labels[i]==0):
                    x3+=1
                else:
                    x4+=1

        #precision
        if x5!=0:
            precision_obj[word] = x3/float(x5)
            precision_sub[word] = x4/float(x5)
        else:
            precision_obj[word] = 0
            precision_sub[word] = 0

        #recall
        if x1==0:
            recall_obj = 0
        else:
            recall_obj = x3/float(x1)
            
        if x2==0:
            recall_sub = 0
        else:
            recall_sub = x4/float(x2)

        #F1
        if (precision_obj[word] + recall_obj)==0:
            f1_obj[word] = 0
        else:
            f1_obj[word] = (2*precision_obj[word]*recall_obj)/float(precision_obj[word] + recall_obj)

        if (precision_sub[word] + recall_sub)==0:
            f1_sub[word] = 0
        else:
            f1_sub[word] = (2*precision_sub[word]*recall_sub)/float(precision_sub[word] + recall_sub)
            

    return precision_obj, f1_obj, precision_sub, f1_sub

#caclulate F1 and Precision scores of a message
#caclulate F1 and Precision scores of a message
def getLexiconF1andPrecisionNeutral(l, messages, labels):

    #initialize dictionaries (exactly the same for positive-negative messages)
    precision_neutral = {}
    f1_neutral = {}
    precision_positive = {}
    f1_positive = {}
    precision_negative = {}
    f1_negative = {}

    #get all words from lexicon
    words = l.lexicon

    #number of messages that are neutral
    x1 = len([x for x in labels if x==0])
    #number of messages that are positive
    x2 = len([x for x in labels if x==1])
    #number of messages that are negative
    x3 = len([x for x in labels if x==-1])

    for word in words:
        #number of messages that contain "word" and are neutral
        x4 = 0
        #number of messages that contain "word" and are positive
        x5 = 0
        #number of messages that contain "word" and are negative
        x6 = 0
        #number of messages that contain the "word"
        x7 = 0

        for i in range(0,len(messages)):
            if (word in messages[i]):
                x7+=1

                if(labels[i]==0):
                    x4+=1
                elif (labels[i]==1):
                    x5+=1
                else:
                    x6+=1

        #precision
        if x7!=0:
            precision_neutral[word] = x4/float(x7)
            precision_positive[word] = x5/float(x7)
            precision_negative[word] = x6/float(x7)
        else:
            precision_neutral[word] = 0
            precision_positive[word] = 0
            precision_negative[word] = 0

        #recall
        if x1==0:
            recall_neutral = 0
        else:
            recall_neutral = x4/float(x1)
            
        if x2==0:
            recall_positive = 0
        else:
            recall_positive = x5/float(x2)

        if x3==0:
            recall_negative = 0
        else:
            recall_negative = x6/float(x3)
            
        #F1
        if (precision_neutral[word] + recall_neutral)==0:
            f1_neutral[word] = 0
        else:
            f1_neutral[word] = (2*precision_neutral[word]*recall_neutral)/float(precision_neutral[word] + recall_neutral)

        if (precision_positive[word] + recall_positive)==0:
            f1_positive[word] = 0
        else:
            f1_positive[word] = (2*precision_positive[word]*recall_positive)/float(precision_positive[word] + recall_positive)

        if (precision_negative[word] + recall_negative)==0:
            f1_negative[word] = 0
        else:
            f1_negative[word] = (2*precision_negative[word]*recall_negative)/float(precision_negative[word] + recall_negative)
            

    return precision_neutral, f1_neutral, precision_positive, f1_positive, precision_negative, f1_negative
	
#calculate F1 and Precision scores for every word of every lexicon
def getScores(lexicons,messages, labels,neutral=False):
    
    scores = []
    if neutral:
         for lexicon in lexicons:
            x1, x2, x3, x4, x5, x6 = getLexiconF1andPrecisionNeutral(lexicon, messages, labels)
            scores.append(x1)
            scores.append(x2)
            scores.append(x3)
            scores.append(x4)
            scores.append(x5)
            scores.append(x6)
    else:
        for lexicon in lexicons:
            x1, x2, x3, x4 = getLexiconF1andPrecision(lexicon, messages, labels)
            scores.append(x1)
            scores.append(x2)
            scores.append(x3)
            scores.append(x4)

    return scores

#return pos_tag list as a set	
def getPosTagsSet(pos_tags):
    s = set()
    
    for x in pos_tags:
        for pos_tag in x:
            s.add(pos_tag)

    return list(s)
        
#return pos_bigrams list as a set   
def getBigramsSet(pos_bigrams):
    s = set()
    
    for x in pos_bigrams:
        for bigram in x:
            s.add(bigram)


    return list(s)
	
#return pos_trigrams list as a set
def getTrigramsSet(pos_bigrams):
    s = set()
    
    for x in pos_bigrams:
        for bigram in x:
            s.add(bigram)


    return list(s)

#calculate bigrams of every item of the list l
def getBigrams(l):
    b = []
    for x in l:
        b.append(list(bigrams(x)))

    return b

#calculate trigrams of every item of the list l
def getTrigrams(l):
    tr = []
    for x in l:
        tr.append(list(trigrams(x)))

    return tr

#calculate pos tag score
def posTagsScore(postags,category,pos_tags,labels):
    
    #keep pos tagsof specific category
    pos_tags_category = subList(pos_tags,labels,category)

    #initialize dictionary
    d = {}

    #calculate score for every bigram
    for postag in postags:
        d[postag] = score(postag,category,pos_tags_category,pos_tags)


    return d

#calculate pos bigram score
def posBigramsScore(bigrams,category,pos_tags_bigrams,labels):
    #keep pos tags bigrams of specific category
    bigrams_category = subList(pos_tags_bigrams,labels,category)

    #initialize dictionary
    d = {}

    #calculate score for every bigram
    for bigram in bigrams:
        d[bigram] = score(bigram,category,bigrams_category,pos_tags_bigrams)


    return d

#calculate pos trigram score
def posTrigramsScore(trigrams,category,pos_tags_trigrams,labels):
    
    #keep pos tags bigrams of specific category
    trigrams_category = subList(pos_tags_trigrams,labels,category)

    #initialize dictionary
    d = {}

    #calculate score for every bigram
    for trigram in trigrams:
        d[trigram] = score(trigram,category,trigrams_category,pos_tags_trigrams)

    return d

#calculate bigram's f1 score
def score(bigram,category,bigrams_category,pos_tags_bigrams):
    #messages of "category" containing "bigram"
    x1 = 0
    for i in range(0,len(bigrams_category)):
        if bigram in bigrams_category[i]:
            x1+=1

    #messages containing "bigram"
    x2 = 0
    for i in range(0,len(pos_tags_bigrams)):
        if bigram in pos_tags_bigrams[i]:
            x2 += 1

    #messages of "category"
    x3 = len(bigrams_category)

    if(x2==0):
        precision=0
    else:
        precision = x1/float(x2)
        
    recall = x1/float(x3)
    

    #return f1 score
    if precision==0 or recall==0:
        return 0
    
    return (2*precision*recall)/float(precision + recall)

#save Glove embeddings
def saveGlove(glove):
    start = time.time()

    with open('resources/words.pkl', 'wb') as output:
        pickle.dump(glove.words, output, pickle.HIGHEST_PROTOCOL)
            
    np.save("resources/embeddings", glove.embeddings)

    print "glove saved"
	
#load Glove embeddings
def loadGlove(d=200):
    start = time.time()

    f1 = 'resources/words.pkl'
    f2 = 'resources/embeddings.npy'

    if (os.path.isfile(f1) and os.path.isfile(f2)):
        with open(f1, 'rb') as input:
            w = pickle.load(input)
            
        e = np.load(f2)
        glove = GloveDictionary.Glove(words=w, emb=e)
    else:
	glove = GloveDictionary.Glove(d)
	saveGlove(glove)

    end=time.time()
    return glove

#save trained moleds
def saveModels(sd1,sd2,sp1,sp2):
    #save SD models
    with open('resources/sd_models.pkl', 'wb') as output:
        pickle.dump(sd1, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(sd2, output, pickle.HIGHEST_PROTOCOL)
    print "Sp models saved!"

    #save SP models
    with open('resources/sp_models.pkl', 'wb') as output:
        pickle.dump(sp1, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(sp2, output, pickle.HIGHEST_PROTOCOL)		
    print "Sd models saved!"
	
#get confidence scores of Subjectivity detection 
def getConfidenceScores(features_train, labels_train, C):
    train_confidence = []
    #confidence scores for training data are computed using K-fold cross validation
    kfold = KFold(features_train.shape[0], n_folds=10)

    for train_index,test_index in kfold:
        X_train, X_test = features_train[train_index], features_train[test_index]
        y_train, y_test = labels_train[train_index], labels_train[test_index]

        #train classifier for the subset of train data
        m = SVM.train(X_train,y_train,c=C,k="linear")

        #predict confidence for test data and append it to list
        conf = m.decision_function(X_test)
        for x in conf:
                train_confidence.append(x)

    return np.array(train_confidence)
	
#save pos scores
def savePosScores(pos_tags_scores_neutral, pos_tags_scores_positive,pos_tags_scores_negative,pos_bigrams_scores_neutral,pos_bigrams_scores_positive,pos_bigrams_scores_negative,pos_trigrams_scores_neutral,pos_trigrams_scores_positive,pos_trigrams_scores_negative,mpqaScores):
    with open('resources/scores.pkl', 'wb') as output:
        pickle.dump(pos_tags_scores_neutral, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_tags_scores_positive, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_tags_scores_negative, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_bigrams_scores_neutral, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_bigrams_scores_positive, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_bigrams_scores_negative, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_trigrams_scores_neutral, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_trigrams_scores_positive, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(pos_trigrams_scores_negative, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(mpqaScores, output, pickle.HIGHEST_PROTOCOL)

    print "POS scores saved"

#save lexicons
def saveLexicons(negationList,slangDictionary,lexicons,mpqa_lexicons):        
    #save lexicons
    with open('resources/lexicons.pkl', 'wb') as output:
        pickle.dump(negationList, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(slangDictionary, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(lexicons, output, pickle.HIGHEST_PROTOCOL)
        pickle.dump(mpqa_lexicons, output, pickle.HIGHEST_PROTOCOL)
        
    print "Lexicons saved"

#save clusters
def saveClusters(clusters):
    #save clusters
    with open('resources/clusters.pkl', 'wb') as output:
        pickle.dump(clusters, output, pickle.HIGHEST_PROTOCOL)

    print "Clusters saved"
    
#load Word Clusters	
def loadClusters():
    return Clusters.Clusters()

#load Lexicons
def loadLexicons():
    #get negations list
    negationList = negations.loadNegations();

    #load Slang Dictionary
    slangDictionary = Slang.Slang()

    #Minqing Hu Lexicon
    minqinghu = MinqingHuLexicon.MinqingHuLexicon()
    #Afinn Lexicon
    afinn = Afinn()
    #NRC Lexicons
    nrc2 = NRCLexicon.NRCLexicon(1)
    nrc5 = NRCLexicon.NRCLexicon(4)
    nrc6 = NRCLexicon.NRCLexicon(5)
    #SentiWordNet Lexicon
    swn = SentiWordNetLexicon.SentiWordNetLexicon(False)
    #SentiWordNet Lexicon - AverageScores
    swn_avg= SentiWordNetLexicon.SentiWordNetLexicon(True)

    #do not include MPQA Lexicons
    lexicons = [minqinghu,afinn,nrc2,nrc5,nrc6,swn,swn_avg]

    #MPQA Lexicons (8 Lexicons)
    S_pos = MPQALexicon.MPQALexicon(0)
    S_neg = MPQALexicon.MPQALexicon(1)
    S_pos_neg = MPQALexicon.MPQALexicon(2)
    S_neu = MPQALexicon.MPQALexicon(3)
    W_pos = MPQALexicon.MPQALexicon(4)
    W_neg = MPQALexicon.MPQALexicon(5)
    W_pos_neg = MPQALexicon.MPQALexicon(6)
    W_neu = MPQALexicon.MPQALexicon(7)

    #SEMEVAL_13 Lexicons
    semval_neutral = MPQALexicon.MPQALexicon(8)
    semval_positive = MPQALexicon.MPQALexicon(9)
    semval_negative = MPQALexicon.MPQALexicon(10)

    #MPQA + SEMEVAL_13 Lexicons
    mpqa_lexicons = [S_pos,S_neg,S_pos_neg,S_neu,W_pos,W_neg,W_pos_neg,W_neu,semval_neutral,semval_positive,semval_negative]

    return negationList, slangDictionary, lexicons, mpqa_lexicons

#load Lexicons from a saved file
def loadLexiconsFromFile():
        f = 'resources/lexicons.pkl'

        #if saved file exists
        if os.path.isfile(f):
            with open(f, 'rb') as input:
                    negationList = pickle.load(input)
                    slangDictionary = pickle.load(input)
                    lexicons = pickle.load(input)
                    mpqa_lexicons = pickle.load(input)
        else:
            negationList, slangDictionary, lexicons, mpqa_lexicons = loadLexicons()
            saveLexicons(negationList,slangDictionary,lexicons,mpqa_lexicons)
	
	return negationList, slangDictionary, lexicons, mpqa_lexicons

#load clusters from a saved file
def loadClustersFromFile():
    f = 'resources/clusters.pkl'

    #if saved file exists
    if os.path.isfile(f):
        with open(f, 'rb') as input:
            clusters = pickle.load(input)
    else:
        clusters = loadClusters()
        saveClusters(clusters)
	
    return clusters

#load scores
def loadScores():
    with open('resources/scores.pkl', 'rb') as input:
        pos_tags_scores_neutral = pickle.load(input)
        pos_tags_scores_positive = pickle.load(input)
        pos_tags_scores_negative = pickle.load(input)
        pos_bigrams_scores_neutral = pickle.load(input)
        pos_bigrams_scores_positive = pickle.load(input)
        pos_bigrams_scores_negative = pickle.load(input)
        pos_trigrams_scores_neutral = pickle.load(input)
        pos_trigrams_scores_positive = pickle.load(input)
        pos_trigrams_scores_negative = pickle.load(input)
        mpqaScores = pickle.load(input)

    return pos_tags_scores_neutral, pos_tags_scores_positive, pos_tags_scores_negative, pos_bigrams_scores_neutral, pos_bigrams_scores_positive, pos_bigrams_scores_negative, pos_trigrams_scores_neutral, pos_trigrams_scores_positive, pos_trigrams_scores_negative, mpqaScores
