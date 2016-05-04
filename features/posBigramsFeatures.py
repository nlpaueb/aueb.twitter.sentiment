#return avg,min,max F1 scores of pos tags
def F1PosTagsScore(pos,pos_tags_scores):
    scores = []

    for x in pos:
        scores.append(pos_tags_scores.get(x,0))
        
    try:
        average = sum(scores)/float(len(scores))
    except:
        average=0
    try:
        maximum = max(scores)
    except:
        maximum = 0
    try:
        minimum = min(scores)
    except:
        minimum = 0

    
    return average, maximum, minimum

#return avg,min,max F1 scores of pos bigrams
def F1PosBigramsScore(pos,pos_bigrams_scores):
    scores = []

   
    for x in pos:
        scores.append(pos_bigrams_scores.get(x,0))

    try:
        average = sum(scores)/float(len(scores))
    except:
        average=0
    try:
        maximum = max(scores)
    except:
        maximum = 0
    try:
        minimum = min(scores)
    except:
        minimum = 0

        
    return average, maximum, minimum

#return avg,min,max F1 scores of pos trigrams
def F1PosTrigramsScore(pos,pos_trigrams_scores):
    scores = []

    for x in pos:
        scores.append(pos_trigrams_scores.get(x,0))

    try:
        average = sum(scores)/float(len(scores))
    except:
        average=0
        
    try:
        maximum = max(scores)
    except:
        maximum = 0
    try:
        minimum = min(scores)
    except:
        minimum = 0

    return average, maximum, minimum
