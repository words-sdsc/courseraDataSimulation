import global_vars
import random

globalUsers = global_vars.globalUsers

def getGameClickUsers(team, numUsers, time):
	#Grab users to fill
	randUsers = random.sample(globalUsers, numUsers)
	gameClickFileBuf = []

	# Not sure how to generate this.
	userSession = 0

	userId = 0
	for users in randUsers:
		gameClickFileBuf.append({userId, userSession, time, random.uniform(0,1)})
		userId += 1

	# Data created, flush it to file.
	# TODO: Add file flush.
