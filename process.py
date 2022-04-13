from cmath import nan
import stat
import geocoder
import requests
from pkg_resources import safe_extra
import tweepy
import sys
import csv
import pandas as pd
import datetime
import preprocess
import numpy as np
from preprocess_jw import removeSGML, tokenizeText, removeStopwords, stemWords
import json


def process_county():


    df = pd.read_csv("tweets.csv", usecols = ['Time','Text','City','County','State','Country']) 
    df = df.reset_index()
    
    count = 0
    for index, row in df.iterrows():
        count += 1
        if(row['Country'] != "United States"):
            df = df.drop([index])
    df = df.reset_index()
    df.to_csv('US_tweets.csv')

    miss_county = []
    df = pd.read_csv('US_tweets.csv', usecols = ['Time','Text','City','County','State','Country'])
    df = df.reset_index()
    for i in range (df.shape[0]):
        if(pd.isnull(df.loc[i, 'County'])):
            miss_county.append(i)
            # print((df.loc[i, 'City'], df.loc[i, 'State']))
    # print(pd.isnull(df.loc[11, 'County']))
    for i in miss_county:
        if(df.loc[i, 'State'] == "District of Columbia" or df.loc[i, 'State'] == "Washington"):
            df.loc[i, 'County'] = "District of Columbia"
        elif(df.loc[i, 'City'] == "San Francisco"):
            df.loc[i, 'County'] = "San Francisco"
        elif(df.loc[i, 'City'] == "Baltimore"):
            df.loc[i, 'County'] = "Baltimore"
        elif(df.loc[i, 'City'] == "Carson City"):
            df.loc[i, 'County'] = "Carson City"
        elif(df.loc[i, 'City'] == "Columbia" and df.loc[i, 'State'] == "South Carolina"):
            df.loc[i, 'County'] = "Richland County"
        elif(df.loc[i, 'City'] == "Alexandria" and df.loc[i, 'State'] == "Virginia"):
            df.loc[i, 'County'] = "Alexandria"
        elif(df.loc[i, 'City'] == "Norfolk" and df.loc[i, 'State'] == "Virginia"):
            df.loc[i, 'County'] = "Norfolk"
        elif(df.loc[i, 'City'] == "Bronx" and df.loc[i, 'State'] == "New York"):
            df.loc[i, 'County'] = "Bronx"
        elif(df.loc[i, 'City'] == "Manhattan"):
            df.loc[i, 'County'] = "New York"
        elif(df.loc[i, 'City'] == "Queens"):
            df.loc[i, 'County'] = "Queens"
        elif(df.loc[i, 'City'] == "Brooklyn"):
            df.loc[i, 'County'] = "Kings"
        elif(df.loc[i, 'City'] == "Denver"):
            df.loc[i, 'County'] = "Denver"
        elif(df.loc[i, 'City'] == "Martinsville"):
            df.loc[i, 'County'] = "Martinsville"
        elif(df.loc[i, 'City'] == "St. Louis"):
            df.loc[i, 'County'] = "St. Louis"
        elif(df.loc[i, 'City'] == "Falls Church" and df.loc[i, 'State'] == "Virginia"):
            df.loc[i, 'County'] = "Falls Church"
        elif(df.loc[i, 'City'] == "Staten Island" and df.loc[i, 'State'] == "New York"):
            df.loc[i, 'County'] = "Richmond"
        elif(df.loc[i, 'City'] == "Sunnyside" and df.loc[i, 'State'] == "New York"):
            df.loc[i, 'County'] = "Queens"
        elif(df.loc[i, 'City'] == "Charlottesville"):
            df.loc[i, 'County'] = "Charlottesville"
        elif(df.loc[i, 'City'] == "Virginia Beach"):
            df.loc[i, 'County'] = "Virginia Beach"
        elif(df.loc[i, 'City'] == "Richmond"):
            df.loc[i, 'County'] = "Richmond"
        elif(df.loc[i, 'City'] == "New York" and df.loc[i, 'State'] == "New York"):
            df.loc[i, 'County'] = "New York"
        elif(df.loc[i, 'City'] == "Roanoke" and df.loc[i, 'State'] == "Virginia"):
            df.loc[i, 'County'] = "Roanoke"
        elif(df.loc[i, 'City'] == "Manchester" and df.loc[i, 'State'] == "Virginia"):
            df.loc[i, 'County'] = "Richmond"
        elif(df.loc[i, 'City'] == "Manchester" and df.loc[i, 'State'] == "Virginia"):
            df.loc[i, 'County'] = "Richmond"
        elif(df.loc[i, 'City'] == "Lynchburg"):
            df.loc[i, 'County'] = "Lynchburg"
        elif(df.loc[i, 'City'] == "Waynesboro"):
            df.loc[i, 'County'] = "Waynesboro"
        elif(df.loc[i, 'City'] == "Seacliff"):
            df.loc[i, 'County'] = "Santa Cruz"
        elif(df.loc[i, 'City'] == "Staunton"):
            df.loc[i, 'County'] = "Staunton"

    for i in range (df.shape[0]):
        if(pd.isnull(df.loc[i, 'County'])):
            df = df.drop([i])
    df.to_csv('US_tweets_county.csv')




def process_tweets(tweet):

    tweet_token = []

    token_ls = tokenizeText(tweet)
    nsw_token = removeStopwords(token_ls)
    punctuations = '''#!()-[]{};:'"\,<>./?@$%^&*_~'''
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

    tweet_token = nsw_token

    if (nsw_token[-1][0]=='h' and nsw_token[-1][1]=='t' and nsw_token[-1][2]=='t' and nsw_token[-1][3]=='p'):
        tweet_token = tweet_token[0:-1]

    last_token = ""
    for i in range (len(tweet_token[-1])):
        if (tweet_token[-1][i] != 'x'):
            last_token += tweet_token[-1][i]
        else:
            break
    
    tweet_token[-1] = last_token

    return tweet_token





if __name__ == '__main__':
    ls = []
    df = pd.read_csv('County_with_fips.csv')
    for i in range(len(df)):
        tweet_token = process_tweets(df.loc[i,'Text'][2:])
        sentence = ""
        for x in tweet_token:
            sentence += x + ' '
        ls.append((df.loc[i,'FIPS'],sentence))
    
    with open('sentence_fip.csv', 'w') as csv_file:  
        writer = csv.writer(csv_file)
        for i in ls:
            writer.writerow(i)








    # # process_county()
    # df = pd.read_csv("County_with_fips.csv") 
    # count = 0
    # words_county = {}
    # for i in range(len(df)):
    #     tweet_token = process_tweets(df.loc[i,'Text'][2:])
    #     if df.loc[i,'County'] in words_county:
    #         words_county[(df.loc[i,'County'],df.loc[i,'FIPS'])] += tweet_token
    #     else:
    #         words_county[(df.loc[i,'County'],df.loc[i,'FIPS'])] = tweet_token
    #     # count += 1
    #     # if count == 9:
    #     #     break
    
    # # with open('token_with_fip.txt', 'w') as convert_file:
    # #     convert_file.write(json.dumps(words_county))
    # with open("token_with_fip.txt", 'w') as f: 
    #     for key, value in words_county.items():
    #         output = str(key[1]) + ' '
    #         for i in value:
    #             output += i + ' '

    #         # f.write(str(key[1]) + ' ' + str(value))
    #         # f.write('%s:%s\n' % (key, value))
    #         f.write(output + '\n')
    

    
    # data = pd.read_csv("US_tweets_county.csv")
    # data = data.drop(['index'], axis=1)
    # data = data.drop(['indexx'], axis=1)
    # data.to_csv('US_tweets_county.csv')
