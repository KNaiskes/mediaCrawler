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
