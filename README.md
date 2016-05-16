#aueb.twitter.sentiment

This is the software that accompanies the [paper](http://nlp.cs.aueb.gr/pubs/SemEval_2016_Task_4.pdf) "aueb.twitter.sentiment at SemEval-2016 Task 4: A Weighted Ensemble of SVMs for Twitter Sentiment Analysis" by Stavros Giorgis, Apostolos Rousas, John Pavlopoulos, Prodromos Malakasiotis and Ion Androutsopoulos. The paper describes the system with which we participated in SemEval-2016 Task 4 (Sentiment Analysis in Twitter) and specifically the Message Polarity Classification subtask. Our system is a weighted ensemble of two systems. The first one is based on a previous sentiment analysis system and uses manually crafted features. The second system of our ensemble uses features based on word embeddings. Our ensemble was ranked 5th among 34 teams.

The basic functionality of the software is to detect the sentiment (positive, negative, neutral) of a message.

#Getting started
```
Python version 2.7.10
Operating System : Linux(Ubuntu)
```
#Requirements

If you are using virtualenv run :

```
virtualenv env
source env/bin/activate
```

Install the required libraries :

```
pip install numpy scipy scikit-learn nltk
```

Download *wordnet* and *sentiwordnet* for NLTK

```
python -c "import nltk;nltk.download('sentiwordnet')"
python -c "import nltk;nltk.download('wordnet')"
```

#Download

```
git clone https://github.com/nlpaueb/aueb.twitter.sentiment.git
cd aueb.twitter.sentiment
```

#Troubleshooting :

Make sure that you have the following requirements installed:

```
sudo apt-get install python-pip python-dev git
```

Make sure that you have a java compiler installed needed for the pos tagging :

```
sudo apt-get install openjdk-7-jdk
```

#External files

In order to be able to run the code successfully you should follow the instructions in [instructions.md](./instructions.md)

#Training

To train the system run :

```
python train.py dataset_file
```

Note that we are not allowed to distribute the datasets provided by SemEval so you have to use your own dataset to train the system.

The dataset must be in the following format:

```
message_id_1  message_sentiment_1 message_1
message_id_2  message_sentiment_2 message_2
…
message_id_k  message_sentiment_k message_k
```
where message_id, message_sentiment and message are separated with tab.

#Sentiment Detection

To detect the sentiment of a tweet run :

```
python detect_sentiment.py “your tweet”
```

#Features list

The complete list of the features which are used for a message's sentiment classification can be found in [features.md](./features.md)
