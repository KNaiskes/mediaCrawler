import requests
import json
from time import sleep
from tokens import *

def fbPlaces(place):
	query = place + "&type=place&/likes"
	fbList = []
	#with open("fbResults.txt", "w") as file:
		#get the first 10 results
	try:
		for i in range(10):
			respond = requests.get("https://graph.facebook.com/search?access_token=" + FacebookToken+ "&q=" + query)
			respond = json.loads(respond.text)["data"][i]["id"]
			respond = "https://www.facebook.com/" + respond
			fbList.append(respond)
	except(ValueError, IndexError):
		return fbList
				#print(respond) #write to a file later
				#respond = respond.replace(" ", "")
				#file.write(respond + "\n")
				#sleep(0.5) #wait some time just to not get banned
	return fbList


def getTweets(tweet):
	tweets = []
	import tweepy
	tweet = "#"+tweet
	auth = tweepy.OAuthHandler(Twitter_consumer_key, Twitter_consumer_secret)
	auth.set_access_token(Twitter_access_token, Twitter_access_token_secret)
	api = tweepy.API(auth)
	#with open("twitterResults.txt", "w") as file:
	try:
		for t in tweepy.Cursor(api.search, q=tweet, result_type="latest").items(10):
			result = "https://twitter.com/statuses/" + str(t.id)
			tweets.append(result)
	except(ValueError, IndexError):
		return tweets
			#file.write(result + "\n")
	return tweets

def getFlickr(keyword):
	flickrList = []
	import flickrapi
	flickr = flickrapi.FlickrAPI(Flickr_key, Flickr_secret)
	# to create link: flickr..../owner/id
	photo = flickr.photos_search(api_key=Flickr_key,text=keyword,per_page=10,page=1,format="parsed-json")
	#print("***********************************")
	#print(photo)
	#print(photo["photos"]["photo"][0]["id"])
	#with open ("flickrResults.txt", "w") as file:
	try:
		for i in range(0,9):
			link = "https://www.flickr.com/photos/" + photo["photos"]["photo"][i]["owner"] + "/" + photo["photos"]["photo"][i]["id"]  
			flickrList.append(link)
	except(ValueError, IndexError):
		return flickrList
				#print(link)
				#file.write(link + "\n")
	return flickrList


def getGplus(keyword):
	gplusList = []
	from apiclient.discovery import build

	api_key = GooglePlus_key

	service = build("plus", "v1", developerKey = api_key)

	activities_resource = service.activities()
	activities_document = activities_resource.search(maxResults=10, orderBy="best", query=keyword).execute()

	#with open("gplusResults.txt", "w") as file:
	try:
		if "items" in activities_document:
			#print("got page with %d" % len(activities_document["items"]))
			for activity in activities_document["items"]:
				gplusList.append(activity["url"])
	except(ValueError, IndexError):
		return gplusList
					#print(activity["url"])
					#print(activity["id"], activity["object"]["content"])
					#file.write(activity["url"]+ "\n")
	return gplusList

def getYoutube(keyword):
	youtubeList = []

	from googleapiclient.discovery import build

	api_key = GooglePlus_key #same key with g+
	
	youtube = build("youtube", "v3", developerKey=api_key)
	search_response = youtube.search().list(q=keyword, maxResults=10, part="id,snippet").execute()
	try:
		for search_result in search_response.get("items", []):
			if search_result["id"]["kind"] == "youtube#video":
				video_id = (search_result["id"]["videoId"])
				video_id = "https://www.youtube.com/watch?v="+video_id
				youtubeList.append(video_id)
	except(ValueError, IndexError):
		return youtubeList

	return youtubeList

def getReddit(keyword):
	redditList = []
	import praw

	reddit = praw.Reddit(client_id = Reddit_client_id,
			client_secret = Reddit_client_secret,
			username = Reddit_username,
			password = Reddit_password,
			user_agent = Reddit_userAgent)

	#print(reddit.user.me())
	reddit.read_only = True
	#print(reddit.read_only)
	#with open("redditResults.txt", "w") as file:
	#for submission in reddit.subreddit(keyword).hot(limit=10):
	#	#print(submission.url) #title
	#	#file.write(submission.url + "\n")
	#	redditList.append(submission.url)
	sub = reddit.subreddit("all")
	for s in sub.search(keyword, limit=10):
		redditList.append(s.url)
	return redditList
