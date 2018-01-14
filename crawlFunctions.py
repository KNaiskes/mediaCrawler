import requests
import json
from tokens import *

query = "coffee&type=place&{greece}"

respond = requests.get("https://graph.facebook.com/search?access_token=" + FacebookToken+ "&q=" + query)
#respond = json.loads(respond.text)["name"] 
respond = json.loads(respond.text)['data'][1]['name']
print(respond)

