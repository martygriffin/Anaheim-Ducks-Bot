
import praw
import OAuth2Util
import urllib3
import certifi

user_agent = "Anaheim Ducks GameDay 1.1 by /u/dahooddawg"
client="########"
secret="########"
username="########"
password="########"
ducksSubreddit='anaheimducks'

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