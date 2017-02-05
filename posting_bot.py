
from datetime import timedelta, datetime
import time
import csv
import sys
import gc
import os
from services import RedditService
from services import NHLScoreService
from utils import Util
 
        
#keeps track of pregame threads that have already been posted
already_done_pregame_thread = []

#keeps track of postgame threads that have already been posted
already_done_post_game_thread = []

#time to selep between checks
sleepTime = 1200

#hours before game to post pregame thread
pregameHoursBefore= 12

#hours after start to start checking for game end
hoursAfterStartToCheck= 2

#NHL team Name
teamName= 'ducks'


while True:
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("checking for games today....." + currentTime)
        file = open('ducks.csv','rb')
        reader = csv.reader(file)

        for line in reader:
                game = Util.convertToDict(line)
                #check if therei a game toda
                if(game["startDate"].date() == datetime.today().date()):
                        #time to post pregream thread
                        postTime = game["startDate"] + timedelta(hours=-pregameHoursBefore)

                        #time to begin check for end of game
                        postGameTimeCheck = game["startDate"] + timedelta(hours=+hoursAfterStartToCheck)
                      
                        #if the post time is before the current time and there is not already a pregame thread posted
                        if(postTime < datetime.today() and game["startDate"].date() not in already_done_pregame_thread):
                                print("connecting.....")
                                try:
                                        RedditService.makePregamePost(game)
                                        already_done_pregame_thread.append(game["startDate"].date())
                                except Exception as e:
                                        print(e)
                                        print("Connection error....will retry in 300 seconds")
                                        time.sleep(600)
                        #if a pre-game thread has already been posted but not a post grame thread
                        elif (postGameTimeCheck < datetime.today() and game["startDate"].date() in already_done_pregame_thread and game["startDate"].date() not in already_done_post_game_thread):
                                print("attempting to make postgame postand speed up score check.....")

                                sleepTime  = 60
                                try:
                                        #check to see if the game is final
                                        if(NHLScoreService.checkForPostGame(datetime.today().month,datetime.today().day, datetime.today().year, teamName, "final")):
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