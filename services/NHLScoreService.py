

import urllib, json

def checkForPostGame(month, date, year, team):
    
        url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate="+str(year)+"-"+str(month)+"-"+str(date)+"&endDate="+str(year)+"-"+str(month)+"-"+str(date)+"&expand=schedule.teams,schedule.linescore&leaderCategories=&leaderGameTypes=R&site=en_nhl&teamId=&gameType=&timecode="
     
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        for day in data["dates"]:
                for game in day["games"]:
                        if("final" in game["status"]["detailedState"].lower()):
                                if team in game["teams"]["away"]["team"]["teamName"].lower():
                                        print("Ducks away game final")
                                        return True
                                if team in game["teams"]["home"]["team"]["teamName"].lower():
                                        print("Ducks home game final")
                                        return True
                  
        print("No "+team+" game or "+team+" game in progress")                                 
        return False 