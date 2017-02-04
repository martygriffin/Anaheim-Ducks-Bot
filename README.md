# Anaheim-Ducks-Bot
Bot for the Anaheim Ducks Subreddit

v1.1

-added support for post game threads

v1.0

-added support for posting pregame threads 12 hours before game time

##Installation

 Required Python Package install for Anaheim Ducks Bot:
 *python-dateutil #awesome datetime parasing
 *OAuth2Util #oauth support for reddit loing
 *praw #python library for interacting with reddit

##Run in foregroung
python ./posting_bot

##Run in Background
./duck_monitor.sh &

The shell script ensures that the posting bot script contiunes to run and automatically restarts it on any failures


