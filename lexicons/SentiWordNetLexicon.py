from nltk.corpus import sentiwordnet as s

#SentiWordNet Lexicon
class SentiWordNetLexicon():

    #empty constructor
    def __init__(self,Average):

        #set to True if we want the average scores of all words POS Tags
        self.average = Average

    #compute score of message
    def score(self,tokens,pos_tags):
        total = 0.0
    
        for i in range(0,len(pos_tags)) :
            #find word sentiment score
            try:
                total += self.findSentiment(tokens[i],pos_tags[i])
            except:
                pass

        return total

    #find word's sentiment score
    def findSentiment(self,token,pos_tag):
        #find average score for alla pos tags
        if self.average:
            synsets = s.senti_synsets(token)
        else: #find score for specific pos tag
            try:
                synsets = s.senti_synsets(token,pos_tag.lower())
            except:
                #catch, if an error occures(if there is not such a pos tag)
                synsets = s.senti_synsets(token)

        if len(synsets)>0 :
            #calculate score for all sentimens(neutral,positive,negative)
            neutral = 0
            positive = 0
            negative = 0

            #average score of all synsets (allagi an vrethei kaliteros tropos)
            for synset in synsets:
                neutral += synset.obj_score()
                positive += synset.pos_score()
                negative += synset.neg_score()

            neutral = neutral/float(len(synsets))
            positive = positive/float(len(synsets))
            negative = negative/float(len(synsets))

            #return sentiment with max score
            if max(neutral,positive,negative) == neutral :
                return neutral
            elif max(neutral,positive,negative) == positive :
                return positive
            else:
                return negative

        else:
            return 0

    #compute the number of tokens(words) that appear in the lexicon
    def getNumberOfAppearances(self,tokens):
        total = 0
        for token in tokens:
            if len(s.senti_synsets(token)) > 0:
                total += 1

        return total