
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

# assign the values accordingly
consumer_key = "ilH6jnBJdh9HQdsufmygvUwMB"
consumer_secret = "LqErCdWfdP6BWf3LH3Q0RrJAXHoFvmweBUNtI1WljJ2A8SMelW"
access_token = "1181071568493056000-3TIQxUKR3FdFk2lzHBoCVsNmeS8UYF"
access_token_secret = "0amhncBmQXJY05SZ4VCQxG3CM4iZhElNrdtdxKL2Ux1la"
    



def generate_dates(since, until):
	d0 = since.split("-")
	d1 = until.split("-")

	d0 = [int(i) for i in d0]
	d1 = [int(i) for i in d1]
	dates = []
	date0 = datetime.date(d0[0], d0[1],d0[2])
	date1 = datetime.date(d1[0], d1[1],d1[2])
	curr = date0

	while curr < date1:
		s = curr.strftime("%Y-%m-%d")

		dates.append(s)
		curr = curr + datetime.timedelta(days=7)
	print(dates)
	return dates

def get_county(city_state):
	location = geocoder.google(city_state)
	return location.current_result.county

def get_fips(lat, long):
    url = 'http://data.fcc.gov/api/block/find?format=json&latitude={}&longitude={}'
    request = url.format(lat, long)
    response = requests.get(request)
    data = response.json()
	return data['Block']['FIPS']


def get_tweets(df_location):

	#http://tweepy.readthedocs.org/en/v3.1.0/getting_started.html#api
	# authorization of consumer key and consumer secret
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	    
	# set access to user's access key and access secret 
	auth.set_access_token(access_token, access_token_secret)
	    
	# calling the api 
	api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, retry_delay=5, retry_errors=set([503]))


	#set count to however many tweets you want
	number_of_tweets = 100

	key = input("Search Keyword:")
	q = "#" + key
	a = "political"


	csvFile = open('result.csv', 'w')
	csvWriter = csv.writer(csvFile)
	fields = ['Time', 'Text', 'City', 'County', 'State']
	csvWriter.writerow(fields)

	geolocator = Nominatim(user_agent="geoapiExercises")

	# dates = generate_dates("2019-11-03", "2020-11-03")
	count = 0
	#geocode='39.833,-98.58,2000mi'
	# for tweet in tweepy.Cursor(api.search_full_archive, query=q, label="prod", maxResults=100, fromDate='202011030000', toDate='202011040000').items():
	for tweet in tweepy.Cursor(api.search_tweets, q=q, count=100,
						   lang="en").items():
		# if tweet.place != None:
		count+=1
		
		city = ""
		county = ""
		state = ""
		# print(tweet.created_at, tweet.text)
		# print(count)
		if (tweet.place!=None):
			coord = tweet.place.bounding_box.coordinates
			# print(coord)
			centroid = ((coord[0][0][0]+coord[0][1][0])/2,(coord[0][1][1]+coord[0][2][1])/2)
			Longitude = str(centroid[0])
			Latitude = str(centroid[1])
			
			# print(Latitude+","+Longitude)
			location = geolocator.reverse(Latitude+","+Longitude)
			add = location.raw['address']
			city = add.get('city', '')
			county = add.get('county', '')
			state = add.get('state', '')
			country = add.get('country', '')
			if (country == "United States"):
				csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), city, county, state])
			# print(tweet.full_name)


		else:
			# print(" ")
			# print(tweet.user.location)
			state, city = process_location(tweet.user.location, df_location)
			city_state = city + ', ' + state
			county = get_county(city_state)
			------------------------------------------------------------------------------------
			county1 = list(df_location[(df_location['city'] == city)]['county_name'])
			county2 = list(df_location[(df_location['state_name'] == state)]['county_name'])
			------------------------------------------------------------------------------------
			
			# county = add.get('county', '')
			csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'), city, county, state])

		
		if (count == 100):
			break

		# t = preprocess(tweet.text.encode('utf-8'))
		# cords = tweet.place.bounding_box
		# l1, l2 = 0, 0
		# for cord in cords:
		# 	print(cord[0])
		# 	exit(1)
		# csvWriter.writerow([tweet.id, tweet.created_at, tweet.text.encode('utf-8'),] )


	# for date in dates:
	#
	# 	for tweet in tweepy.Cursor(api.search_tweets,q=q,count=100,
	# 							   lang="en",geocode='39.833,-98.58,2000mi',until=date).items():
	# 		# if tweet.place != None:
	# 		count += 1
	# 		print (tweet.created_at, tweet.text)
	# 		csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


def process_location(str, df_location):
	words = str.split(", ")
	state = ""
	city = ""
	for i in words:
		if ((len(i) == 2 and i in df_location['state_id'].values) or (i in df_location['state_name'].values)):
			state = i
			# print(i)
		elif (i in df_location['city'].values):
			city = i
	if (len(state)==2):
		state = (df_location[df_location['state_id'] == state]['state_name'])
		state = list(state)[0]

		

	return state,city
	# if (len(words) > 1):
	# 	if ((len(words[-1]) == 2 and words[-1].upper() in df_location['state_id']) or (words[-1].lower() in df_location['state_name'].str.lower())):
	# 		return "match"
	# 	else:
	# 		return str
	# else:
	# 	if (words[0].lower() in df_location['city'].str.lower()):
	# 		return "match"
	# 	else:
	# 		return str






if __name__ == '__main__':

	# print(generate_dates('2020-01-02', "2020-04-09"))
	df_location = pd.read_csv("uscities.csv", usecols = ['city','city_ascii','state_id','state_name','county_name','lat','lng']) 
	get_tweets(df_location)
	#



