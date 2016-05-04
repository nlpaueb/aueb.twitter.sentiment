#Twitter word clusters
class Clusters():

    #clusters directory
    directory = "clusters/TwitterWordClusters/"

    #clusters file
    file1 = "50mpaths2.txt"

    #constructor
    def __init__(self):
        #initialize dictionary, dictionary represents clusters
        self.d = {}
        self.keys = []

        #load cluster
        self.loadClusters()

    #load Clusters
    def loadClusters(self):
        #open file
        f = open(Clusters.directory+Clusters.file1,"r")
        
        for line in f.readlines():
            line = line.decode('utf8')
            cluster_id = line.split("\t")[0]
            word = line.split("\t")[1]
            
            self.d[word] = cluster_id
        f.close()

        self.keys = list(set(self.d.values()))
