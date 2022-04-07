import tweepy
import sys
import csv
import pandas as pd
import datetime
import preprocess

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

def get_tweets():

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


	# dates = generate_dates("2019-11-03", "2020-11-03")

	for tweet in tweepy.Cursor(api.search_full_archive, query=q, label="prod", maxResults=100, fromDate='201911040000', toDate='202011040000').items():
	# for tweet in tweepy.Cursor(api.search_tweets, q=q, count=100,
	# 					   lang="en", geocode='39.833,-98.58,2000mi').items():
		# if tweet.place != None:
		print(tweet.created_at, tweet.text)
		# t = preprocess(tweet.text.encode('utf-8'))
		cords = tweet.place.bounding_box
		l1, l2 = 0, 0
		for cord in cords:
			print(cord[0])
			exit(1)
		csvWriter.writerow([tweet.id, tweet.created_at, tweet.text.encode('utf-8'),] )


	# for date in dates:
	#
	# 	for tweet in tweepy.Cursor(api.search_tweets,q=q,count=100,
	# 							   lang="en",geocode='39.833,-98.58,2000mi',until=date).items():
	# 		# if tweet.place != None:
	# 		count += 1
	# 		print (tweet.created_at, tweet.text)
	# 		csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

	print(count)
if __name__ == '__main__':

	# print(generate_dates('2020-01-02', "2020-04-09"))

	df = get_tweets()
	df
	#



