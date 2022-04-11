import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn import svm


def load_data(training_tweets):
    parties = ["Democratic","Republican"]
    df = pd.read_csv(training_tweets)
    df = df[['text', 'party']]
    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(df['text'], df['party'], test_size=0.2)

    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Train_Y)
    Test_Y = Encoder.fit_transform(Test_Y)

    return (Train_X, Test_X, Train_Y, Test_Y)


def train_svm(Train_X, Test_X, Train_Y, Test_Y):
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    SVM.fit(Train_X, Train_Y)
    return SVM


if __name__ == "__main__":
    training_file = "tweets.csv"
    (Train_X, Test_X, Train_Y, Test_Y) = load_data(training_file)
    clf = train_svm((Train_X, Test_X, Train_Y, Test_Y))


