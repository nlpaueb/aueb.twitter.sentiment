#Socal Lexicon
class SocalLexicon():
    
    #lexicon directory
    directory = "lexicons/SO-CAL/"

    #lexicon files
    file1 = "adj_dictionary1.11.txt"
    file2 = "adv_dictionary1.11.txt"
    file3 = "int_dictionary1.11.txt"
    file4 = "noun_dictionary1.11.txt"
    file5 = "verb_dictionary1.11.txt"
    
    #constructor
    def __init__(self):
        #initialize dictionary
        self.d = {}
        #load Lexicon
        self.loadLexicon()

    #load a lexicon file
    def loadLexiconFile(self,filename):
        f = open(SocalLexicon.directory+filename,"r")

        for line in f.readlines():
            try:
                line = line.decode('utf8')
            except:
                 line = unicode(line, errors='replace')
            key = line.split("\t")[0]
            value = line.split("\t")[1]
            self.d[key]=float(value)

        f.close()

    #load SO-CAL Lexicon        
    def loadLexicon(self):        

        #load lexicons
        self.loadLexiconFile(SocalLexicon.file1)
        self.loadLexiconFile(SocalLexicon.file2)
        self.loadLexiconFile(SocalLexicon.file3)
        self.loadLexiconFile(SocalLexicon.file4)
        self.loadLexiconFile(SocalLexicon.file5)
		
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