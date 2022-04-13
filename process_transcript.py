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
    dem_words = []
    rep_words = []
        # print(i[0])

    if (ts[0:4] == "HARR" or ts[0:4] == "BIDE"):
        token_ls = tokenizeText(ts)
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
        return ("Democrat", dem_words[1:])

    elif(ts[0:4] == "PENC" or ts[0:4] == "TRUM"):
        token_ls = tokenizeText(ts)
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
        return ("Republic", rep_words[1:])
    else:
        return ("MOD", "")
    



if __name__ == '__main__':

    path = "/Users/jennawang/Desktop/EECS486/project/EECS-486-Final-Project/debate2020"
    os.chdir(path)
    ls = []
    # iterate through all file
    count = 0
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt"):
            file_path = f"{path}/{file}"
            # print(file_path)
            # call read text file function
            full_text = read_text_file(file_path)
            full_text = full_text[2:]
            for i in full_text:
                tuple = process_ts(i)
                if (tuple[0]=="MOD"):
                    continue
                count+=1
            # print(tuple)
                ls.append(tuple)
            


    with open("party_transcript.csv", 'w') as csvfile: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
        csvwriter.writerow(['Party', 'Text']) 
        
    # writing the data rows 
        csvwriter.writerows(ls)

