import global_vars
import random
import numpy.random
import datetime

# Keeps track of total index.
clickIndex = 0

def writeGameClicksForTeam(team, numHits, time):
	gameClicks = createGameClickUsers(team, numHits, time)

	# Data created, flush it to file.
	# Append file writer.
	appendFile = open("game-clicks.log", "a")
	for row in gameClicks:
		appendFile.write("time=%s, clickid=%s,  userid=%s, usersessionid=%s, isHit=%s\n" %
			(row[0], row[1], row[2], row[3], row[4]))
	appendFile.close()


# Creates a distribution from given userID CPS. Then
def createGameClickUsers(userIDs, numHits, time):
	# Calculate distribution of dataset based off CPS.
	cpsDistribute = getCPSUserList(userIDs, 1000)

	gameClickFileBuf = []

	# TODO: will be defined after next day function is defined
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

	return datetime.datetime(year, month, day, hour, minute, sec, 0, None)

# Creates a list of userIDs reflecting clicksPerSec distribution.
def getCPSUserList(userIDs, samples):
	result = []
	while len(result) <= samples:
		randUserID = random.choice(userIDs)
		# CDF of normal distribution. Add the user if succeed.
		if numpy.random.normal(0.5, 0.4) <= global_vars.globalUsers[randUserID]["tags"]["clicksPerSec"]:
			result.append(randUserID)

	return result


# Returns a 1 hit, or 0 miss for accuracy in mind. Uses CDF of normal.
def getIsHitBasedOffAccuracy(accuracy):
	# Observe the CDF for probability
	if numpy.random.normal(0.5, 0.4)  <= accuracy:
		return 1
	return 0
