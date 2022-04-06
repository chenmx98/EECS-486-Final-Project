import tweepy
import sys
import csv

# assign the values accordingly
consumer_key = "ilH6jnBJdh9HQdsufmygvUwMB"
consumer_secret = "LqErCdWfdP6BWf3LH3Q0RrJAXHoFvmweBUNtI1WljJ2A8SMelW"
access_token = "1181071568493056000-3TIQxUKR3FdFk2lzHBoCVsNmeS8UYF"
access_token_secret = "0amhncBmQXJY05SZ4VCQxG3CM4iZhElNrdtdxKL2Ux1la"
    



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
	q = key
	a = "political"
	fetched_tweets = api.search_tweets(q) + api.search_tweets(a)
	print("Search query : " , q)

	text = {}
	for tweet in fetched_tweets:
		text[tweet.location] = tweet.text

	print(len(text))

if __name__ == '__main__':


	get_tweets()




