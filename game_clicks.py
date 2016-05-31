import global_vars
import random
import numpy.random
import datetime
import math
import update_day

# Keeps track of total index.
clickIndex = 0

def writeGameClicksForTeam(teamID, team, time):
	if len(team) == 0:
		return
	numHits = calculateHitsRequired(teamID, team)
	gameClicks = createGameClickUsers(team, numHits, time)

	teamLevel = getTeamFromTeamID(teamID)["currentLevel"]

	# Data created, flush it to file.
	# Append file writer.
	appendFile = open("game-clicks.log", "a")
	for row in gameClicks:
		appendFile.write("%s, clickid=%s, userid=%s, usersessionid=%s, isHit=%s, teamId=%s, teamLevel=%s\n" %
			(row[0].strftime(global_vars.timestamp_format), row[1], row[2], row[3], row[4], teamID, teamLevel))
	appendFile.close()

def calculateHitsRequired(teamID, team):
	tracker = None
	hitsReqPerSlice = 0
	reqTotalHits = 0
	if teamID not in global_vars.teamLevelTracker:
		tracker = addTeamLevelTracker(teamID, team)
		currentLevel = getTeamFromTeamID(teamID)["currentLevel"]

		# Limit lower level for subtraction.
		if currentLevel <= 1:
			currentLevel = 2
		#required hits
		reqTotalHits = ((currentLevel+0) * (currentLevel+0) - 1)

		hitsReqPerSlice = math.ceil((reqTotalHits / tracker["slices"]))
		tracker["hitsReqPerSlice"] = hitsReqPerSlice
		tracker["reqTotalHits"] = reqTotalHits
	else:
		tracker = global_vars.teamLevelTracker[teamID]
		hitsReqPerSlice = tracker["hitsReqPerSlice"]
		reqTotalHits = tracker["reqTotalHits"]
		hitsReqPerSlice = tracker["hitsReqPerSlice"]

	if math.floor(reqTotalHits / hitsReqPerSlice) <= 0:
		tracker["hits"] = reqTotalHits
		return reqTotalHits - tracker["hits"]

	tracker["hits"] += hitsReqPerSlice
	return hitsReqPerSlice

# Function to keep track of level up. Returns tracker dict.
def addTeamLevelTracker(teamID, team):
	# Expected accuracy of team.
	expectedAcc = calculateTotalAccuracyPerSec(team) / len(team)
	if expectedAcc <= 0:
		expectedAcc = 100
	expectedTimeSlice = round(global_vars.dayDuration.total_seconds() / expectedAcc)
	if expectedTimeSlice <= 0:
		expectedTimeSlice = 1 # at least one.

	track = {}
	track["hits"] = 0
	track["slices"] = expectedTimeSlice
	global_vars.teamLevelTracker[teamID] = track

	return track

# Calculate the accuracy per sec for days estimate.
def calculateTotalAccuracyPerSec(team):
	totalCPS = 0
	totalAcc = 0
	for userID in team:
		user = getUserFromUserID(userID)
		totalCPS += user["tags"]["clicksPerSec"]
		totalAcc += user["tags"]["gameaccuracy"]

	return totalAcc * 10 /totalCPS # Accuracy times 10 for weight

# Creates a distribution from given userID CPS. Then
def createGameClickUsers(userIDs, numHits, time):
	# Calculate distribution of dataset based off CPS.
	cpsDistribute = getCPSUserList(userIDs, 1000)

	gameClickFileBuf = []

	userSession = 0

	counter = 0
	totalClicks = 0
	global clickIndex
	# Previous created time.
	prevTime = time
	# loop until we have satisfied number of hits
	while counter < numHits:
		# Randomly select a value from our distribution.
		randUserID = random.choice(cpsDistribute)
		userSession =  update_day.getSessionWithUserID(randUserID)["userSessionid"]
		# Generate hit value
		isHit = getIsHitBasedOffAccuracy(global_vars.globalUsers[randUserID]["tags"]["gameaccuracy"])
		# Append Result
		gameClickFileBuf.append([0, clickIndex, randUserID, userSession, isHit])
		if isHit > 0:
			counter += 1
		# Increment unique counter id.
		totalClicks += 1
		clickIndex += 1

	# Insert time now that we have total clicks and return
	generateTime(time, totalClicks, gameClickFileBuf)

	return gameClickFileBuf

# Inserts the time value into the data buffer.
def generateTime(startTime, numUsers, dataBuffer):
	# Lee way for each random time picking
	# Code will expire in 2^32 seconds or 2^64 seconds years.
	deltaTime = global_vars.dayDuration.total_seconds() / numUsers
	counter = 0
	prevTime = startTime
	changeTime = None
	while counter < numUsers:
		changeTime = datetime.timedelta(seconds=deltaTime)
		dataBuffer[counter][0] = getRandTime(prevTime, prevTime + changeTime)
		counter += 1
		prevTime = prevTime + changeTime

	return dataBuffer

# Function to get time inbetween [leftExtreme, rightExtreme]
# Should be datetime bounds
def getRandTime(leftExtreme, rightExtreme):
	# Use random integer for higher colission (more realistic)
	if rightExtreme < leftExtreme:
		return 0

	# Don't care too much about the year, but add check if you are doing
	# year time steps.
	year = random.randint(leftExtreme.year, rightExtreme.year)

	if leftExtreme.month < rightExtreme.month:
		month = random.randint(leftExtreme.month, rightExtreme.month)
	else:
		month = random.randint(rightExtreme.month, leftExtreme.month)

	if leftExtreme.day < rightExtreme.day:
		day = random.randint(leftExtreme.day, rightExtreme.day)
	else:
		day = random.randint(rightExtreme.day, leftExtreme.day)

	if leftExtreme.hour < rightExtreme.hour:
		hour = random.randint(leftExtreme.hour, rightExtreme.hour)
	else:
		hour = random.randint(rightExtreme.hour, leftExtreme.hour)

	if leftExtreme.minute < rightExtreme.minute:
		minute = random.randint(leftExtreme.minute, rightExtreme.minute)
	else:
		minute = random.randint(rightExtreme.minute, leftExtreme.minute)

	if leftExtreme.second < rightExtreme.second:
		sec = random.randint(leftExtreme.second, rightExtreme.second)
	else:
		sec = random.randint(rightExtreme.second, leftExtreme.second)

	noGoodDate = True
	while noGoodDate:
		try:
			result = datetime.datetime(year, month, day, hour, minute, sec, 0, None)
			noGoodDate = False
		except ValueError:
			day = day - 1
			continue

	return result

# Creates a list of userIDs reflecting clicksPerSec distribution.
def getCPSUserList(userIDs, samples):
	result = []
	while len(result) <= samples:
		randUserID = random.choice(userIDs)
		# CDF of normal distribution. Add the user if succeed.
		if numpy.random.normal(0.5, 0.4) <= getUserFromUserID(randUserID)["tags"]["clicksPerSec"]:
			result.append(randUserID)

	return result

def getUserFromUserID(userID):
	for user in global_vars.globalUsers:
		if user["id"] == userID:
			return user
	return None

def getTeamFromTeamID(teamID):
	for team in global_vars.globalTeams:
		if team["teamid"] == teamID:
			return team

	return None

# Returns a 1 hit, or 0 miss for accuracy in mind. Uses CDF of normal.
def getIsHitBasedOffAccuracy(accuracy):
	# Observe the CDF for probability
	if numpy.random.normal(0.5, 0.4)  <= accuracy:
		return 1
	return 0
