#Minqing Hu Lexicon
class MinqingHuLexicon():
    
    #lexicon directory
    directory = "lexicons/Minqing Hu/"

    #lexicon files
    file1="negative-words.txt"
    file2="positive-words.txt"

    #ignore char
    ignore = ";"

    #constructor
    def __init__(self):
        #initialize dictionary
        self.d = {}
        #load Lexicon
        self.loadLexicon()

    #load a lexicon file with a predetermined score
    def loadLexiconFile(self,filename,score):
        f = open(MinqingHuLexicon.directory+filename,"r")

        for line in f.readlines():
            if (not line.startswith(MinqingHuLexicon.ignore)):
                key = line.strip()
                self.d[key]=score

        f.close()

    #load Minqing Hu Lexicon
    def loadLexicon(self):
        #load negative sentiment lexicon with score -1
        self.loadLexiconFile(MinqingHuLexicon.file1,-1.0)
        #load positive sentiment lexicon with score +1
        self.loadLexiconFile(MinqingHuLexicon.file2,1.0)

    #compute score of a message
    def score(self,tokens):
        total = 0.0
        for token in tokens:
            total += self.d.get(token,0.0)
            
        return total

    #polarity
    def polarity(self,tokens):
        s = abs(self.score(tokens))
        if s<=1:
            return 0
        else:
            return 1

    #compute the number of tokens(words) that appear in the lexicon
    def getNumberOfAppearances(self,tokens):
        total = 0
        for token in tokens:
            if self.d.has_key(token):
                total+=1

        return total