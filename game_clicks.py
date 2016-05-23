import global_vars
import random

def getGameClickUsers(team, numUsers, time):
	globalUsers = global_vars.globalUsers
	globalUSession = globa_vars.globalUSession

	# Grab users to fill.
	randIDS= random.sample(globalUsers.viewKeys(), numUsers)
	gameClickFileBuf = []

	# Not sure how to generate this.
	userSession = 0

	for userID in randIDS:
		gameClickFileBuf.append([userID, userSession, time, random.uniform(0,1)])

	# Data created, flush it to file.
	# TODO: Add file flush.
