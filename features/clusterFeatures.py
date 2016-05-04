#check if a word of the message appears in a cluster
def checkClusters(tokens,clusters):  
    #initialize list with zeros
    tags = [0] * len(clusters.keys)

    c = []
    for token in tokens:
        c.append(clusters.d.get(token,"no_cluster"))

    c = [x for x in c if x!="no_cluster"] 

    for i in c:
        tags[clusters.keys.index(i)] = 1
    
    return tags