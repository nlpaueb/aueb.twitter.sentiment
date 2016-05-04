#check if a message has negation
def hasNegation(tokens,negationList):
    for token in tokens:
        if token in negationList:
            return 1

    return 0
	
#check if message has negation preceding words from lexicon
def hasNegationPrecedingLexicon(lexicon,tokens,negationList):
    for i in range(0,len(tokens)):
        if tokens[i] in lexicon.lexicon:
            #get 5 preciding tokens
            subList = tokens[max(0,i-5):i]

            #check if these tokens are in the lexicon
            for token in subList:
                if token in negationList:
                    return 1

    return 0
	
#calculate the existence of happy emoticons
def happy_emoticons(tokens):
    
   return int("<smile>" in tokens)

#calculate the existence of sad emoticons
def sad_emoticons(tokens):

    return int("<sadface>" in tokens)

#the number of appearaces of a pos trigram (Pronoun,Verb,Verb)
def numberOfPronounVerbVerb(trigrams):
  return len([a for a,b,c in trigrams if a=="O" and b=="V" and c =="V"])

  #the number of appearaces of a pos trigram (Verb,Determiner,Noun)
def numberOfVerbDeterminerNoun(trigrams):
  return len([a for a,b,c in trigrams if a=="V" and b=="D" and c =="N"])

  #the number of appearaces of a pos trigram (Position,Determiner,Noun)
def numberOfPositionDeterminerNoun(trigrams):
  return len([a for a,b,c in trigrams if a=="P" and b=="D" and c =="N"])

#the number of appearaces of a pos bigram (Adjective,Noun)
def numberOfAdjectiveNoun(bigrams):
    return len([b for b,t in bigrams if b=="A" and t=="N"])
	
#the number of appearaces of a pos bigram (Verb,Verb)
def numberOfVerbVerb(bigrams):
    return len([b for b,t in bigrams if b=="V" and t=="V"])

#the number of appearaces of a pos bigram (Noun,Verb)
def numberOfNounVerb(bigrams): 
   return len([b for b,t in bigrams if b=="N" and t=="V"])

#the number of appearaces of a pos bigram (Adverb,Adverb)
def numberOfVerbAdverb(bigrams):
    return len([b for b,t in bigrams if b=="V" and t=="R"])

#the number of appearaces of a pos bigram (Adverb,Verb)
def numberOfAdverbVerb(bigrams):
    return len([b for b,t in bigrams if b=="R" and t=="V"])

#the number of appearaces of a pos bigram (Pronoun,Verb)
def numberOfPronounVerb(bigrams):
  return len([b for b,t in bigrams if b=="O" and t=="V"])
