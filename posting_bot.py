import praw
import OAuth2Util
from dateutil.parser import parse
from datetime import timedelta, datetime
import time
import csv
import sys

print ("Duck Bot Start Up")

def convertToDict(line):
	gameDict = {}
	date = parse(line[0] + " "+line [1])
	gameDict["startDate"] = date
	gameDict["startTime"] = line[1]
	gameDict["teams"] = line[2]
	gameDict["location"] = line[3]
	gameDict["description"] = line[4]
	return gameDict
def makePregamePost(game):
	print("connecting.....")
	user_agent = "Anaheim Ducks GameDay 1.0 by /u/dahooddawg"
	r = praw.Reddit(user_agent=user_agent)
	o = OAuth2Util.OAuth2Util(r)
	o.refresh(force=True)
	r.submit('subreddit name goes here', game["startDate"].date().strftime("%B %d, %Y") +" - "+game["teams"], text=game["startTime"]+" PST - "+game["location"]+" - "+game["description"])
	print("posted for "+game["teams"])



already_done = []

while(True):
	print("checking for games today.....")
	file = open('ducks.csv','rb')
	reader = csv.reader(file)
	for line in reader:
			#convert game data to Dict
        	game = convertToDict(line)
        	#check if there is a game today
    		if(game["startDate"].date() == datetime.today().date()):
    			postTime = game["startDate"] + timedelta(hours=-12)
    			#check if it is 12 hours before game time
    			if(postTime < datetime.today() and game["startDate"].date() not in already_done):
    				#make pregram thread post
    				try:
    					makePregamePost(game)
    				except: 
    					print("Connection error....will retry in 300 seconds")
    					time.sleep(300)

    				#make that this game was posted so we do not duplicate any work
    				already_done.append(game["startDate"].date())
    				break
	file.close()
	time.sleep(1800)
    #sleep for 30 mins
    



