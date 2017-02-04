
from dateutil.parser import parse
def convertToDict(line):
        gameDict = {}
        date = parse(line[0] + " "+line [1])
        gameDict["startDate"] = date
        gameDict["startTime"] = line[1]
        gameDict["teams"] = line[2]
        gameDict["location"] = line[3]
        gameDict["description"] = line[4]
        return gameDict   