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

user_agent = "Anaheim Ducks GameDay 1.0 by /u/dahooddawg"
subreddit = "insert subreddit name here"


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

        r = praw.Reddit(user_agent=user_agent)
        o = OAuth2Util.OAuth2Util(r)
        o.refresh(force=True)
        r.submit(subreddit, 'Pregame Thread: '+game["startDate"].date().strftime("%B %d, %Y") +" - "+game["teams"], text=game["startTime"]+" PST - "+game["location"]+" - "+game["description"])
        print("posted pregame for "+game["teams"])
def makeGamePost(game):
        print("connecting.....")
        r = praw.Reddit(user_agent=user_agent)
        o = OAuth2Util.OAuth2Util(r)
        o.refresh(force=True)
        r.submit(subreddit, 'Game Thread: '+game["teams"], text="Keep it classy and lets go Ducks!")
        print("posted  game thread for "+game["teams"])

already_done = []
already_done_game_thread = []

while(True):
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("checking for games today....." + currentTime)
        file = open('ducks.csv','rb')
        reader = csv.reader(file)

        for line in reader:
                game = convertToDict(line)
                print("checking csv:")
                if(game["startDate"].date() == datetime.today().date()):
                        postTime = game["startDate"] + timedelta(hours=-12)
                        gameThreadTime = game["startDate"] + timedelta(hours=-.5)
                        print("PostTime :")
                        print(postTime)
                        print("Game Thread Time :")
                        print(gameThreadTime)
                        if(postTime < datetime.today() and game["startDate"].date() not in already_done):
                                print("connecting.....")
                                try:
                                        makePregamePost(game)
                                except:
                                        print("Connection error....will retry in 300 seconds")
                                        time.sleep(300)
                                already_done.append(game["startDate"].date())


                        if(gameThreadTime < datetime.today() and game["startDate"].date() not in already_done_game_thread):
                                #make game thread post
                                try:
                                        makeGamePost(game)
                                except:
                                        print("Connection error....will retry in 300 seconds")
                                        time.sleep(300)

                                        #make that this game was posted so we do not duplicate any work
                                already_done_game_thread.append(game["startDate"].date())


        print('Sleeping for 10 minutes......zzzzzzzzzz........zzzzzzzz.......')
        file.close()
        time.sleep(600)
