import praw
import OAuth2Util
from dateutil.parser import parse
from datetime import timedelta, datetime
import time
import csv
import urllib3
import certifi
import sys
import gc
import os

import urllib, json


user_agent = "Anaheim Ducks GameDay 1.1 by /u/dahooddawg"
client="########"
secret="########"
username="########"
password="########"
ducksSubreddit='anaheimducks'


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
        print("attempting post.....")
        r = praw.Reddit(user_agent=user_agent,password=password,username=username,client_id=client,client_secret=secret)
        subreddit = r.subreddit(ducksSubreddit)
        subreddit.submit('Pregame Thread: '+game["startDate"].date().strftime("%B %d, %Y") +" - "+game["teams"], selftext=game["startTime"]+" PST - "+game["location"]+" - "+game["description"])
        print("posted pregame for "+game["teams"])

def makePostGamePost(game):
        print("attempting post.....")
        r = praw.Reddit(user_agent=user_agent,password=password,username=username,client_id=client,client_secret=secret)
        subreddit = r.subreddit(ducksSubreddit)
        subreddit.submit('Post Game Thread: '+game["startDate"].date().strftime("%B %d, %Y") +" - "+game["teams"])
        print("posted post game for "+game["teams"])

def checkForPostGame(month, date, year):

        url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate="+str(year)+"-"+str(month)+"-"+str(date)+"&endDate="+str(year)+"-"+str(month)+"-"+str(date)+"&expand=schedule.teams,schedule.linescore&leaderCategories=&leaderGameTypes=R&site=en_nhl&teamId=&gameType=&timecode="
     
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for day in data["dates"]:
                for game in day["games"]:
                        if("final" in game["status"]["detailedState"].lower()):
                                if "ducks" in game["teams"]["away"]["team"]["teamName"].lower():
                                        print("Ducks away game final")
                                        return True
                                if "ducks" in game["teams"]["home"]["team"]["teamName"].lower():
                                        print("Ducks home game final")
                                        return True

                    

        print("No Ducks game or Ducks game in progress")                                 
        return False     

already_done = []
already_done_game_thread = []
already_done_post_game_thread = []

sleepTime = 1200

while(True):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("checking for games today....." + currentTime)
        file = open('ducks.csv','rb')
        reader = csv.reader(file)

        for line in reader:
                game = convertToDict(line)
                if(game["startDate"].date() == datetime.today().date()):
                        postTime = game["startDate"] + timedelta(hours=-12)
                        gameThreadTime = game["startDate"] + timedelta(hours=-1)
                        print("PostTime :")
                        print(postTime)
                        print("Game Thread Time :")
                        print(gameThreadTime)
                        if(postTime < datetime.today() and game["startDate"].date() not in already_done):
                                print("connecting.....")
                                try:
                                        makePregamePost(game)
                                        already_done.append(game["startDate"].date())
                                except:
                                        print("Connection error....will retry in 300 seconds")
                                        time.sleep(600)
                        elif (game["startDate"].date() in already_done and game["startDate"].date() not in already_done_post_game_thread):
                                print("attempting to make postgame postand speed up score check.....")

                                sleepTime  = 60
                                try:
                                        if(checkForPostGame(datetime.today().month,datetime.today().day, datetime.today().year)):
                                                makePostGame(game)
                                                already_done_post_game_thread.append(game["startDate"].date())
                                                sleepTime = 1200
                                except:
                                        print("Connection error....will retry in 300 seconds")
                                        sleepTime = 1200
                                        time.sleep(600)




        print('Sleeping for'+str(sleepTime)+' seconds......zzzzzzzzzz........zzzzzzzz.......')
        file.close()
        time.sleep(sleepTime)