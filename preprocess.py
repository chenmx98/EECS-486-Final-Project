# Chenming Xing
# chenminx 69022952
import re
import sys
import os
import string
from stem import PorterStemmer
# from tqdm import tqdm

# regex to remove contents in <>
REMOVETAG = re.compile('<.*?>')

# list of stop words
STOPWORD = list()
f = open("stopwords",'r')
for word in f.readlines():
    STOPWORD.append(word[:-1])

# List of common English contractions
# Source: https://en.wikipedia.org/wiki/Wikipedia%3aList_of_English_contractions
contractions = {
"a'ight ": "alright",
"ain't ": "am not",
"amn't": "am not",
"arencha ": "are not you",
"aren't": "are not",
"‘bout ": "about",
"can't": "cannot",
"cap’n ": "captain",
"cause ": "because",
"’cept ": "except",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"cuppa": "cup of",
"dammit ": "damn it",
"daren't": "dare not",
"daresn't": "dare not",
"dasn't": "dare not",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"dunno ": "do not know",
"d'ye ": "do you",
"e'en ": "even",
"e'er ": "ever",
"em ": "them",
"everybody's": "everybody is",
"everyone's": "everyone is",
"fo’c’sle ": "forecastle",
"’gainst ": "against",
"g'day ": "good day",
"gimme ": "give me",
"giv'n ": "given",
"gi'z ": "give us",
"gonna ": "going to",
"gon't ": "go not",
"gotta ": "got to",
"hadn't": "had not",
"had've": "had have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he had",
"he'll": " he will",
"helluva ": "hell of a",
"he's": "he is",
"here's": "here is",
"how'd ": "how did",
"howdy ": "how do you do",
"how'll": "how will",
"how're": "how are",
"how's": "how is",
"i'd": "i would",
"i'd've": "i would have",
"i'd'nt": "i would not",
"i'd'nt've": "i would not have",
"i'll": "i will",
"i'm": "i am",
"imma ": "i am going to",
"i'm'o ": "i am going to",
"innit ": "isn't it",
"ion ": "i do not",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"idunno ": "i do not know",
"kinda ": "kind of",
"let's": "let us",
"ma'am ": "madam",
"mayn't": "may not",
"may've": "may have",
"methinks ": "i think",
"mightn't": "might not",
"might've": "might have",
"mustn't": "must not",
"mustn't've": "must not have",
"must've": "must have",
"‘neath ": "beneath",
"needn't": "need not",
"nal ": "and all",
"ne'er ": "never",
"o'clock": "of the clock",
"o'er": "over",
"ol'": "old",
"oughtn't": "ought not",
"‘round": "around",
"shalln't": "shall not",
"shan't": "shall not",
"she'd": "she had",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've ": "should not have",
"somebody's": "somebody is",
"someone's": "someone is",
"something's": "something is",
"so're ": "so are",
"so’s ": "so is",
"so’ve ": "so have",
"that'll": "that will",
"that're ": "that are",
"that's": "that is",
"that'd": "that had",
"there'd": "there had",
"there'll": "there will",
"there're": "there are",
"there's": "there is",
"these're": "these are",
"these've": "these have",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"this's": "this is",
"those're ": "those are",
"those've ": "those have",
"thout ": "without",
"’til ": "until",
"tis ": "it is",
"to've ": "to have",
"twas ": "it was",
"tween ": "between",
"twere ": "it were",
"wanna": "want to",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"whatcha": "what are you",
"what'd": "what did",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"where'd": "where did",
"where'll": "where will",
"where're": "where are",
"where's": "where is",
"where've": "where have",
"which'd": "which had",
"which'll": "which will",
"which're": "which are",
"which's": "which is",
"which've": "which have",
"who'd": "who would",
"who'd've": "who would have",
"who'll": "who will",
"who're": "who are",
"who's": "who is",
"who've": "who have",
"why'd": "why did",
"why're": "why are",
"why's": "why is",
"willn't": "will not",
"won't": "will not",
"wonnot": "will not",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd've": "you all would have ",
"y'all'd'n't've": "you all would not have ",
"y'all're": "you all are ",
"y'all'ren't": "you all are not ",
"y'at ": "you at",
"yes’m": "yes madam",
"yessir": "yes sir",
"you'd": "you had / you would",
"you'll": "you will",
"you're": "you are",
"you've": "you have",
"when'd": "when did",
"willn't": "will not",
}

numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

def removeSGML(raw_SGML: str) -> str:
    """
    Function that removes the SGML tags.
    :param raw_SGML: string
    :return str: string
    """
    return re.sub(REMOVETAG,'',raw_SGML)

def tokenizeText(raw_text: str) -> list:
    """
    Function that tokenizes the text.
    :param raw_text: string
    :return list: list (of tokens)
    """
    out_list = list()
    words = raw_text.strip().split()
    for word in words:
        curr_word = word.lower()
        # remove , and . and the end of the word
        if word[-1] == "," or word[-1] == ".":
            curr_word = curr_word[:-1]

        if "'" in curr_word:
            if curr_word in contractions:
                curr_word = contractions[curr_word]
            elif curr_word.endswith("'s"):
                curr_word = curr_word[:-2] + ' ' + curr_word[-2:]
            elif curr_word.endswith("s'"):
                curr_word = curr_word[:-1]

        for idx in range(0, len(curr_word)):
            if curr_word[idx] in string.punctuation:
                if curr_word[idx] == '-' or curr_word[idx] == '.':
                    continue
                if idx > 0 and curr_word[idx-1] not in numbers:
                    curr_word = curr_word.replace(curr_word[idx], ' ')

        words = curr_word.split()
        for w in words:
            out_list.append(w)
    return out_list

def removeStopwords(input_list: list) -> list:
    """
    Function that removes the stopwords.
    :param input_list: list (of tokens)
    :return list: list (of tokens)
    """
    out_list = list()
    for word in input_list:
        if word not in STOPWORD:
            out_list.append(word)
    return out_list

def stemWords(input_list: list) -> list:
    """
    Function that stems the words.
    :param input_list: list (of tokens);
    :return list: list (of stemmed tokens)
    """
    p = PorterStemmer()
    out_list = list()
    for word in input_list:
        res = p.stem(word, 0, len(word) - 1)
        out_list.append(res)
    return out_list


def summarize(collection: dict, k=50):
    """
    Function to summarize the collection of tokens
    :param collection: dictionary(k: filename, v: list of tokens)
    :return: total num of words, vocabulary size, most frequent k words (default: 50)
    """
    word_count = 0
    token_dict = dict()
    for list in collection.values():
        for token in list:
            word_count += 1
            if token in token_dict:
                token_dict[token] += 1
            else:
                token_dict[token] = 1

    high_freq_key = sorted(token_dict, key=token_dict.get, reverse=True)[:k]
    out_list = []
    for key in high_freq_key:
        out_list.append((key, token_dict[key]))

    num25 = word_count * 0.25
    num25_count = 0
    num25_words = 0

    # # Save vocabulary as txt
    # f = open("vocabs", 'w')
    # i = 0
    # for v in token_dict.keys():
    #     f.write(v)
    #     f.write(" ")
    #     i+=1
    # print("vocab:",i)
    # f.close()

    for word in sorted(token_dict, key=token_dict.get, reverse=True):
        if num25_count < num25:
            num25_count += token_dict[word]
            num25_words += 1
        else:
            print(num25_words, " words accounts for 25% of the total ", word_count, " words. (", num25, ")")
            break

    return word_count, len(token_dict.keys()), out_list

def process_input(input: str) -> list:
    """
    Process the raw_SGML input, output the list of tokens
    1) removeSGML
    2) tokenizeText
    3) removeStopWords
    4) stemWords
    :param input: raw_SGML
    :return: list of tokens
    """
    raw_text = removeSGML(input)
    word_list = tokenizeText(raw_text)
    word_list = removeStopwords(word_list)
    return stemWords(word_list)

# test sentences
test_1 = "The current population of U.S.A. is 332,087,410 as of Friday, 01/22/2021, based on Worldometer elaboration of the latest United Nations' data."
test_2 = "There're 1,000 good cars by the end of 1/19/2015."
test_3 = "What day's it today? It's Saturday!"

if __name__ == '__main__':
    collection = dict()
    if len(sys.argv) == 1:
        # Default debugging choice
        directory = 'cranfieldDocs/'
        # for filename in tqdm(os.listdir(directory)):
        for filename in os.listdir(directory):
            with open(os.path.join(directory, filename), 'r') as f:
                raw_SGML = f.read()
                collection[filename] = process_input(raw_SGML)
    elif sys.argv[1] == 'f':
        f = open(sys.argv[2],'r')
        collection[sys.argv[2]] = process_input(f.read())
    else:
        directory = sys.argv[1] + '/'
        # for filename in tqdm(os.listdir(directory)):
        for filename in os.listdir(directory):
            with open(os.path.join(directory, filename), 'r') as f:
                raw_SGML = f.read()
                collection[filename] = process_input(raw_SGML)

    word_count, vocab_size, high_freq_list = summarize(collection, 50)
    f = open("preprocess.output", 'w')
    f.write("Words "+ str(word_count) + '\n')
    f.write("Vovabulary " + str(vocab_size) + '\n')
    f.write("Top 50 words\n")

    for word in high_freq_list:
        f.write(word[0]+ " " + str(word[1]) + '\n')
    f.close()

    print("Completed!")
    # Test sentences
    # print(process_input(test_1))
    # print(process_input(test_2))
    # print(process_input(test_3))

    # # Subset of cranfields
    # collection_08 = dict()
    # f_08 = open("cranfieldDocs/cranfield0008",'r')
    # input_08 = f_08.read()
    # collection_08[0] = process_input(input_08)
    # w08, v08, h08 = summarize(collection_08)
    # print("cranfield0008: ")
    # print("Word count: ", w08)
    # print("Vocab size: ", v08)
    #
    # collection_798 = dict()
    # f_798 = open("cranfieldDocs/cranfield0798",'r')
    # input_798 = f_798.read()
    # collection_798[0] = process_input(input_798)
    # w95, v95, h95 = summarize(collection_798)
    # print("cranfield0798: ")
    # print("Word count: ", w95)
    # print("Vocab size: ", v95)


