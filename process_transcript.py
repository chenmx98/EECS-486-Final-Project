from cmath import nan
from concurrent.futures import process
import geocoder
import requests
from pkg_resources import safe_extra
import tweepy
import sys
import csv
import os
import pandas as pd
import numpy as np
from preprocess_jw import removeSGML, tokenizeText, removeStopwords, stemWords

  
  
def read_text_file(file_path):
    ts = []
    with open(file_path, 'r') as f:
        ts = f.readlines()
    return ts
  
def process_ts(ts):
    dem_ts = []
    rep_ts = []
    dem_words = []
    rep_words = []
    for i in ts:
        # print(i[0])
        if (i[0] == "H" or i[0] == "B"):
            dem_ts.append(i)
        elif(i[0] == "P" or i[0] == "T"):
            rep_ts.append(i)
    

    for text in dem_ts:
        token_ls = tokenizeText(text)
        nsw_token = removeStopwords(token_ls)
        punctuations = '''!()-[]{};:'"\,<>./?@$%^&*_~-'''
        for t in range (len(nsw_token)):
            nsw_token[t] = nsw_token[t].lower()
            for l in range(len(nsw_token[t])):
                # print(nsw_token[t])
                if (nsw_token[t][l] == '\\'):
                    nsw_token[t] = nsw_token[t][0:l]
                    break
            for l in nsw_token[t]:
                if (l in punctuations):
                    nsw_token[t] = nsw_token[t].replace(l, "")
        while("" in nsw_token):
            nsw_token.remove("")
        dem_words += nsw_token

    for text in rep_ts:
        token_ls = tokenizeText(text)
        nsw_token = removeStopwords(token_ls)
        punctuations = '''!()-[]{};:'"\,<>./?@$%^&*_~'''
        for t in range (len(nsw_token)):
            nsw_token[t] = nsw_token[t].lower()
            for l in range(len(nsw_token[t])):
                # print(nsw_token[t])
                if (nsw_token[t][l] == '\\'):
                    nsw_token[t] = nsw_token[t][0:l]
                    break
            for l in nsw_token[t]:
                if (l in punctuations):
                    nsw_token[t] = nsw_token[t].replace(l, "")
        while("" in nsw_token):
            nsw_token.remove("")
        rep_words += nsw_token

    return dem_words, rep_words



if __name__ == '__main__':

    path = "/Users/jennawang/Desktop/EECS486/project/EECS-486-Final-Project/debate2020"
    os.chdir(path)
    democrat = []
    republic = []
    # iterate through all file
    count = 0
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}/{file}"
            # print(file_path)
            # call read text file function
            dem, rep = process_ts(read_text_file(file_path))
            democrat += dem
            republic += rep
        # count += 1
        # if (count == 1):
        #     break
    # print(democrat)
    # print(republic)
    dem_file = open("dem_terms.txt","w")#write mode
    for i in democrat:
        dem_file.write(i+' ')
    rep_file = open("rep_terms.txt","w")#write mode
    for i in republic:
        rep_file.write(i+' ')
