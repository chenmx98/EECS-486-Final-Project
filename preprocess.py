# Name: Yuhong Chen
# Unique Name: yuhchen

import os
import re
import sys
import string

# code from https://tartarus.org/martin/PorterStemmer/python.txt
from stemmer import PorterStemmer

def removeSGML(str):
    """Remove SGML tags and return result string"""
    return re.sub('<.*?>', '', str)

def decontraction(str):
    """
    Decontract some common phrases in English.
    Input: a token
    Output: decontraction form of the token, and if decontraction is successful
    """
    original = str
    str = re.sub(r"won\'t", "will not", str)
    str = re.sub(r"can\'t", "can not", str)
    str = re.sub(r"n\'t", " not", str)
    str = re.sub(r"\'re", " are", str)
    str = re.sub(r"\'s", " is", str)
    str = re.sub(r"\'d", " would", str)
    str = re.sub(r"\'t", " not", str)
    str = re.sub(r"\'ve", " have", str)
    str = re.sub(r"\'m", " am", str)
    return str, original != str

def processPunctuation(token, searchResult, resultList):
    """
    Process different punctuation respectively for tokenization.
    Input: a token, iterator of punctuation match, list of token processed
    output: None
    """
    tempList = []
    counter = 0
    for match in searchResult:
        start = match.start()
        end = match.end()
        punctuation = token[start:end]
        if punctuation == '.':
            # if first letter is not capitalized and is not surrounded by numbers
            if (not token[0].isupper() and end == len(token)) or \
               (end < len(token) and not token[end].isnumeric()) or (start > 0 and not token[start-1].isnumeric()):
                # identify words like n.y. with multiple period as abbreviation
                furtherMatch = re.search('\.', token[end:])
                if furtherMatch is not None and furtherMatch.start() > 0:
                    break
                # if token does not meet any criterions of abbreviation stuff, split it
                tempList.append(token[counter:start])
                tempList.append(token[start:end])
                counter = end
        elif punctuation == ',' or punctuation == '/':
            # if it is not surrounded by numbers, then we can split it
            if start == 0 or not token[start-1].isnumeric() or end == len(token) or not token[end].isnumeric():
                tempList.append(token[counter:start])
                tempList.append(token[start:end])
                counter = end
        elif punctuation == "'":
            # attempt to decontract the token
            str, changed = decontraction(token[start:])
            # if changes are done, combine result into list
            if changed:
                str = str.strip()
                tempList.extend(str.split(" "))
            # if no changes are done, split the punctuation
            else:
                tempList.append(token[counter:start])
                tempList.append(token[start:end])
            counter = end
        # make sure words with - stay connect
        elif punctuation == "-":
            continue
        # separate all other punctuations
        else:
            tempList.append(token[counter:start])
            tempList.append(token[start:end])
            counter = end
    # combine result of tokenization on current token to final list
    tempList.append(token[counter:])
    tempList = [i for i in tempList if i]
    resultList.extend(tempList)
    return

def tokenizeText(str):
    """Tokenize texts and return list of tokens"""
    tokens = str.split(" ")
    result = []
    for token in tokens:
        # for each tokens, find punctuation in it and process based on search result
        searchResult = re.finditer(f"[{string.punctuation}]", token)
        processPunctuation(token, searchResult, result)
    return result

def removeStopWords(tokenizedWords):
    """Remove all stop words from tokenizedWords"""
    # find all words need to be removed based on stopword file
    WordsToRemove = []
    with open("stopwords", 'r') as stopwords_file:
        stopwords = stopwords_file.read().splitlines()
        for word in tokenizedWords:
            if word.lower() in stopwords:
                WordsToRemove.append(word)

    # remove all these words from list
    for word in WordsToRemove:
        try:
            while True:
                tokenizedWords.remove(word)
        except:
            pass
    return tokenizedWords

def stemWord(tokenizedWords):
    """Stem all words in tokenizedWords"""
    ps = PorterStemmer()
    for index, word in enumerate(tokenizedWords):
        tokenizedWords[index] = ps.stem(word, 0, len(word)-1)
    return tokenizedWords

if __name__ == '__main__':
    totalWords = 0
    finalMap = {}
    for filename in os.listdir(f"{sys.argv[1]}/"):
        # process each file in cranfieldDocs independently
        filename = f"{sys.argv[1]}/{filename}"
        with open(filename, 'r') as file:
            tokenization = ""
            for line in file.read().splitlines():
                tokenization += " " + removeSGML(line)
            tokenization = tokenizeText(tokenization)
            tokenization = removeStopWords(tokenization)
            tokenization = stemWord(tokenization)
            
            # count the number of words and word occurrences
            for word in tokenization:
                if word not in string.punctuation:
                    totalWords += 1
                    if word not in finalMap.keys():
                        finalMap[word] = 1
                    else:
                        finalMap[word] += 1
    # sort the map based on values
    finalMap = sorted(finalMap.items(), key=lambda x: x[1], reverse=True)

    # print all data into the output file
    with open("preprocess.output", "w+") as output:
        output.write(f"Word {totalWords}\n")
        output.write(f"Vocabulary {len(finalMap)}\n")
        output.write("Top 50 words\n")

        counter = 0
        for word, frequency in finalMap:
            if counter < 50:
                output.write(f"{word} {frequency}\n")
                counter += 1
            else:
                break

    """
    # this calculate number of words account for 25% of total number of words
    counter = 0
    numWord = 0
    threshold = int(totalWords * 0.25)
    for word, frequency in finalMap:
        counter += frequency
        numWord += 1
        if counter >= threshold:
            print(f"we need at least {numWord} words\n")
            break
    """

    """
    # this calculate the number of words and vocabulary for each 300 files in cranfieldDocs
    totalWords = 0
    vocabMap = {}
    threshold = 300
    for filename in os.listdir("cranfieldDocs/"):
        # process each file in cranfieldDocs independently
        filename = f"cranfieldDocs/{filename}"
        with open(filename, 'r') as file:
            tokenization = ""
            for line in file.read().splitlines():
                tokenization += " " + removeSGML(line)
            tokenization = tokenizeText(tokenization)
            tokenization = removeStopWords(tokenization)
            tokenization = stemWord(tokenization)
            
            # count the number of words and frequency
            for word in tokenization:
                if word not in string.punctuation:
                    totalWords += 1
                    if word not in vocabMap.keys():
                        vocabMap[word] = 1
                    else:
                        vocabMap[word] += 1

        # if we processed 300 files, report it and start again with next 300 files
        threshold -= 1
        if threshold == 0:
            print(f"Total words are {totalWords}, number of vocabulary is {len(vocabMap)}.")
            vocabMap.clear()
            totalWords = 0
            threshold = 300
    """