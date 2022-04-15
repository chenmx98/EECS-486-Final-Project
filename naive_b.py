# Name:Zhongxing Zhou Unique name:ryanzhou
import sys
import os
import math
import pandas as pd
from jw import process_tweets
from evaluation import process_validation
from preprocess import tokenizeText, removeSGML
folder_name = ""
train_folder_name = ""

# a. Function that trains a Naive Bayes classifier:
# name: trainNaiveBayes;
# input: the list of file paths to be used for training;
# output: data structure with class probabilities (or log of probabilities);
# output: data structure with word conditional probabilities (or log of probabilities);
# output: any other parameters required (e.g., vocabulary size).
def trainNaiveBayes(file_path):
    global folder_name
    global train_folder_name
    # fake, true, total
    class_probability = [0,0,0]
    word_occurance = {}
    word_occurance_dem = {}
    word_occurance_rep = {}
    word_conditional_dem = {}
    word_conditional_rep = {}
    for file in file_path:
        with open(train_folder_name + '/' + file, encoding="ISO-8859-1") as infile:
        # with open(folder_name + file, encoding='utf8', errors='ignore') as infile:
            if file[:3] == "Dem":
                class_probability[0] += 1
            if file[:3] == "Rep":
                class_probability[1] += 1
            class_probability[2] += 1
            Lines = infile.readlines()
            for w in Lines:
                ww = w.split()
                for word in ww:
                    if word not in word_occurance:
                        word_occurance[word] = 1
                    else:
                        word_occurance[word] += 1
                    if file[:3] == "Dem":
                        if word not in word_occurance_dem:
                            word_occurance_dem[word] = 1
                        else:
                            word_occurance_dem[word] += 1
                    if file[:3] == "Rep":
                        if word not in word_occurance_rep:
                            word_occurance_rep[word] = 1
                        else:
                            word_occurance_rep[word] += 1
    class_probability[0] = math.log(class_probability[0] / class_probability[2])
    class_probability[1] = math.log(class_probability[1] / class_probability[2])
    vocab_size = len(word_occurance)
    for word in word_occurance:
        if word in word_occurance_dem:
            word_dem = word_occurance_dem[word]
        else:
            word_dem = 0
        word_conditional_dem[word] = math.log((word_dem + 1) / (len(word_occurance_dem) + vocab_size))
        if word in word_occurance_rep:
            word_rep = word_occurance_rep[word]
        else:
            word_rep = 0
        word_conditional_rep[word] = math.log((word_rep + 1) / (len(word_occurance_rep) + vocab_size))
    return class_probability, word_conditional_dem, word_conditional_rep, vocab_size, len(word_occurance_dem), len(word_occurance_rep)

# Function that predicts the class (true or fake) of a previously unseen document:
# name: testNaiveBayes;
# input: the file path to be used for test;
# input: the output produced by trainNaiveBayes;
# output: predicted class (the string “true” or the string “fake”. You can assume these to be the
# only classes to be predicted)
# The tokens that are not in the vocabulary should have smoothing applied.
def testNaiveBayes(word_county, class_probability, word_conditional_dem, word_conditional_rep, vocab_size, lf, lt):
    global folder_name
    rep_prob = class_probability[1]
    dem_prob = class_probability[0]
    # print(len(word_conditional_dem))
    dem_or_rep = {}
    for county in word_county:
        for word in county:
            if word in word_conditional_dem:

                dem_prob += word_conditional_dem[word]
            else:
                dem_prob += math.log(1 / (lf + vocab_size))
            if word in word_conditional_rep:
                rep_prob += word_conditional_rep[word]
            else:
                rep_prob += math.log(1 / (lt + vocab_size))
        # print(dem_prob)
        # print(rep_prob)
        if dem_prob > rep_prob:
            dem_or_rep[county] = "0"
        else:
            dem_or_rep[county] = "1"
    return dem_or_rep




def main():
    global folder_name
    global train_folder_name
    # folder_name = sys.argv[1]
    train_folder_name = "Debate2020"
    all_train_file = os.listdir(train_folder_name)
    accuracy = 0
    class_probability, word_conditional_dem, word_conditional_rep, vocab_size, lf, lt = trainNaiveBayes(all_train_file)
    # df = pd.read_csv("US_tweets_county.csv")
    # # count = 0
    # words_county = {}
    # for i in range(len(df)):
    #     tweet_token = process_tweets(df.loc[i, 'Text'][2:])
    #     if df.loc[i, 'County'] in words_county:
    #         words_county[df.loc[i, 'County']] += tweet_token
    #     else:
    #         words_county[df.loc[i, 'County']] = tweet_token
    # # print(words_county)
    words_county = {}
    with open("token_with_fip.txt") as input:
        lines = input.readlines()
        for line in lines:
            line = line.rstrip()
            line = line.split()
            line[0] = line[0][:-2]
            words_county[line[0]] = line[1:]
    result = testNaiveBayes(words_county, class_probability, word_conditional_dem, word_conditional_rep, vocab_size, lf,
                            lt)
    # print(result)
    # print(process_validation(result))
    with open("data/result/" + 'naive_result','w') as out:
        for i in result:
            out.write(i + ' ' + result[i] + '\n')



    # for i in range(len(all_file)):
    #     test_file = all_file[i]
    #     train_file = all_file[:i] + all_file[i + 1:]
    #     class_probability, word_conditional_fake, word_conditional_true, vocab_size, lf, lt = trainNaiveBayes(train_file)
    #     result = testNaiveBayes(test_file, class_probability, word_conditional_fake, word_conditional_true, vocab_size, lf, lt)
    #     wcf = dict(sorted(word_conditional_fake.items(), key=lambda x: x[1], reverse=True)[:10])
    #     wct = dict(sorted(word_conditional_true.items(), key=lambda x: x[1], reverse=True)[:10])
    #
    #
    #         if result == test_file[:4]:
    #             accuracy += 1
    #
    # print(accuracy / len(all_file))






if __name__ == '__main__':
    main()