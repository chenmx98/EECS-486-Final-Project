import pandas as pd
import numpy as np
import sklearn
import json
import csv
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn import svm
from sklearn.metrics import accuracy_score
from tqdm import tqdm

def process_election_result():
    filepath = "data/train/countypres_2000-2020.csv"
    df = pd.read_csv(filepath, usecols=["county_fips", "party", "candidatevotes", "totalvotes"])
    elect_dict = {}
    for i in range(len(df)):
        # print(df.iloc[i])
        fips = df.iloc[i]["county_fips"]
        party = df.iloc[i]["party"]
        if fips not in elect_dict:
            elect_dict[fips] = {}
            elect_dict[fips][party] = 1.0 * df.iloc[i]["candidatevotes"]/df.iloc[i]["totalvotes"]
        else:
            elect_dict[fips][party] = 1.0 * df.iloc[i]["candidatevotes"]/df.iloc[i]["totalvotes"]

    with open("elect_dict.json", "w") as outfile:
        json.dump(elect_dict, outfile, indent=4)


def predict():
    # dem_text = open("data/train/dem_terms.txt",'r').read().split(" ")
    # rep_text = open("data/train/rep_terms.txt",'r').read().split(" ")
    #
    #

    # print(np.array(dem_text).shape)
    # dem_arr = np.vstack((np.array(dem_text), np.zeros_like(np.array(dem_text,dtype=np.int))))
    # rep_arr = np.vstack((np.array(rep_text), np.ones_like(np.array(rep_text,dtype=np.int))))
    # train_list = np.hstack((dem_arr, rep_arr))
    df_train = pd.read_csv("Debate2020/party_transcript.csv", names=["Party","Text"])
    df_pred = pd.read_csv("sentence_fip.csv", names=["FIPS", "Text"])

    # train_arr = df_train["Text"]
    # train_label = df_train["Party"]
    # pred_arr = df_pred["Text"]

    # print(len(train_arr), len(train_label), len(pred_arr))

    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(df_train['Text'], df_train['Party'],
                                                                        test_size=0.2)
    # Train_X = df_train["Text"]
    # Train_Y = df_train["Party"]
    Pred_X = df_pred["Text"]

    Encoder = LabelEncoder()
    Encoder.fit(Train_Y)
    Train_Y = Encoder.transform(Train_Y)
    Test_Y = Encoder.transform(Test_Y)

    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(df_train['Text'])

    Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    Test_X_Tfidf = Tfidf_vect.transform(Test_X)
    Pred_X_Tfidf = Tfidf_vect.transform(Pred_X)
    clf = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    clf.fit(Train_X_Tfidf, Train_Y)
    print("Training Complete!")
    predictions_SVM = clf.predict(Test_X_Tfidf)
    print("SVM Accuracy Score -> ", accuracy_score(predictions_SVM, Test_Y) * 100)

    df_pred["Pred"] = clf.predict(Pred_X_Tfidf)
    print("Predicting complete")
    df_pred.to_csv("Predict_counties.csv")


    print(Train_Y)
    # Tfidf_vect = TfidfVectorizer()
    # Tfidf_vect.fit(train_arr)
    # Train_X_Tfidf = Tfidf_vect.transform(Train_X)


    # print(Train_X_Tfidf.shape, Train_Y.shape)
    # print("Training SVM")
    #
    # clf = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    #
    # clf.fit(Train_X_Tfidf, Train_Y)
    return

# def predict(clf,vectorizer, test_str):
#     print("Predicting")
#     Test_X = vectorizer.transform(test_str)
#     # print(Test_X.shape)
#     res = clf.predict(Test_X)
#     print(res.tolist())
#     res_score = np.linalg.norm(np.array(res))/np.linalg.norm(np.ones_like(res))
#     return res_score


if __name__ == "__main__":

    predict()
    # clf, v = train_svm()
    #
    # testfile = open('token_with_fip.txt', "r")
    #
    # f = open('data/result/pred_SVM_result.csv', 'w', encoding='UTF8')
    # writer = csv.writer(f)
    #
    # print("Predicting")
    #
    # for line in tqdm(testfile.readlines()):
    #     test_arr = line.split(" ")
    #     fips = test_arr[0]
    #     test_arr.pop(0)
    #     res = [fips, predict(clf,v,test_arr)]
    #     writer.writerow(res)

    # for i in testdict.keys():



