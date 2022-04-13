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
    df = pd.DataFrame(columns=["party", "terms"], index=['dem', 'rep'])
    df.loc["dem"] = pd.Series({"party":"dem","terms": dem_text})
    df.loc["rep"] = pd.Series({"party":"rep","terms": rep_text})
    Train_X = df['terms']
    Train_Y = df['party']
    Encoder = LabelEncoder()
    Encoder.fit(Train_Y)
    Train_Y = Encoder.transform(Train_Y)
    # Tfidf_vect = TfidfVectorizer(max_features=5000)
    # Tfidf_vect.fit(df['terms'])
    # Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    clf = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    clf.fit(Train_X, Train_Y)

    return clf

def predict(clf, test_str):
    vectorizer = TfidfVectorizer()
    Test_X = vectorizer.fit_transform(test_str)
    res = clf.predict(Test_X)
    return res


# if __name__ == "__main__":



