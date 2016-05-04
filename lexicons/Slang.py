#Slang Dictionary
class Slang():

    #dictionary directory
    directory = "lexicons/SlangDictionary/"

    #dictionary file
    file1 = "slangDict.txt"

    #constructor
    def __init__(self):
        #initialize dictionary
        self.d = {}

        #load Slang Dictionary
        self.loadDictionary()

    #load Slang Dictionary
    def loadDictionary(self):
        f = open(Slang.directory+Slang.file1,"r")

        for line in f.readlines():
            line = line.decode('utf8')
            slang_word = line.split("\t")[0]
            word = line.split("\t")[1]
            #remove "\n" char 
            word = word[0:(len(word)-1)]

            self.d[slang_word] = word

        f.close()

    #check if a word is in Slang Dictionary
    def isSlang(self,word):
        return self.d.has_key(word)

    def replaceSlang(self,slang):
        return self.d[slang]   