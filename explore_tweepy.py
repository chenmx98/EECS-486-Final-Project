import tweepy
import csv
import json

# assign the values accordingly
consumer_key = "ilH6jnBJdh9HQdsufmygvUwMB"
consumer_secret = "LqErCdWfdP6BWf3LH3Q0RrJAXHoFvmweBUNtI1WljJ2A8SMelW"
access_key = "1181071568493056000-3TIQxUKR3FdFk2lzHBoCVsNmeS8UYF"
access_secret = "0amhncBmQXJY05SZ4VCQxG3CM4iZhElNrdtdxKL2Ux1la"
    
def get_tweets(username):
          
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  
        # Access to user's access key and access secret
        auth.set_access_token(access_key, access_secret)
  
        # Calling api
        api = tweepy.API(auth)
  
        # 200 tweets to be extracted
        number_of_tweets=200
        tweets = api.user_timeline(screen_name=username)
        print(tweets)

  
        # Empty Array
        tmp=[]
  
        # create array of tweet information: username,
        # tweet id, date/time, text
        tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created
        for j in tweets_for_csv:
  
            # Appending tweets to the empty array tmp
            tmp.append(j)
  
        # Printing the tweets
        print(tmp)
        
        
        
if __name__ == '__main__':
  
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    get_tweets("charlieputh")

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)
