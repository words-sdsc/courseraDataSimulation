import global_vars
import random
import numpy.random

def writeGameClicksForTeam(team, numUsers, time):
	gameClicks = createGameClickUsers(team, numUsers, time)

	# Data created, flush it to file.
	# Append file writer.
	appendFile = open("game-clicks.log", "a")
	for row in gameClicks:
		appendFile.write("%s, user_session=%s, %s, isHit=%s\n" %
			(row[0], row[1], row[2], row[3]))
	appendFile.close()


# Creates a list of game click rows for writing to file.
def createGameClickUsers(userIDs, numClicks, time):
	globalUsers = global_vars.globalUsers
	# Grab users to fill. Based off the user's clicks per sec.
	# TODO: Minimum 1 click for each user?
	randIDS = getRandUsersBasedOffCPS(userIDs, numClicks)
	gameClickFileBuf = []

	# TODO: Will set user session after next day update is implemented.
	userSession =  0

	for userID in randIDS:
		gameClickFileBuf.append([userID, userSession, time, getIsHitBasedOffAccuracy(global_vars.globalUsers[userID]["tags"]["gameaccuracy"])])

	return gameClickFileBuf


# Gets a random user with CPS in mind.
# TODO: Implement minimum user get threshold.
def getRandUsersBasedOffCPS(userIDs, numUsers):
	if numUsers <= 0:
		return []

	result = []
	counter = 0
	while counter < numUsers:
		# Get a random user.
		randUser = random.choice(userIDs)

		# Accept random user based off clicksPerSec
		if random.randint(1, 10) <= global_vars.globalUsers[randUser]["tags"]["clicksPerSec"]:
			result.append(randUser)
			counter += 1

	return result


# Returns a 1 hit, or 0 miss for accuracy in mind. Uses CDF of normal.
def getIsHitBasedOffAccuracy(accuracy):
	# Observe the CDF for probability
	if numpy.random.normal(0.5, 0.4)  <= accuracy:
		return 1
	return 0
