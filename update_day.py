import global_vars
import datasets.py

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
	# TODO
	#levelUp()
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
def userMovement(playingUsers, notPlayingUsers, unassignedUsers, TD):
	userLeaveRate = TD.to_seconds() /  1200 # Seconds that avg user should stay

	playingToNotPlaying(userRetainRate, playingUsers, notPlayingUsers, TD)
	notPlayingToUnassigned(0.60, playingUsers, notPlayingUsers, unassignedUsers, TD)

	unassignedToNotPlaying(0.60, playingUsers, notPlayingUsers, unassignedUsers, TD)
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
	buf = [session["userSessionid"], session["assignmentid"],
		session["startTimeStamp"], TD, session["team_level"],
		session["platformType"]]

	# Add user to write buffer.
	userSessionBuffer.append([sessionId] + buf)

	# delete the old session
	del global_vars.globalUSessions[sessionId]


# Generate movement of fraction of people going to unassigned
def notPlayingToUnassigned(fraction, playingUsers, notPlayingUsers, unassignedUsers, TD):
	# fraction is percentage of users from all notplaying that move.
	for index, userIDs in notPlayingUsers:
		for userID in userIDs:
			if random.uniform(0, 1) <= fraction:
				# Move the user.
				unassignedUsers[index] = userID
				userIDs.remove(userID)

				# Delete empty team.
				if len(userIDs) <= 0
					deleteTeam(userIDs, playingUsers, notPlayingUsers, unassignedUsers, TD)


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

	# Being lazy and copy
	session = newSession
	# Add buffer:
	buf = [session["userSessionid"], session["assignmentid"],
		session["startTimeStamp"], session["endTimeStamp"], session["team_level"],
		session["platformType"]]
	# Append buffer
	userSessionBuffer.append(buf)

# Generate movement of prob of people going to not playing
def unassignedToNotPlaying(fraction, playingUsers, notPlayingUsers, unassignedUsers, TD):
	# fraction is percentage of users from all unassigned that move
	for index, userIDs in unassignedUsers:
		for userID in userIDs:
				if random.uniform(0, 1) <= fraction:
					# Move the user
					notPlayUsers[index] = userID
					userIDs.remove(userID)

					# Create new team!
					team = {}
					team["teamid"] = global_vars.teamIDCounter
					global_vars.teamIDCounter += 1
					team["name"] = datasets.getUserNames(1)[0]
					team["teamCreationTime"] = TD
					team["teamEndTime"] = float("inf")
					team["strength"] = datasets.getProbabilities(0.5,0.5,1)[0]
					team["currentLevel"] = 1
					createTeam(team, playingUsers, notPlayUsers, unassignedUsers)

					# Create team assignment.
					createTeamAssignment(team["teamid"], userID, TD)


def notPlayingToPlaying(fraction, playingUsers, notPlayUsers, TD):
	# fraction / num users in team = each users chance of leaving
	for index, userIDs in notPlayingUsers
		prob = fraction / len(userIDs)
		for userID in userIDs
			if random.uniform(0, 1) < prob
				playingUsers[index].append(userID)
				userIDs.remove(userID)
				startUserSession(userID, TD)

# Create team assignment and write to buffer.
def createTeamAssignment(teamid, userid, TD)
	assignT = {}
	assignT["assignmentid"] = global_vars.counter
	global_vars.counter += 1
	assignT["userid"] = userid
	assignT["teamid"] = teamid
	assignT["startTimeStamp"] = TD

	global_vars.globalTeamAssignments.append(assignT)

	# Write to buffer.
	teamAssignBuffer.append([assignT["assignmentid"], assignT["userid"], assignT["teamid"], assignT["startTimeStamp"]])


# Create a team, overwrite team if exists.
def createTeam(team, playingUsers, notPlayingUsers, unassignedUsers):
	global_vars.globalTeams.append(team)
	playingUsers[team["teamid"]] = []
	notPlayingUsers[team["teamid"]] = []
	unassignedUsers[team["teamid"]] = []

# Writes to buffer the end
# team and delete team.
def deleteTeam(team, index, playingUsers, notPlayingUsers, unassignedUsers, TD):
	teamRemoved = global_vars.globalTeams.pop(index)
	teamRemoved["teamEndTime"] = TD
	teamBuffer.append(teamRemoved.values())
	# Delete all traces of this team.
	del playingUsers[index]
	del notPlayingUsers[index]
	del unassignedUsers[index]


# Function to check if a team has leveled up from previous day.
def levelUp():
	#TODO

# Write the teams buffer.
def flushWriteTeams():
	appendFile = open("team.log")
	for buf in teamAssignBuffer:
		appendFile.write("teamid=%s, name=%s, teamCreationTime=%s, teamEndTime=%s, strength=%s, currentLevel=%s" %
		(buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]))

	appendFile.close()
	teamAssignBuffer = []

# Write the assign teams buffer.
def flushTeamAssign():
	appendFile = open("team-assignments.log")
	for buf in teamAssignBuffer:
		appendFile.write("assignmentid=%s, userid=%s, teamid=%s, startTimeStamp=%s" %
		(buf[0], buf[1], buf[2], buf[3]))

	appendFile.close()
	teamAssignBuffer = []

# Write the level up buffer.
def flushLevelUp():
	# TODO
	levelUpBuffer = []

# Writes the user session buffer.
def flushUserSession():
	appendFile = open("user-session.log")
	for buf in teamAssignBuffer:
		appendFile.write("userSessionid=%s, assignmentid=%s, starTimeStamp=%s, endTimeStamp=%s, team_level=%s, platformType=%s" %
		(buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]))

	appendFile.close()
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
