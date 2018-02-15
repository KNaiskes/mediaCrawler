import requests
import json
from time import sleep
from tokens import *

def fbPlaces(place):
	query = place + "&type=place&/likes"
	fbList = dict()
	links = []
	titles = []

	try:
		for i in range(10):
			respond = requests.get("https://graph.facebook.com/search?access_token=" + FacebookToken+ "&q=" + query)
			takeLink= json.loads(respond.text)["data"][i]["id"]
			takeTitle = json.loads(respond.text)["data"][i]["name"]
			takeLink = "https://www.facebook.com/" + takeLink 
			links.append(takeLink)
			titles.append(takeTitle)
		fbList = dict(zip(links, titles))
	except(ValueError, IndexError):
		return fbList
	return fbList


def getTweets(tweet):
	tweets = dict()
	links = []
	titles = []
	import tweepy
	tweet = "#"+tweet
	auth = tweepy.OAuthHandler(Twitter_consumer_key, Twitter_consumer_secret)
	auth.set_access_token(Twitter_access_token, Twitter_access_token_secret)
	api = tweepy.API(auth)
	try:
		for t in tweepy.Cursor(api.search, q=tweet, result_type="latest").items(10):
			linkGet = "https://twitter.com/statuses/" + str(t.id)
			titleGet = t.text
			links.append(linkGet)
			titles.append(titleGet)
		tweets = dict(zip(links, titles))
	except(ValueError, IndexError):
		return tweets
	return tweets

def getFlickr(keyword):
	flickrList = dict()
	links = []
	titles = []
	import flickrapi
	flickr = flickrapi.FlickrAPI(Flickr_key, Flickr_secret)
	# to create link: flickr..../owner/id
	photo = flickr.photos_search(api_key=Flickr_key,text=keyword,per_page=10,page=1,format="parsed-json")
	try:
		for i in range(0,9):
			#link = "https://www.flickr.com/photos/" + photo["photos"]["photo"][i]["owner"] + "/" + photo["photos"]["photo"][i]["id"]  
			linkGet = "https://www.flickr.com/photos/" + photo["photos"]["photo"][i]["owner"] + "/" + photo["photos"]["photo"][i]["id"] 
			titleGet = photo["photos"]["photo"][i]["title"] 
			links.append(linkGet)
			titles.append(titleGet)
		flickrList = dict(zip(links, titles))
	except(ValueError, IndexError):
		return flickrList
	return flickrList


def getGplus(keyword):
	gplusList = dict() 
	links = []
	titles = []
	from apiclient.discovery import build

	api_key = GooglePlus_key

	service = build("plus", "v1", developerKey = api_key)

	activities_resource = service.activities()
	activities_document = activities_resource.search(maxResults=10, orderBy="best", query=keyword).execute()

	try:
		if "items" in activities_document:
			for activity in activities_document["items"]:
				links.append(activity["url"])
				titles.append(activity["title"])
		gplusList = dict(zip(links, titles))
	except(ValueError, IndexError):
		return gplusList
	return gplusList

def getYoutube(keyword):
	youtubeList = dict()
	links = []
	titles = []

	from googleapiclient.discovery import build

	api_key = GooglePlus_key #same key with g+
	
	youtube = build("youtube", "v3", developerKey=api_key)
	search_response = youtube.search().list(q=keyword, maxResults=10, part="id,snippet").execute()
	try:
		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				find_title = search_result["snippet"]["title"]
				titles.append(find_title)
				video_id = (search_result["id"]["videoId"])
				video_id = "https://www.youtube.com/watch?v="+video_id
				links.append(video_id)
		youtubeList = dict(zip(links, titles))

	except(ValueError, IndexError):
		return youtubeList

	return youtubeList

def getReddit(keyword):
	redditList = dict()
	links = []
	titles = []
	import praw

	reddit = praw.Reddit(client_id = Reddit_client_id,
			client_secret = Reddit_client_secret,
			username = Reddit_username,
			password = Reddit_password,
			user_agent = Reddit_userAgent)

	try:
		reddit.read_only = True
		sub = reddit.subreddit("all")
		for s in sub.search(keyword, limit=10):
			links.append(s.url)
			titles.append(s.title)
		redditList = dict(zip(links, titles))
	except(ValueError, IndexError):
		redditList
	return redditList
