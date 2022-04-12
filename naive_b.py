# Name:Zhongxing Zhou Unique name:ryanzhou
import sys
import os
import math
from preprocess import tokenizeText, removeSGML
folder_name = ""

# a. Function that trains a Naive Bayes classifier:
# name: trainNaiveBayes;
# input: the list of file paths to be used for training;
# output: data structure with class probabilities (or log of probabilities);
# output: data structure with word conditional probabilities (or log of probabilities);
# output: any other parameters required (e.g., vocabulary size).
def trainNaiveBayes(file_path):
    global folder_name
    # fake, true, total
    class_probability = [0,0,0]
    word_occurance = {}
    word_occurance_fake = {}
    word_occurance_true = {}
    word_conditional_fake = {}
    word_conditional_true = {}
    for file in file_path:
        with open(folder_name + file, encoding="ISO-8859-1") as infile:
        # with open(folder_name + file, encoding='utf8', errors='ignore') as infile:
            if file[:4] == "fake":
                class_probability[0] += 1
            if file[:4] == "true":
                class_probability[1] += 1
            class_probability[2] += 1
            Lines = infile.readlines()
            Lines = removeSGML(Lines)
            after_process = tokenizeText(Lines)
            for word in after_process:
                if word not in word_occurance:
                    word_occurance[word] = 1
                else:
                    word_occurance[word] += 1
                if file[:4] == "fake":
                    if word not in word_occurance_fake:
                        word_occurance_fake[word] = 1
                    else:
                        word_occurance_fake[word] += 1
                if file[:4] == "true":
                    if word not in word_occurance_true:
                        word_occurance_true[word] = 1
                    else:
                        word_occurance_true[word] += 1
    class_probability[0] = math.log(class_probability[0] / class_probability[2])
    class_probability[1] = math.log(class_probability[1] / class_probability[2])
    vocab_size = len(word_occurance)
    for word in word_occurance:
        if word in word_occurance_fake:
            word_fake = word_occurance_fake[word]
        else:
            word_fake = 0
        word_conditional_fake[word] = math.log((word_fake + 1) / (len(word_occurance_fake) + vocab_size))
        if word in word_occurance_true:
            word_true = word_occurance_true[word]
        else:
            word_true = 0
        word_conditional_true[word] = math.log((word_true + 1) / (len(word_occurance_true) + vocab_size))
    return class_probability, word_conditional_fake, word_conditional_true, vocab_size, len(word_occurance_fake), len(word_occurance_true)

# Function that predicts the class (true or fake) of a previously unseen document:
# name: testNaiveBayes;
# input: the file path to be used for test;
# input: the output produced by trainNaiveBayes;
# output: predicted class (the string “true” or the string “fake”. You can assume these to be the
# only classes to be predicted)
# The tokens that are not in the vocabulary should have smoothing applied.
def testNaiveBayes(test_file, class_probability, word_conditional_fake, word_conditional_true, vocab_size, lf, lt):
    global folder_name
    true_prob = class_probability[1]
    fake_prob = class_probability[0]
    with open(folder_name + test_file, encoding="ISO-8859-1") as infile:
        Lines = infile.readlines()
        Lines = removeSGML(Lines)
        after_process = tokenizeText(Lines)
        for word in after_process:
            if word in word_conditional_fake:
                fake_prob += word_conditional_fake[word]
            else:
                fake_prob += math.log(1 / (lf + vocab_size))
            if word in word_conditional_true:
                true_prob += word_conditional_true[word]
            else:
                true_prob += math.log(1 / (lt + vocab_size))

    if fake_prob > true_prob:
        return "fake"
    else:
        return "true"






def main():
    global folder_name
    folder_name = sys.argv[1]
    all_file = os.listdir(folder_name)
    accuracy = 0

    with open("naivebayes.output." + folder_name[:-1], 'w') as out:
        for i in range(len(all_file)):
            test_file = all_file[i]
            train_file = all_file[:i] + all_file[i + 1:]
            class_probability, word_conditional_fake, word_conditional_true, vocab_size, lf, lt = trainNaiveBayes(train_file)
            result = testNaiveBayes(test_file, class_probability, word_conditional_fake, word_conditional_true, vocab_size, lf, lt)
            wcf = dict(sorted(word_conditional_fake.items(), key=lambda x: x[1], reverse=True)[:10])
            wct = dict(sorted(word_conditional_true.items(), key=lambda x: x[1], reverse=True)[:10])

            # for x, y in wcf.items():
            #     print(x + " " + str(y))
            # print("true")
            # for x, y in wct.items():
            #     print(x + " " + str(y))

            if result == test_file[:4]:
                accuracy += 1
            out.write(test_file + " " + result + '\n')
    print(accuracy / len(all_file))






if __name__ == '__main__':
    main()