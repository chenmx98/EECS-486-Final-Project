# import tweepy


# # API key: 6GrSl68AveRadczuH4R2Cyg3A
# # API key secret: bAbwlziza3eozXHMiFE40k1hUl8GZU3nIw6oU2KZopECRCKRvP
# # Access token: 724625263095623680-m3Ek3CVYJUWr6iWtnSsbbJbeF5XYyWy
# # Access token secret: 0nwxKTEhoHje6q6fF1BWsszsOaccvc6XAnfMNOSK1z6I1
# # Bearer token: AAAAAAAAAAAAAAAAAAAAAB%2F8awEAAAAA7XFOWOnOa016O09IT6L7WAVjBXI%3D4PQ43xCqdmRKAgW7z9i9Kdzr9oQuNTnm5Nm7arunhkhUD1oaDC
# # Client ID: bTBrUGNndVhpQzdWRmhOZWVWUEk6MTpjaQ
# # Client Secret: SybWMCaP_QTjvV-KDAkLV-mB7RzNd14ljcPkQM990ErqdwZ_Nn

# import tweepy

# # client = tweepy.Client(
# #    "6GrSl68AveRadczuH4R2Cyg3A", "bAbwlziza3eozXHMiFE40k1hUl8GZU3nIw6oU2KZopECRCKRvP",
# #    "724625263095623680-m3Ek3CVYJUWr6iWtnSsbbJbeF5XYyWy", "0nwxKTEhoHje6q6fF1BWsszsOaccvc6XAnfMNOSK1z6I1"
# # )
# # api = tweepy.API(client)


# auth = tweepy.OAuthHandler("bTBrUGNndVhpQzdWRmhOZWVWUEk6MTpjaQ", "SybWMCaP_QTjvV-KDAkLV-mB7RzNd14ljcPkQM990ErqdwZ_Nn")
# auth.set_access_token("724625263095623680-m3Ek3CVYJUWr6iWtnSsbbJbeF5XYyWy", "0nwxKTEhoHje6q6fF1BWsszsOaccvc6XAnfMNOSK1z6I1")
# api = tweepy.API(auth)
# number_of_tweets=200
# tweets = api.user_timeline(screen_name="TAEYANG")
# tmp=[] 
# tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created 
# for j in tweets_for_csv:

#         # Appending tweets to the empty array tmp
#     tmp.append(j) 

#     # Printing the tweets
# print(tmp)

# # public_tweets = api.home_timeline()
# # for tweet in public_tweets:
# #     print(tweet.text)







import tweepy
import csv
import json

# assign the values accordingly
consumer_key = "ilH6jnBJdh9HQdsufmygvUwMB"
consumer_secret = "LqErCdWfdP6BWf3LH3Q0RrJAXHoFvmweBUNtI1WljJ2A8SMelW"
access_token = "1181071568493056000-3TIQxUKR3FdFk2lzHBoCVsNmeS8UYF"
access_token_secret = "0amhncBmQXJY05SZ4VCQxG3CM4iZhElNrdtdxKL2Ux1la"
    
# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    
# set access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret)
    
# calling the api 
api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=10, retry_delay=5, retry_errors=set([503]))

number_of_tweets=200
tweets = api.user_timeline(screen_name="twitter-handle")
print(tweets)
stop
tmp=[] 
tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created 
for j in tweets_for_csv:
     # Appending tweets to the empty array tmp
    tmp.append(j) 

    # Printing the tweets
print(tmp)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)
