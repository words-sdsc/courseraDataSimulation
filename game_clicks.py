import global_vars
import random
import numpy.random

def writeGameClicksForTeam(team, numHits, time):
	gameClicks = createGameClickUsers(team, numHits, time)

	# Data created, flush it to file.
	# Append file writer.
	appendFile = open("game-clicks.log", "a")
	for row in gameClicks:
		appendFile.write("%s, user_session=%s, %s, isHit=%s\n" %
			(row[0], row[1], row[2], row[3]))
	appendFile.close()


# Creates a distribution from given userID CPS. Then
def createGameClickUsers(userIDs, numHits, time):
	# Calculate distribution of dataset based off CPS.
	cpsDistribute = getCPSUserList(userIDs, 1000)

	gameClickFileBuf = []

	# TODO: will be defined after next day function is defined
	userSession = 0

	counter = 0
	# loop until we have satisfied number of hits
	while counter < numHits:
		# Randomly select a value from our distribution.
		randUserID = random.choice(cpsDistribute)
		# Generate hit value
		isHit = getIsHitBasedOffAccuracy(global_vars.globalUsers[randUserID]["tags"]["gameaccuracy"])
		# Append Result
		gameClickFileBuf.append([randUserID, userSession, time, isHit])
		if isHit > 0:
			counter += 1

	return gameClickFileBuf

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
