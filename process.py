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
from geopy.geocoders import Nominatim

if __name__ == '__main__':
    geolocator = Nominatim(user_agent="geoapiExercises")

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