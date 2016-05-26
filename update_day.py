import global_vars

# Team assignment buffer used for housing all team writes.
teamAssignBuffer = []

# Contains Level Events format for flushing.
levelUpBuffer = []

# Contains data to write for ENDING teams.
teamBuffer = []

# Contains user session info to write to file.
userSessionBuffer = []

def simulateNextDay(playingUsers, notPlayingUsers, unassignedUsers, TD):
	# Take a snap shot of the previous sessions and team assignments.
	global_vars.yesterday_globalUSessions = list(global_vars.globalUSessions)
	global_vars.yesterday_globalTeamAssignments = list(global_vars.globalTeamAssignments)

	# Function call for leveling up!
	levelUp()
	# Function dealing with any user movement.
	userMovement(playingUsers, notPlayingUsers, unassignedUsers, TD)

	# Flush the buffers for writing.
	flushWriteTeams()
	flushTeamAssign()
	flushLevelUp()
	flushUserSession()


# Simualte the user movements. Starts from stoping user play, to unassign
# and then unassigned to not playing to playing. That way all transitions
# are recorded.
def userMovement(playingUsers, notPlayingUsers, unassginedUsers, TD):
	userLeaveRate = TD.to_seconds() /  1200 # Seconds that user should stay

	playingToNotPlaying(userRetainRate, playingUsers, notPlayingUsers, TD)
	notPlayingToUnassigned()

	unassignedToNotPlaying()
	notPlayingToPlaying(userRetainRate, playingUsers, notPlayingUsers, TD)



# Helper functions for simulation #

# fraction / # users in team =
def playingToNotPlaying(fraction, playingUsers, notPlayingUsers, TD):
	# fraction / num users in team = each users chance of leaving
	for index, userIDs in playingUsers
		prob = fraction / len(userIDs)
		for userID in userIDs
			if random.uniform(0, 1) < prob
				notPlayUsers[index].append(userID)
				userIDs.remove(userID)
				endUserSession(userID, TD)


# Ends user session for users.
def endUserSession(userID, TD):
	# Edit globals
	session = getSessionWithUserID(userID)
	buf = list(session.values())
	# Write end time.
	buf[3] = TD

	# Add user to write buffer.
	userSessionBuffer.append([sessionId] + buf)

	# delete the old session
	del global_vars.globalUSessions[sessionId]

def notPlayingToUnassigned(fraction):
	# fraction / num users in team = each users chance of leaving
	checkTeamEmpty()

# Function to start user session
def startUserSession(userID, TD):
	assignment = getTeamAssignmentWithUserID(userID)
	assignmentID = assignment["assignmentid"]

	newSession = {}
	newSession['userSessionid'] = global_vars.counter
	global_vars.counter += 1
	newSession['assignmentid'] = assignmentID
	newSession['startTimeStamp'] = TD
	newSession['endTimeStamp'] = float("inf")
	newSession['team_level'] = getTeamWithAssignmentID(assignmentID)["currentLevel"]

	platforms	= global_vars.platforms
	freq 		= global_vars.freq
	newSession['platformType']	= np.random.choice(platforms, 1, replace=False, p=freq)[0]

	# Add to global session.
	global_vars.globalUSessions.append(newSession)

def unassignedToNotPlaying():
	checkTeamEmpty()


def notPlayingToPlaying(fraction, playingUsers, notPlayUsers, TD):
	# fraction / num users in team = each users chance of leaving
	for index, userIDs in notPlayingUsers
		prob = fraction / len(userIDs)
		for userID in userIDs
			if random.uniform(0, 1) < prob
				playingUsers[index].append(userID)
				userIDs.remove(userID)
				startUserSession(userID, TD)



# Function to check if given team is empty, if so, write to buffer.
def checkTeamEmpty(team):

# Function to check if a team has leveled up from previous day.
def levelUp():

# Write the teams buffer.
def flushWriteTeams():

	teamBuffer = []

# Write the assign teams buffer.
def flushTeamAssign():

	teamAssignBuffer = []

# Write the level up buffer.
def flushLevelUp():

	levelUpBuffer = []

# Writes the user session buffer.
def flushUserSession():

	userSessionBuffer = []

# Helper function
def getTeamWithAssignmentID(assignmentID):
	teamID = global_vars.globalTeamAssignments[assignmentID]["teamid"]
	return global_vars.globalTeams[teamID]


# Gets the team assignment. -1 if DNE.
def getTeamAssignmentWithUserID(userID):
	for assign in global_vars.globalTeamAssignments:
		if assign["userid"] == userID:
			return assign
	return -1

# Returns entire session else -1.
def getSessionWithUserID(userID):
	teamID = getTeamAssignmentWithUserID(userID)

	for session in global_vars.globalUSessions:
		if session["assignmentid"] == userID:
			return session
	return -1
