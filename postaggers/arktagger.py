import subprocess
import os
from os import remove,system

#postagger directory
directory = "postaggers/"
#jar path
jar_path = "ark-tweet-nlp-0.3.2/"
#jar name
jar_name = "ark-tweet-nlp-0.3.2.jar"
#file name
file_name = "tweet.txt"

#the command which is going to be executed
command = "java -Xmx500m -jar "+directory+jar_path+jar_name+" "+directory+file_name

#write a message to a file
def messageToFile(message):
    text_file = open(directory+file_name, "w")
    text_file.write(message.encode("utf-8"))
    text_file.close()

#write a message list to a file
def listToFile(messages):
    text_file = open(directory+file_name,"w")
    for m in messages:
        text_file.write(m.encode("utf-8"))
    text_file.close()

#load a file to a list
def fileToList(path):
    tags = []
    data = open(path,"r")
    for line in data:
        tags.append(line.split("\t")[1].split(" "))
    return tags    

#call java library in order to find the pos tags of the message
#pos tag for only one message
def pos_tag_message(message):

    #create temporary text file with the message
    messageToFile(message)
        
    #use the text file as input to the pos tagger and get output
    result = subprocess.check_output(command,shell=True)

    print type(result)

    #get tokens
    tokens = result.split("\t")[1].split(" ")

    #delete temporary text file
    remove(directory+file_name)

    return tokens

#pos tag for a list of messages
def pos_tag_list(messages):

    #create temporary text file with the messages
    listToFile(messages)

    #use the text file as input to the pos tagger and get output
    #system(command+" >"+directory+"out.txt")
	
    devnull = open(os.devnull,'w')
                
    with open(directory+"out.txt", 'w') as output:
        subprocess.check_call(command, stdout=output, stderr=devnull,shell=True)
		 
    #read file to list
    results = fileToList(directory+"out.txt")
	
    devnull.close()
	
    #delete temporary text files
    remove(directory+file_name)
    remove(directory+"out.txt")
	
    return results
