import requests
import json
from time import sleep
from tokens import *
import tweepy


def fbPlaces(place):
	query = place + "&type=place&/likes"

	#get the first 10 results
	for i in range(10):
		respond = requests.get("https://graph.facebook.com/search?access_token=" + FacebookToken+ "&q=" + query)
		respond = json.loads(respond.text)["data"][i]["name"]
		print(respond) #write to a file later
		sleep(2) #wait some time just to not get banned


def getTweets():
	auth = tweepy.OAuthHandler(Twitter_consumer_key, Twitter_consumer_secret)
	auth.set_access_token(Twitter_access_token, Twitter_access_token_secret)
	
	api = tweepy.API(auth)
	result = api.search(q="#athens", count=10, result_type = "latest", tweet_mode="extended")
	for r in result:
		print("*************************")
		print(r.full_text)
		sleep(5)
