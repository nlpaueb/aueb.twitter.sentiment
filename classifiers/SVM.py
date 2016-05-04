#SVM Classifier

from sklearn import svm

#train model
def train(features,labels,g="auto",c=1,k="linear",coef0=0,degree=2):
    #define classifier
    if k=="linear":
        model = svm.LinearSVC(C=c,class_weight="balanced")
    elif k=="poly":
        model=svm.SVC(C=c,kernel=k,degree=degree,coef0=coef0)
    elif k=="rbf":
        model=svm.SVC(C=c,kernel=k,gamma=g,class_weight="balanced",cache_size=1000)

    #fit data
    model.fit(features,labels)

    return model

#predicts labels
def predict(features,model):
    return model.predict(features)




