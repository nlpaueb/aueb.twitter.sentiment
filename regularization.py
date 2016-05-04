from sklearn import preprocessing
import numpy as np
import math

#reguralize features to [-1,1] , xi=xi-meam/3*variance
def regularize(features):

    #regularize per column
    for i in range(0,len(features[0])):
	try:
	        #take evary column
        	feat=features[:,i]
    
	        #mean and variance of every column	
        	mean=np.mean(feat)
	        var=np.var(feat)

        	if(var!=0):
	            features[:,i]=(features[:,i]-mean)/float(3*var)
        	else :
	            features[:,i]=0
	except:
		pass

    features[features>1]=1
    features[features<-1]=-1
     
    return features

#reguralize features to [-1,1] horizontally, yi=yi/norm(yi,2)
def regularizeHorizontally(features):
    for i in range(0,features.shape[0]):
	if (features[i] == np.zeros(features[i].shape)).all() == True:
		pass
	else:
		features[i] = features[i]/np.linalg.norm(features[i],ord=2)

    features[features>1]=1
    features[features<-1]=-1
    
    return features

#xi=xi-xmin/xman-xmin
def regularizeMaxMin(features):

    #regularize per column
    for i in range(0,len(features[0])):

        #take evary column
        feat=features[:,i]
    
        #max and min value of every feature 
        xmax=max(feat)
        xmin=min(feat)

        if((xmax-xmin)!=0):
            features[:,i]=(features[:,i]-xmin)/float(xmax-xmin)
        else :
            features[:,i]=0
            
     
    return features
