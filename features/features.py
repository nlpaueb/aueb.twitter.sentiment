import numpy as np
from morphologicalFeatures import *
from posBasedFeatures import *
from lexiconBasedFeatures import *
from posBigramsFeatures import *
from otherFeatures import *
from clusterFeatures import *

#return feautures of a list of messages as an array
def getFeatures(messages,tokens,pos,slangDictionary,lexicons,mpqa_lexicons,pos_bigrams,pos_trigrams,pos_bigrams_scores_objective,pos_bigrams_scores_subjective,pos_trigrams_scores_objective,pos_trigrams_scores_subjective,pos_tags_scores_objective,pos_tags_scores_subjective,mpqaScores,negationList,clusters,pos_bigrams_scores_neutral=None,pos_trigrams_scores_neutral=None,pos_tags_scores_neutral=None):
    #initialize empty list with features for all message
    features = []

    #calculate features for every message
    for i in range(0,len(messages)):
        #list with features for one message
        f = calculateFeatures(messages[i],tokens[i],pos[i],slangDictionary,lexicons,mpqa_lexicons,pos_bigrams[i],pos_trigrams[i],pos_bigrams_scores_objective,pos_bigrams_scores_subjective,pos_trigrams_scores_objective,pos_trigrams_scores_subjective,pos_tags_scores_objective,pos_tags_scores_subjective,mpqaScores,negationList,clusters,pos_bigrams_scores_neutral,pos_trigrams_scores_neutral,pos_tags_scores_neutral)

        #add f to features
        features.append(f)

    #convert features list to numpy array
    features = np.array(features)
    #return test array , with no actual features
    #features_array = np.random.rand(len(messages),10)

    #return result
    return features

#calculate features for a message
def calculateFeatures(message,tokens,pos,slangDictionary,lexicons,mpqa_lexicons,pos_bigrams,pos_trigrams,pos_bigrams_scores_objective,pos_bigrams_scores_subjective,pos_trigrams_scores_objective,pos_trigrams_scores_subjective,pos_tags_scores_objective,pos_tags_scores_subjective,mpqaScores,negationList,clusters,pos_bigrams_scores_neutral,pos_trigrams_scores_neutral,pos_tags_scores_neutral):    

    f=[]
    #Morphological Features
  
    #existance of enlogated tokens in message e.g. "baaad"
    x = hasElongatedWords(message)
    f.append(x)

    #the number of elongated tokens in the message
    x = numberOfElongatedWords(message)
    f.append(x)

    #existance of date expressions in message
    x = hasDateExpressions(message)
    f.append(x)

    #existance of time expressions in message
    x = hasTimeExpressions(message)
    f.append(x)

    #the number of tokens of the message that are fully capitalized
    x = countFullyCapitalizeTokens(tokens)
    f.append(x)

    #the number of tokens that are partially capitalized
    x = countPartiallyCapitalizeTokens(tokens)
    f.append(x)

    #the number of tokens that start with an upper case letter
    x = countUpper(tokens)
    f.append(x)

    #the number of exclamation marks in the message
    ex = countExclamationMarks(message)
    f.append(ex)

    #the number of question marks
    qu = countQuestionMarks(message)
    f.append(qu)

    #the sum of exclamation and question marks
    x = ex + qu
    f.append(x)

    #the number of tokens containing only exclamation marks
    x = onlyQuestionMarks(tokens)
    f.append(x)

    #the number of tokens containing only exclamation marks
    x = onlyExclamationMarks(tokens)
    f.append(x)

    #the number of tokens containing only exclamation marks
    x = onlyQuestionOrExclamationMarks(tokens)
    f.append(x)

    #the number of tokens containing only ellipsis (...)
    x = countEllipsis(tokens)
    f.append(x)

    #the existence of a subjective emoticon at the message's end
    x = hasEmoticonAtEnd(tokens[len(tokens)-1],pos[len(pos)-1])
    f.append(x)

    #the existence of an ellipsis and a link (URL) at the message's end
    x = hasUrlOrEllipsisAtEnd(tokens[len(tokens)-1],pos[len(pos)-1])
    f.append(x)

    #the existence of an exclamation mark at the message's end
    x = hasExclamationMarkAtEnd(tokens[len(tokens)-1])
    f.append(x)

    #the existence of a question mark at the message's end
    x = hasQuestionMarkAtEnd(tokens[len(tokens)-1])
    f.append(x)

    #the existence of a question or an exclamation mark at the message's end
    x = hasQuestionOrExclamationMarkAtEnd(tokens[len(tokens)-1])
    f.append(x)

    #the existence of slang
    x = hasSlang(tokens,slangDictionary)
    f.append(x)

    #Pos Based Features

    #the number of adjectives in the message
    x1 = numberOfAdjectives(pos)
    #f.append(x)

    #the number of adverbs
    x2 = numberOfAdverbs(pos)
    #f.append(x)

    #the number of interjections
    x3 = numberOfIntejections(pos)
    #f.append(x)

    #the number of verbs
    x4 = numberOfVerbs(pos)
    #f.append(x)

    #the number of nouns
    x5 = numberOfNouns(pos)
    #f.append(x)

    #the number of proper nouns
    x6 = numberOfProperNouns(pos,tokens)
    #f.append(x)

    #the number of urls
    x7 = numberOfUrls(pos,tokens)
    #f.append(x)

    #the number of subjective emoticons
    x8 = numberOfSubjectiveEmoticons(pos,tokens)
    #f.append(x)

    #find the sum of "special" tokens
    s = x1+x2+x3+x4+x5+x6+x7+x8

    #divide scores with s and normialize to [-1,1]
    try:
        f.append(2*(x1/float(s))-1)
        f.append(2*(x2/float(s))-1)
        f.append(2*(x3/float(s))-1)
        f.append(2*(x4/float(s))-1)
        f.append(2*(x5/float(s))-1)
        f.append(2*(x6/float(s))-1)
        f.append(2*(x7/float(s))-1)
        f.append(2*(x8/float(s))-1)
    except:
        f.append(0)
        f.append(0)
        f.append(0)
        f.append(0)
        f.append(0)
        f.append(0)
        f.append(0)
        f.append(0)
        
##    f.append(x1/float(s))
##    f.append(x2/float(s))
##    f.append(x3/float(s))
##    f.append(x4/float(s))
##    f.append(x5/float(s))
##    f.append(x6/float(s))
##    f.append(x7/float(s))
##    f.append(x8/float(s))

    #Pos Tags Features
        
    #the average,maximun,minium f1 score for the messages pos bigrams for negative messages
    average, maximum, minimum = F1PosTagsScore(pos,pos_tags_scores_objective)
    f.append(average)
    f.append(maximum)
    f.append(minimum)

    #the average,maximun,minium f1 score for the messages pos bigrams for positive messages
    average, maximum, minimum = F1PosTagsScore(pos,pos_tags_scores_subjective)
    f.append(average)
    f.append(maximum)
    f.append(minimum)

    if pos_tags_scores_neutral is not None:
        #the average,maximun,minium f1 score for the messages pos bigrams for neutral messages
        average, maximum, minimum = F1PosTagsScore(pos,pos_tags_scores_neutral)
        f.append(average)
        f.append(maximum)
        f.append(minimum)


    #Pos Bigrams Features
    
    #the average,maximun,minium f1 score for the messages pos bigrams for objective messages
    
    
    average, maximum, minimum = F1PosBigramsScore(pos_bigrams,pos_bigrams_scores_objective)
    f.append(average)
    f.append(maximum)
    f.append(minimum)

    #the average,maximun,minium f1 score for the messages pos bigrams for objective messages
    average, maximum, minimum = F1PosBigramsScore(pos_bigrams,pos_bigrams_scores_subjective)
    f.append(average)
    f.append(maximum)
    f.append(minimum)
    
    if pos_bigrams_scores_neutral is not None:
        average, maximum, minimum = F1PosBigramsScore(pos_bigrams,pos_bigrams_scores_neutral)
        f.append(average)
        f.append(maximum)
        f.append(minimum)

    #Pos Trigrams Features

    #the average,maximun,minium f1 score for the messages pos bigrams for negative messages
    average, maximum, minimum = F1PosTrigramsScore(pos_trigrams,pos_trigrams_scores_objective)
    f.append(average)
    f.append(maximum)
    f.append(minimum)

    #the average,maximun,minium f1 score for the messages pos bigrams for positive messages
    average, maximum, minimum = F1PosTrigramsScore(pos_trigrams,pos_trigrams_scores_subjective)
    f.append(average)
    f.append(maximum)
    f.append(minimum)

    if pos_trigrams_scores_neutral is not None:
        average, maximum, minimum = F1PosBigramsScore(pos_trigrams,pos_trigrams_scores_neutral)
        f.append(average)
        f.append(maximum)
        f.append(minimum)
        
    # Lexicon Based Features

    #iterate for every lexicon
    for lexicon in lexicons:
        #score of lexicon (total score of all words)
        x = sumOfScores(lexicon,message,tokens,pos)
        f.append(x)

        #average of scores
        f.append(x/float(len(tokens)))

        #max score of words
        x = maxOfScores(lexicon,tokens,pos,False)
        f.append(x)

        #min score of words
        x = minOfScores(lexicon,tokens,pos,False)
        f.append(x)

        #the count of words of the message that appear in the lexicon
        x = numberOfAppearances(lexicon,tokens)
        f.append(x)

        #the score of the last word of the message
        x = scoreOfLastWord(lexicon,tokens[len(tokens)-1],pos[len(pos)-1])
        f.append(x)

        #the score of the last word of the message that appears in the lexicon
        x = scoreOfLastWordAppearedInLexicon(lexicon,tokens,pos)
        f.append(x)

    #iterate for every mpqa lexicon (no score features because the mpqa lexicons have no subjectivity scores assinged to words)
    for lexicon in mpqa_lexicons:
        #the count of words of the message that appear in the lexicon
        x = numberOfAppearances(lexicon,tokens)
        f.append(x)

    #lexicon presicion and F1 scores
    #lexicon_precision_objective, lexicon_f1_objective, lexicon_precision_subjective, lexicon_f1_subjective

    #iterate for every mpqa lexicon
    if pos_bigrams_scores_neutral is not None:
        step=6
    else:
        step=4
        
    for i in range(0,len(mpqaScores),step):    
        #precision-objective
        average, minimum, maximum = LexiconScores(mpqaScores[i],tokens)
        f.append(average)
        f.append(minimum)
        f.append(maximum)

        #precision-subjective
        average, minimum, maximum = LexiconScores(mpqaScores[i+1],tokens)
        f.append(average)
        f.append(minimum)
        f.append(maximum)

        #F1-objective
        average, minimum, maximum = LexiconScores(mpqaScores[i+2],tokens)
        f.append(average)
        f.append(minimum)
        f.append(maximum)

        #F1-subjective
        average, minimum, maximum = LexiconScores(mpqaScores[i+3],tokens)
        f.append(average)
        f.append(minimum)
        f.append(maximum)

        if pos_bigrams_scores_neutral is not None:
            #precision-neutral
            average, minimum, maximum = LexiconScores(mpqaScores[i+4],tokens)
            f.append(average)
            f.append(minimum)
            f.append(maximum)

            #F1-neutral
            average, minimum, maximum = LexiconScores(mpqaScores[i+5],tokens)
            f.append(average)
            f.append(minimum)
            f.append(maximum)
        

    #Other Features

    #check if message has negation
    x = hasNegation(tokens,negationList)
    f.append(x)

    #check if message has negation preceding words from lexicon
    x = hasNegationPrecedingLexicon(mpqa_lexicons[2],tokens,negationList)
    f.append(x)

    x = hasNegationPrecedingLexicon(mpqa_lexicons[6],tokens,negationList)
    f.append(x)
    
    #Word Clusters
    tags = checkClusters(tokens,clusters)
    f+=tags

    return f
    
