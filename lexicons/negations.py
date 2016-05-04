#load negations list
def loadNegations():
    directory = "lexicons/negationsList/"
    file1 = "negations.txt"

    f = open(directory+file1,"r")

    negationsList = []

    for line in f.readlines():
        line = line.decode('utf8')
        negationsList.append(line[0:len(line)-1])
		
    f.close()

    return negationsList