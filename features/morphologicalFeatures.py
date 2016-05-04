import re

#return 1 if the sentence contains an elongated token
#return 0 otherwise
def hasElongatedWords(sentence):
    elong = re.compile("([a-zA-Z])\\1{2,}")
    if bool(elong.search(sentence)):
        return 1
    else:	
        return 0

#find the number of elongated tokens im message
def numberOfElongatedWords(sentence):
    elong = re.compile("([a-zA-Z])\\1{2,}")
    return len([word for word in sentence.split() if elong.search(word)])


#check if the sentence has a time expression
def hasTimeExpressions(sentence):

    #pattern - 12:00 pm
    p1 = re.compile(r"\d{1,2}:\d{1,2}.(AM|am|PM|pm|Pm|Am|a.m.|p.m.|A.M.|P.M.)+")

    #pattern - 12.00 pm
    p2 = re.compile(r"\d{1,2}\.\d{1,2}.(AM|am|PM|pm|Pm|Am|a.m.|p.m.|A.M.|P.M.)+")

    #pattern - 12 pm
    p3 = re.compile(r"\d{1,2}.(AM|am|PM|pm|Pm|Am|a.m.|p.m.|A.M.|P.M.)+")

    #pattern - at 12 o'clock
    p4 = re.compile(r"at \d{1,2} o'clock")

    if (bool(p1.search(sentence)) or bool(p2.search(sentence)) or bool(p3.search(sentence)) or bool(p4.search(sentence))):
        return 1
    else:
        return 0

#check if the sentence has a date expression
def hasDateExpressions(sentence):

    #pattern - 16/12/1985
    p1 = re.compile(r"\d{1,2}/\d{1,2}/\d{4}")

    #pattern - 16-12-1985
    p2 = re.compile(r"\d{1,2}-\d{1,2}-\d{4}")

    #pattern - 16.12.1985
    p3 = re.compile(r"\d{1,2}.\d{1,2}.\d{4}")

    #pattern - 16/12
    p4 = re.compile(r"\d{1,2}/\d{1,2}")

    #pattern - 16-12
    p5 = re.compile(r"\d{1,2}-\d{1,2}")

    #pattern - 16.12
    p6 = re.compile(r"\d{1,2}.\d{1,2}")

    #pattern - 15(or 15th etc) of December
    p7 = re.compile(r"\d{1,2}(st|th|nd|rd)* of (Jan|jan|Feb|feb|Mar|mar|Apr|apr|May|may|June|june|July|july|Aug|aug|Sep|sep|Oct|oct|Nov|nov|Dec|dec)+")

    #name of day
    p8 = re.compile(r"(Monday|monday|Tuesday|tuesday|Wednesday|wednesday|Thursday|thursday|Friday|friday|Saturday|saturday|Sunday|sunday)")
    
    #month day 
    p9 = re.compile(r"(Jan|jan|Feb|feb|Mar|mar|Apr|apr|May|may|June|june|July|july|Aug|aug|Sep|sep|Oct|oct|Nov|nov|Dec|dec) \d{1,2}(st|th|nd|rd)*")

    #return if the sentence match a pattern
    if (bool(p1.search(sentence)) or bool(p2.search(sentence)) or bool(p3.search(sentence)) or bool(p4.search(sentence)) or bool(p5.search(sentence)) or bool(p6.search(sentence)) or bool(p7.search(sentence)) or bool(p8.search(sentence)) or bool(p9.search(sentence))):
        return 1
    else:
        return 0                 

#compute the number of tokens of the message that are fully capitalized
def countFullyCapitalizeTokens(tokens):
    #return len([word for word in tokens if word=="<allcaps>"])
    return len([word for word in tokens if word.isupper()])

#compute the number of tokens of the message that are partially capitalized    
def countPartiallyCapitalizeTokens(tokens):
    return len([word for word in tokens if (any(x.isupper() for x in word) and any(y.islower() for y in word))])

#compute the number of tokens that start with upper case letter
def countUpper(tokens):
    return len([word for word in tokens if word[0].isupper()])

#compute the number of exclamation marks in the message
def countExclamationMarks(message):
    return message.count("!")

#compute the number of question marks
def countQuestionMarks(message):
    return message.count("?")

#the number of tokens containing only exclamation marks
def onlyQuestionMarks(tokens):
    x = 0
    for token in tokens:
        if token.count("?") == len(token):
            x+=1

    return x

#the number of tokens containing only exclamation marks
def onlyExclamationMarks(tokens):
    x = 0
    for token in tokens:
        if token.count("!") == len(token):
            x+=1

    return x

#the number of tokens containing only exclamation marks
def onlyQuestionOrExclamationMarks(tokens):
    x = 0
    for token in tokens:
        if (token.count("?") + token.count("!")) == len(token):
            x+=1

    return x

#compute the number of tokens containing only ellipsis (...)
def countEllipsis(tokens):
    return len([word for word in tokens if word=="..."])

#check the existence of a subjective emoticon at the message's end
def hasEmoticonAtEnd(last_token,last_tag):
    if (last_tag=="E" or last_token=="<sadface>" or last_token=="<smile>"):
        return 1
    else:
        return 0

#check the existence of an ellipsis and a link (URL) at the message's end
def hasUrlOrEllipsisAtEnd(last_token,last_tag):
    if(last_tag=="U" or last_token=="..." or last_token=="<url>"):
        return 1
    else:
        return 0

#check the existence of an exclamation mark at the message's end
def hasExclamationMarkAtEnd(last_token):
    if "!" in last_token:
        return 1
    else:
        return 0

#check the existence of a question mark at the message's end
def hasQuestionMarkAtEnd(last_token):
    if "?" in last_token:
        return 1
    else:
        return 0

#check the existence of a question or an exclamation mark at the message's end
def hasQuestionOrExclamationMarkAtEnd(last_token):
    if ("?" in last_token) or ("!" in last_token):
        return 1
    else:
        return 0

#check the existence of slang
def hasSlang(tokens,slangDictionary):
    for token in tokens:
        if slangDictionary.isSlang(token):
            return 1

    return 0
