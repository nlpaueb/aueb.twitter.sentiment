##Instructions for downloading all required files

1. **Word clusters**
  * Go to http://www.cs.cmu.edu/~ark/TweetNLP/ 
  * Search for “50mpaths2” and download it as “50mpaths2.txt”
  * Copy “50mpaths2.txt” to "clusters/TwitterWordClusters/" directory
  
2. **Glove**
  * Go to http://nlp.stanford.edu/projects/glove/
  * Download “glove.twitter.27B.zip” and extract it
  * Copy “glove.twitter.27B.25d.txt”, “glove.twitter.27B.50d.txt”, “glove.twitter.27B.100d.txt” and “glove.twitter.27B.200d.txt” to “embeddings/Glove/” directory

3. **Affin lexicon**
  * Go to https://github.com/fnielsen/afinn/tree/master/afinn
  * Download all files and copy them to “lexicons/afinn” directory

4. **Minqing Hu lexicon**
  * Go to http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar
  * Download opinion lexicon
  * Copy “negative-words.txt” and “positive-words.txt” to “lexicons/Minqing Hu/” directory

5. **MPQA lexicon**
  * Go to http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
  * Download lexicon and extract it
  * Copy “subjclueslen1-HLTEMNLP05.tff” to “lexicons/MPQA/” directory

6. **NRC lexicons**
  * Go to http://saifmohammad.com/WebPages/lexicons.html
  * Download “NRC Word-Emotion Association Lexicon“, extract it and copy “NRC-Emotion-Lexicon-v0.92” folder to “lexicons/NRC/” directory
  * Download “MaxDiff Twitter Sentiment Lexicon”, extract it and copy “MaxDiff-Twitter-Lexicon” folder to “lexicons/NRC/” directory
  * Download “NRC Hashtag Sentiment Lexicon”, extract it and copy “NRC-Hashtag-Sentiment-Lexicon-v0.1” folder to “lexicons/NRC/” directory
  * Download “NRC Hashtag Affirmative Context Sentiment Lexicon and NRC Hashtag Negated Context Sentiment Lexicon” , extract it and copy “HashtagSentimentAffLexNegLex” folder to “lexicons/NRC/” directory
  * Download “Sentiment140 Lexicon”, extract it and copy “Sentiment140-Lexicon-v0.1” folder to “lexicons/NRC” directory
  * Download “Sentiment140 Affirmative Context Lexicon and Sentiment140 Negated Context Lexicon”, extract it and copy “Sentiment140AffLexNegLex” folder to “lexicons/NRC/” directory

7. **Slang dictionary**
  * Go to “lexicons/SlangDictionary” directory and create an empty file named “slangDict.txt”. Every line of  “slangDict.txt” should contain a slang word and its meaning. The slang word and the meaning should be tab separated
  * The slangs words we used where obtained from http://www.noslang.com/dictionary/

8. **So-cal lexicon**
  * Go to https://github.com/DrOttensooser/BiblicalNLPworks/tree/master/SkyDrive/NLP/CommonWorks/Data/Opion-Lexicon-English/SO-CAL
  * Download all files and copy them to “lexicons/SO-CAL” directory

9. **Pos-tagger for Twitter**
  * Go to https://code.google.com/archive/p/ark-tweet-nlp/downloads
  * Download “ark-tweet-nlp-0.3.2.tgz” and extract it
  * Copy “ark-tweet-nlp-0.3.2” folder to “postaggers/” directory

10. **Word tokenizer for Twitter**
  * Go to https://github.com/myleott/ark-twokenize-py
  * Download all files and copy them to “tokenizers/” directory

