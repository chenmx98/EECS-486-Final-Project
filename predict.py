import pandas as pd
import numpy as np
import sklearn
import json
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn import svm

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


def train_svm():
    dem_text = open("data/train/dem_terms.txt",'r').read().split(" ")
    rep_text = open("data/train/rep_terms.txt",'r').read().split(" ")



    # print(np.array(dem_text).shape)

    dem_arr = np.vstack((np.array(dem_text), np.zeros_like(np.array(dem_text))))
    rep_arr = np.vstack((np.array(rep_text), np.ones_like(np.array(rep_text))))
    train_list = np.hstack((dem_arr, rep_arr))

    print(train_list.shape)

    Train_X = train_list[0]
    Train_Y = train_list[1]

    Tfidf_vect = TfidfVectorizer()
    Tfidf_vect.fit(Train_X)

    Train_X_Tfidf = Tfidf_vect.transform(Train_X)


    print(Train_X_Tfidf.shape, Train_Y.shape)
    print("Training SVM")

    clf = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')

    clf.fit(Train_X_Tfidf, Train_Y)
    print("Training Complete!")
    return clf,Tfidf_vect

def predict(clf,vectorizer, test_str):
    print("Predicting")
    Test_X = vectorizer.transform(test_str)
    print(Test_X.shape)
    res = clf.predict(Test_X)
    return res


# if __name__ == "__main__":



