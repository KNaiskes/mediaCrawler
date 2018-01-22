import requests
import json
from time import sleep
from tokens import *

def fbPlaces(place):
	query = place + "&type=place&/likes"

	#get the first 10 results
	for i in range(10):
		respond = requests.get("https://graph.facebook.com/search?access_token=" + FacebookToken+ "&q=" + query)
		respond = json.loads(respond.text)["data"][i]["name"]
		print(respond) #write to a file later
		sleep(2) #wait some time just to not get banned


def getTweets(tweet):
	import tweepy
	tweet = "#"+tweet
	auth = tweepy.OAuthHandler(Twitter_consumer_key, Twitter_consumer_secret)
	auth.set_access_token(Twitter_access_token, Twitter_access_token_secret)
	
	api = tweepy.API(auth)
	result = api.search(q=tweet, count=10, result_type = "latest", tweet_mode="extended")
	for r in result:
		print("*************************")
		print(r.full_text)
		sleep(5)

def getFlickr(keyword):
	import flickrapi
	flickr = flickrapi.FlickrAPI(Flickr_key, Flickr_secret)
	# to create link: flickr..../owner/id
	photo = flickr.photos_search(api_key=Flickr_key,text=keyword,per_page=10,page=1,format="parsed-json")
	print("***********************************")
	#print(photo)
	#print(photo["photos"]["photo"][0]["id"])
	for i in range(0,9):
		link = "https://www.flickr.com/photos/" + photo["photos"]["photo"][i]["owner"] + "/" + photo["photos"]["photo"][i]["id"]  
		print(link)

def getGplus(keyword):
	from apiclient.discovery import build

	api_key = GooglePlus_key

	service = build("plus", "v1", developerKey = api_key)

	activities_resource = service.activities()
	activities_document = activities_resource.search(maxResults=10, orderBy="best", query=keyword).execute()

	if "items" in activities_document:
		print("got page with %d" % len(activities_document["items"]))
		for activity in activities_document["items"]:
			print(activity["url"])
			#print(activity["id"], activity["object"]["content"])

def getReddit(keyword):
	import praw

	reddit = praw.Reddit(client_id = Reddit_client_id,
			client_secret = Reddit_client_secret,
			username = Reddit_username,
			password = Reddit_password,
			user_agent = Reddit_userAgent)

	#print(reddit.user.me())
	reddit.read_only = True
	print(reddit.read_only)
	for submission in reddit.subreddit(keyword).hot(limit=10):
		print(submission.url) #title
