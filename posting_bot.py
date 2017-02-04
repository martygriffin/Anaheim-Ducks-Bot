from dateutil.parser import parse
from datetime import timedelta, datetime
import time
import csv
import sys
import gc
import os
from services import RedditService
from services import NHLScoreService



def convertToDict(line):
        gameDict = {}
        date = parse(line[0] + " "+line [1])
        gameDict["startDate"] = date
        gameDict["startTime"] = line[1]
        gameDict["teams"] = line[2]
        gameDict["location"] = line[3]
        gameDict["description"] = line[4]
        return gameDict    
        
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
                                        RedditService.makePregamePost(game)
                                        already_done.append(game["startDate"].date())
                                except Exception as e:
                                        print(e)
                                        print("Connection error....will retry in 300 seconds")
                                        time.sleep(600)
                        elif (game["startDate"].date() in already_done and game["startDate"].date() not in already_done_post_game_thread):
                                print("attempting to make postgame postand speed up score check.....")

                                sleepTime  = 60
                                try:
                                        if(NHLScoreService.checkForPostGame(datetime.today().month,datetime.today().day, datetime.today().year, "ducks")):
                                                RedditService.makePostGamePost(game)
                                                already_done_post_game_thread.append(game["startDate"].date())
                                                sleepTime = 1200
                                except Exception as e:
                                        print(e)
                                        print("Connection error....will retry in 300 seconds")
                                        sleepTime = 1200
                                        time.sleep(600)

        print('Sleeping for'+str(sleepTime)+' seconds......zzzzzzzzzz........zzzzzzzz.......')
        file.close()
        time.sleep(sleepTime)