#calculate the number of adjectives in the message
def numberOfAdjectives(pos):
    return len([x for x in pos if x=="A"])

#calculate the number of adverbs
def numberOfAdverbs(pos):
    return len([x for x in pos if x=="R"])

#calculate the number of interjections
def numberOfIntejections(pos):
    return len([x for x in pos if x=="!"])

#calculate the number of verbs
def numberOfVerbs(pos):
    return len([x for x in pos if x=="V"])

#calculate the number of nouns
def numberOfNouns(pos):
    return len([x for x in pos if x=="N"])

#calculate the number of proper nouns
def numberOfProperNouns(pos,tokens):
    x = 0

    for i in range(0,len(pos)):
        try:
            #pos tagger wrongly tags these words as a proper noun
            if pos[i]=="^" and not(tokens[i]=="<user>" or tokens[i]=="<sadface>" or tokens[i]=="<smile>" or tokens[i]=="<url>"):
                x+=1
        except:
            pass

    return x
            

#calculate the number of urls
def numberOfUrls(pos,tokens):
    return (len([x for x in tokens if x=="<url>"]))

#calculate the number of subjective emoticons
def numberOfSubjectiveEmoticons(pos,tokens):
    return (len([x for x in tokens if (x=="<sadface>" or x=="<smile>")]))

#calculate the number of positive emoticons
def numberOfPositiveEmoticons(tokens):
   
    return len([x for x in tokens if x=="<smile>"])

#calculate the number of neutral emoticons
def numberOfNeutralEmoticons(tokens):
    
    return len([x for x in tokens if x=="<neutralface>"])

#calculate the number of negative emoticons
def numberOfNegativeEmoticons(tokens):

   return len([x for x in tokens if x=="<sadface>"])
