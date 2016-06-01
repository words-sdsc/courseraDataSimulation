import global_vars
import datasets
import random
import numpy

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
	global_vars.yesterday_globalUSessions 		= list(global_vars.globalUSessions)
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

	userRate = global_vars.dayDuration.total_seconds() /  2400000 # Seconds that avg user should stay

	playingToNotPlaying(userRate, playingUsers, notPlayingUsers, TD)
	notPlayingToUnassigned(0.01, playingUsers, notPlayingUsers, unassignedUsers, TD)

	unassignedToNotPlaying(0.01, playingUsers, notPlayingUsers, unassignedUsers, TD)
	notPlayingToPlaying(0.40, playingUsers, notPlayingUsers, TD)

# Helper functions for simulation #

# fraction / # users in team =
def playingToNotPlaying(fraction, playingUsers, notPlayingUsers, TD):
	# print "START GENERATING p to nP"
	# print playingUsers
	# print notPlayingUsers
	# print "\n"
	# fraction / num users in team = each users chance of leaving
	total = 0
	for key, userIDs in playingUsers.iteritems():
		length = len(userIDs)
		if length == 0:
			length = 1
		prob = fraction / length
		#print "prob = ", prob
		remove = []
		for index, userID in enumerate(userIDs):
			if random.uniform(0, 1) <= prob:
				#print "deleteing userid = ", userID
				notPlayingUsers[key].append(userID)
				remove.append(index)
				# print "Ending session (pTnP): "
				session = endUserSession(userID, TD)
				# print "Session" + str(session) + "\n"
		deleteWithKeys(remove, userIDs)
		total += len(remove)
	print 'Deleted number of users = ', total 
	# print "START GENERATING p to nP"
	# print playingUsers
	# print notPlayingUsers
	# print "\n"

# Ends user session for users.
# Returns the session found and removed.
def endUserSession(userID, TD):
	# Edit globals
	session 	=getSessionWithUserID(userID)
	assignment 	= getTeamAssignmentWithUserID(userID)
	teamID 		= assignment["teamid"]

	#for assgn in global_vars.globalTeamAssignments:
	#				if assgn['userid']==userID:
	#					thisassign = assgn
	#					for ses in global_vars.globalUSessions:
	#						if ses['assignmentid']==thisassign['assignmentid']:
	#							session=ses

	#assigned = [assgn['userid'] for assgn in global_vars.globalTeamAssignments if assgn['userid']==userID]
	#print assigned

	#print session, userID
	#print "Session for assgid = ", session['assignmentid']
	buf = [session["userSessionid"], session["assignmentid"],session["startTimeStamp"], TD, session["team_level"],session["platformType"], userID, teamID]

	# Add user to write buffer.
	userSessionBuffer.append(buf)

	# delete the old session, currently inefficient, could be optimized
	# print "Deleting session: " + str(session) + "\n"
	global_vars.globalUSessions.remove(session)

	return session


# Generate movement of fraction of people going to unassigned
def notPlayingToUnassigned(fraction, playingUsers, notPlayingUsers, unassignedUsers, TD):
	# print "START GENERATING nP to un"
	# print playingUsers
	# print notPlayingUsers
	# print unassignedUsers
	# print "\n"
	# fraction is percentage of users from all notplaying that move.
	removeTeams = []
	for key, userIDs in notPlayingUsers.iteritems():
		remove = []
		for index, userID in enumerate(userIDs):
			if random.uniform(0, 1) <= fraction:
				# Move the user.
				unassignedUsers.append(userID)
				remove.append(index)
				# Delete empty team.
				deleteTeamAssignment(userID)

		if playingUsers.has_key(key):
			if len(userIDs) <= 0 and len(playingUsers[key]) <= 0:
				removeTeams.append(key)
		else:
			if len(userIDs) <= 0:
				removeTeams.append(key)

		deleteWithKeys(remove, userIDs)
	deleteTeams(removeTeams, playingUsers, notPlayingUsers, TD)
	# print "DONE GENERATING nP to un"
	# print playingUsers
	# print notPlayingUsers
	# print unassignedUsers
	# print "\n"

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
		newSession['platformType']	= numpy.random.choice(platforms, 1, replace=False, p=freq)[0]
	else:
		newSession['platformType'] = platform
	# Add to global session.
	global_vars.globalUSessions.append(newSession)

	return newSession

# Generate movement of prob of people going to not playing
#[5/28/16, 7:58:00 PM] Charles Chen: assigned the non-assigned teams to a team
#[5/28/16, 7:58:07 PM] Charles Chen: but does not allow them to play

# assigns a team to unassigned
def unassignedToNotPlaying(fraction, playingUsers, notPlayingUsers, unassignedUsers, TD):
	# fraction is percentage of users from all unassigned that move
	# print "START GENERATING un to nP"
	# print playingUsers
	# print notPlayingUsers
	# print unassignedUsers
	# print "\n"
	remove = []
	for index, userID in enumerate(unassignedUsers):
			# User selected to move
			if random.uniform(0, 1) <= fraction:
				teamID = 0
				# Go to existing team.
				if random.uniform(0, 1) >= fraction:
					# Update existing team info.
					randTeamID = random.choice(notPlayingUsers.keys())

					if randTeamID not in playingUsers:
						playingUsers[randTeamID] = []

					notPlayingUsers[randTeamID].append(userID)
					teamID = randTeamID
				else:
					# Create new team!
					team = {}
					team["name"] = datasets.getUserNames(1)[0]
					team["teamCreationTime"] = TD
					team["teamEndTime"] = float("inf")
					team["strength"] = datasets.getProbabilities(0.5,0.5,1)[0]
					team["currentLevel"] = 1
					team["teamid"] = global_vars.teamIDCounter
					teamID = team["teamid"]
					global_vars.teamIDCounter += 1
					# Actual function to create team.
					createTeam(team, playingUsers, notPlayingUsers)
					notPlayingUsers[teamID].append(userID)

				# Create team assignment info. Necessary for both choices.
				#print "Creating TAssignment For: " + str(userID)
				createTeamAssignment(teamID, userID, TD)
				# Remove the user
				remove.append(index)
	deleteWithKeys(remove, unassignedUsers)
	# print "DONE GENERATING un to nP"
	# print playingUsers
	# print notPlayingUsers
	# print unassignedUsers
	# print "\n"

def notPlayingToPlaying(fraction, playingUsers, notPlayUsers, TD):
	# fraction / num users in team = each users chance of leaving
	# print "START GENERATING nP to tP"
	# print  playingUsers
	# print notPlayUsers
	# print "\n"
	total = 0
	for key, userIDs in notPlayUsers.iteritems():
		if len(userIDs) > 0:
			prob = fraction / len(userIDs)
		else:
			prob = fraction
		remove = []
		for index, userID in enumerate(userIDs):
			if random.uniform(0, 1) <= prob:
				if key in playingUsers:
					playingUsers[key].append(userID)
				else:
					playingUsers[key] = [userID]
				remove.append(index)
				#print "NotPlayingToPlaying: " + str(userID)
				#print getTeamAssignmentWithUserID(userID)
				startUserSession(userID, TD)
				total += 1
				#print "\n"
		deleteWithKeys(remove, userIDs)
	print "Starting sessions for number of users =", total
	# print "DONE GENERATING nP to tP:"
	# print playingUsers
	# print notPlayUsers
	# print "\n"

def deleteTeamAssignment(userid):
	assign = getTeamAssignmentWithUserID(userid)
	#print assign
	global_vars.globalTeamAssignments.remove(assign)

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
def createTeam(team, playingUsers, notPlayingUsers):
	global_vars.globalTeams.append(team)
	# Are they required?
	# playingUsers[team["teamid"]] = []
	notPlayingUsers[team["teamid"]] = []

def deleteTeams(indexes, playingUsers, notPlayingUsers, TD):
	for index in indexes:
		deleteTeam(index, playingUsers, notPlayingUsers, TD)

# Writes to buffer the end
# team and delete team.
def deleteTeam(index, playingUsers, notPlayingUsers, TD):
	teamRemoved = getTeamWithTeamID(index)
	global_vars.globalTeams.remove(teamRemoved)

	teamRemoved["teamEndTime"] = TD
	global teamBuffer
	teamBuffer.append([teamRemoved["teamid"], teamRemoved["name"], teamRemoved["teamCreationTime"], teamRemoved["teamEndTime"], teamRemoved["strength"], teamRemoved["currentLevel"]])
	# Delete all traces of this team.
	if playingUsers.has_key(index):
		del playingUsers[index]

	if notPlayingUsers.has_key(index):
		del notPlayingUsers[index]


# Function to check if a team has leveled up from previous day.
def levelUp(playingUsers, notPlayingUsers, TD):
	removal = []
	for teamID, tracker in global_vars.teamLevelTracker.iteritems():
		if tracker["hits"] >= tracker["reqTotalHits"]:
			levelTeam(teamID, TD)
			# print "LEVEL UP! TeamID: " + str(teamID) + "\n"
			updateUserSessionWithTeam(playingUsers[teamID], teamID, TD)
			removal.append(teamID)

	deleteWithKeys(removal, global_vars.teamLevelTracker)
	return

# Leveup the team. -1 if team not found. 1 if found
def levelTeam(teamID, TD):
	for team in global_vars.globalTeams:
		if team["teamid"] == teamID:
			team["currentLevel"] += 1

			# Write to buffer
			levelUpBuffer.append([global_vars.eventIDCounter, TD, teamID, team["currentLevel"] - 1, "end"])
			global_vars.eventIDCounter += 1
			levelUpBuffer.append([global_vars.eventIDCounter, TD, teamID, team["currentLevel"], "start"])
			global_vars.eventIDCounter += 1
			
			return 1
	return -1

# Function to update the user sessions in a team.
def updateUserSessionWithTeam(team, teamID, TD):
	for userID in team:
		# print "Updating " + str(userID)
		oldSession = endUserSession(userID, TD)
		# print "Ending session: "
		# print "Session: " + str(oldSession) + "\n"
		# print "Starting session: "
		start = startUserSession(userID, TD, oldSession["platformType"])
		# print "Session: " + str(start) + "\n"

# Write the teams buffer.
def flushWriteTeams():
	global teamBuffer
	appendFile = open("team.log", "a")
	for buf in teamBuffer:
		appendFile.write("teamid=%s, name=%s, teamCreationTime=%s, teamEndTime=%s, strength=%s, currentLevel=%s\n" %
		(buf[0], buf[1], buf[2].strftime(global_vars.timestamp_format), buf[3].strftime(global_vars.timestamp_format), buf[4], buf[5]))

	appendFile.close()
	del teamBuffer[:]

# Write the assign teams buffer.
def flushTeamAssign():
	global teamAssignBuffer
	appendFile = open("team-assignments.log", "a")
	for buf in teamAssignBuffer:
		appendFile.write("time=%s, team=%s, userid=%s, assignmentid=%s\n" %
		(buf[3].strftime(global_vars.timestamp_format), buf[2], buf[1], buf[0]))

	appendFile.close()

	#check teamAssignBuffer for duplicate teams per user

	del teamAssignBuffer[:]

# Write the level up buffer.
def flushLevelUp():
	global levelUpBuffer
	appendFile = open("level-events.log", "a")
	for buf in levelUpBuffer:
		appendFile.write("%s eventid=%s, teamid=%s, level=%s, eventType=%s\n" %
		(buf[1].strftime(global_vars.timestamp_format), buf[0], buf[2], buf[3], buf[4]))

	del levelUpBuffer[:]

# Writes the user session buffer.
def flushUserSession():
	global userSessionBuffer
	appendFile = open("user-session.log", "a")
	for buf in userSessionBuffer:
		appendFile.write("userSessionid=%s, userid=%s, teamid=%s, assignmentid=%s, startTimeStamp=%s, endTimeStamp=%s, team_level=%s, platformType=%s\n" %
		(buf[0], buf[6], buf[7], buf[1], buf[2].strftime(global_vars.timestamp_format), buf[3].strftime(global_vars.timestamp_format), buf[4], buf[5]))

	appendFile.close()
	del userSessionBuffer[:]

# Delete dictionary elements given key
def deleteWithKeys(keys, dictionary):
	keys = sorted(keys, key=int, reverse=True)
	for key in keys:
		del dictionary[key]

def getTeamWithTeamID(teamID):
	for team in global_vars.globalTeams:
		if team["teamid"] == teamID:
			return team
	return None

# Helper function
def getTeamWithAssignmentID(assignmentID):
	for assign in global_vars.globalTeamAssignments:
		if assign["assignmentid"]==assignmentID:
			teamID = assign["teamid"]
			return getTeamWithTeamID(teamID)


# Gets the team assignment. None if DNE.
def getTeamAssignmentWithUserID(userID):
	result = None
	for assign in global_vars.globalTeamAssignments:
		if assign["userid"] == userID:
			result = assign
			# print "Find assign w/uid"
			# print "Teamm Assign: " + str(result)
	return result


# Returns entire session else -1.
def getSessionWithUserID(userID):
	assignment = getTeamAssignmentWithUserID(userID)
	#print "Assignment = ", assignment["assignmentid"]
	for session in global_vars.globalUSessions:
		if session["assignmentid"] == assignment["assignmentid"]:
			return session
	return None
