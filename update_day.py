import global_vars
import datasets
import random

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
	levelUp(playingUsers, notPlayingUsers, TD)
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
	userRate = global_vars.dayDuration.total_seconds() /  1200 # Seconds that avg user should stay

	playingToNotPlaying(userRate, playingUsers, notPlayingUsers, TD)
	notPlayingToUnassigned(0.60, playingUsers, notPlayingUsers, unassignedUsers, TD)

	unassignedToNotPlaying(0.60, playingUsers, notPlayingUsers, unassignedUsers, TD)
	notPlayingToPlaying(userRate, playingUsers, notPlayingUsers, TD)


# Helper functions for simulation #

# fraction / # users in team =
def playingToNotPlaying(fraction, playingUsers, notPlayingUsers, TD):
	# fraction / num users in team = each users chance of leaving
	for key, userIDs in playingUsers.iteritems():
		prob = fraction / len(userIDs)
		remove = []
		for index, userID in enumerate(userIDs):
			if random.uniform(0, 1) < prob:
				#print "deleteing userid = ", userID
				notPlayingUsers[key].append(userID)
				remove.append(index)
				endUserSession(userID, TD)
		deleteWithKeys(remove, userIDs)


# Ends user session for users.
# Returns the session found and removed.
def endUserSession(userID, TD):
	# Edit globals
	session=None #getSessionWithUserID(userID)
	for assgn in global_vars.globalTeamAssignments:
					if assgn['userid']==userID:
						thisassign = assgn
						for ses in global_vars.globalUSessions:
							if ses['assignmentid']==thisassign['assignmentid']:
								session=ses

	#assigned = [assgn['userid'] for assgn in global_vars.globalTeamAssignments if assgn['userid']==userID]
	#print assigned



	#print session, userID
	#print "Session for assgid = ", session['assignmentid']
	buf = [session["userSessionid"], session["assignmentid"],
		session["startTimeStamp"], TD, session["team_level"],
		session["platformType"]]

	# Add user to write buffer.
	userSessionBuffer.append(buf)

	# delete the old session, currently inefficient, could be optimized
	global_vars.globalUSessions.remove(session)

	return session


# Generate movement of fraction of people going to unassigned
def notPlayingToUnassigned(fraction, playingUsers, notPlayingUsers, unassignedUsers, TD):
	# fraction is percentage of users from all notplaying that move.
	for key, userIDs in notPlayingUsers.iteritems():
		remove = []
		for index, userID in userIDs:
			if random.uniform(0, 1) <= fraction:
				# Move the user.
				unassignedUsers[key] = userID
				remove.append(index)

				# Delete empty team.
				if len(userIDs) <= 0:
					deleteTeam(userIDs, playingUsers, notPlayingUsers, unassignedUsers, TD)
		deleteWithKeys(remove, userIDs)

# Function to start user session, if none platform, uses distribution to random choose.
# Returns whatever was created.
def startUserSession(userID, TD, platform = None):
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
	if platform == None:
		newSession['platformType']	= np.random.choice(platforms, 1, replace=False, p=freq)[0]
	else:
		newSession['platformType'] = platform
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
	return newSession

# Generate movement of prob of people going to not playing
def unassignedToNotPlaying(fraction, playingUsers, notPlayingUsers, unassignedUsers, TD):
	# fraction is percentage of users from all unassigned that move
	for key, userIDs in unassignedUsers.iteritems():
		remove = []
		for index, userID in enumerate(userIDs):
				if random.uniform(0, 1) <= fraction:
					# Move the user
					notPlayUsers[key] = userID
					remove.append(index)

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
		deleteWithKeys(remove, userIDs)

def notPlayingToPlaying(fraction, playingUsers, notPlayUsers, TD):
	# fraction / num users in team = each users chance of leaving
	for key, userIDs in notPlayingUsers.iteritems:
		prob = fraction / len(userIDs)
		remove = []
		for index, userID in enumerate(userIDs):
			if random.uniform(0, 1) < prob:
				playingUsers[key].append(userID)
				remove.append(index)
				startUserSession(userID, TD)
		deleteWithKeys(remove, userIDs)

# Create team assignment and write to buffer.
def createTeamAssignment(teamid, userid, TD):
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
def levelUp(playingUsers, notPlayingUsers, TD):
	removal = []
	for teamID, tracker in global_vars.teamLevelTracker.iteritems():
		if tracker["hits"] >= tracker["reqTotalHits"]:
			levelTeam(teamID, TD)
			updateUserSession(playingUsers[teamID], teamID, TD)
			removal.append(teamID)

	deleteWithKeys(removal, global_vars.teamLevelTracker)
	return

# Leveup the team. -1 if team not found. 1 if found
def levelTeam(teamID, TD):
	for key, team in global_vars.globalTeams:
		if team["teamid"] == teamID:
			team["currentLevel"] += 1

			# Write to buffer
			levelUpBuffer.append([global_vars.eventIDCounter, TD, teamID, team["currentLevel"] - 1, "end"])
			levelUpBuffer.append([global_vars.eventIDCounter, TD, teamID, team["currentLevel"] + 1, "start"])

			return 1
	return -1

# Function to update the user sessions in a team.
def updateUserSessionWithTeam(team, teamID, TD):
	for userID in team:
		oldSession = endUserSession(userID, TD)
		startUserSession(userID, TD, oldSession["platformType"])

# Write the teams buffer.
def flushWriteTeams():
	appendFile = open("team.log")
	for buf in teamBuffer:
		appendFile.write("teamid=%s, name=%s, teamCreationTime=%s, teamEndTime=%s, strength=%s, currentLevel=%s" %
		(buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]))

	appendFile.close()
	teamBuffer = []

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

	appendFile = open("level-events.log")
	for buf in levelUpBuffer:
		appendFile.write("eventid=%s, timeStamp=%s, teamid=%s, level=%s, eventType=%s" %
		(buf[0], buf[1], buf[2], buf[3], buf[4]))

	levelUpBuffer = []

# Writes the user session buffer.
def flushUserSession():
	appendFile = open("user-session.log")
	for buf in userSessionBuffer:
		appendFile.write("userSessionid=%s, assignmentid=%s, starTimeStamp=%s, endTimeStamp=%s, team_level=%s, platformType=%s" %
		(buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]))

	appendFile.close()
	userSessionBuffer = []

# Delete dictionary elements given key
def deleteWithKeys(keys, dictionary):
	for key in keys:
		del dictionary[keys]

# Helper function
def getTeamWithAssignmentID(assignmentID):
	for assign in global_vars.globalTeamAssignments:
		if assign["assignmentid"]==assignmentID:
			teamID = assign["teamid"]
			return global_vars.globalTeams[teamID]


# Gets the team assignment. None if DNE.
def getTeamAssignmentWithUserID(userID):
	for assign in global_vars.globalTeamAssignments:
		if assign["userid"] == userID:
			return assign
	return None

# Returns entire session else -1.
def getSessionWithUserID(userID):
	assignment = getTeamAssignmentWithUserID(userID)
	#print "Assignment = ", assignment["assignmentid"]
	for session in global_vars.globalUSessions:
		if session["assignmentid"] == assignment["assignmentid"]:
			return session
	return None
