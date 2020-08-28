from myToken import myToken #python class that contains personal information [user id, token from spotify]

import requests #to make a request to the spotify API
import json
import pandas as pd
import databaseConnection as dbConn

from datetime import datetime
from datetime import timedelta #to calculate difference in the dates


sessionData = myToken().getAccessInfo() #return a list containing the user id and
												#a session token

USERID = sessionData[0] 
TOKEN = sessionData[1]
URL = "https://api.spotify.com/v1/me/player/recently-played?limit=50&after={}"


DATABASE = "db/spotify_data.db"

def get_yesterdays_time():
	#convert the time to milliseconds
	return int((datetime.now() - timedelta(days = 1)).timestamp() * 1000)

def get_useful_data(rawData):
	for item in rawData["items"]:
		tempSong = []
		#Artist name, song name, played_at, day_played, time_played
		tempSong = [item["track"]["artists"][0]["name"], item["track"]["name"], item["played_at"], item["played_at"][:10], item["played_at"][11:19]]
		yield tempSong
	

if __name__ == "__main__":
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer {}".format(TOKEN)
	}

	#get yesterday's time in milliseconds
	time = get_yesterdays_time() 
	

	response = requests.get(URL.format(time), headers=headers)
	rawData = response.json()

	#list with the songs
	songsList = list(get_useful_data(rawData)) #return a generator, so must convert to list

	#make a dataframe from the song list
	dfSongs = pd.DataFrame(songsList, columns=["artist", "song", "id", "date", "date-time"])
	print(dfSongs)
	
