#read .tsv file and return labels and messages as lists
def opentsv(filepath):
    #initialize lists
    ids = []
    labels=[]
    messages=[]
    
	#open file
    data = open(filepath,'r')

	#read file
    for line in data.readlines():
        try:
            line = line.decode('utf8')
        except:
            line = unicode(line, errors='replace')
            
        l = len(line.split("\t"))
		#check if the file has 3 or 4 columns
        if l==4:
            labels.append(line.split("\t")[2])
            message=line.split("\t")[3]
            messages.append(message)
        elif l==3:
            labels.append(line.split("\t")[1])
            message=line.split("\t")[2]
            messages.append(message)
			
        ids.append(line.split("\t")[0])
        
    data.close()

    return ids,labels,messages