#!/usr/bin/python

import sys
import getopt
import global_vars
from initialize import *
from ad_clicks import *
from buy_clicks import *
from game_clicks import *
from update_day import *
import os
from random import randint

# Main function file.
def main():

	# print "Initializing..."

	global_vars.globalUsers = createUserDatabase(2000) #randint(2000, 3000)) #userID = index on the list
	global_vars.globalTeams = createTeamDatabase(200) #randint(100,200))  #teamID = index on the list
	global_vars.globalTeamAssignments = asssignUsersTOteams(global_vars.globalUsers, global_vars.globalTeams)
	global_vars.globalUSessions = initializeUserSessions(global_vars.globalTeamAssignments, global_vars.globalTeams)

	#auxillary functions:
	#____[1] get team members who are playing right now
	playingMembers 	= getPlayingTeamMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments) # ['teamid']->[userid1, userid2,...] (have open sessions)

	#____[2] get all team members assigned to each team
	allMembers  	= getAllTeamMembers(global_vars.globalTeamAssignments) #['teamid']->[userid1, userid2,...] (all members)

	#____[3] get available team members who are assigned but not playing
	freeMembers		= getFreeTeamMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments) #['teamid']->[userid1,...] (free users with no open sessions)

	#Remove old log files
	for f in ["ad-clicks.log","buy-clicks.log","game-clicks.log","team-assignments.log","users.log", "user-session.log", "level-events.log", "team.log"]:
		if os.path.isfile(f):
			os.remove(f)

	#____[4] unassigned users : returns a set of unassigned users
	unassignedUsers = getUnassignedUsers(global_vars.globalTeamAssignments)

	#start time for Day = 0
	TD = datetime.datetime.now() + datetime.timedelta(days=random.uniform(2, 3))

	# SETTINGS FOR ITERATIONS #

	# Number of day iterations.
	dayIteration = 10

	# Time measure per day.
	global_vars.dayDuration = datetime.timedelta(hours=4)

	# Loops for day simulation.
	counter = 0
	while counter < dayIteration:
		print "Time Slice Number: " + str(counter + 1)
		teamCounter = 0

		for key, teams in playingMembers.iteritems():
			if teamCounter % 100 == 0:
				print "Generating team: " + str(teamCounter)

			# Write the game_clicks.
			# Write one team for now.
			writeGameClicksForTeam(key, teams, TD)
			teamCounter += 1

		# *APPENDS* ad clicks to "ad-clicks.log" for current players from time = TD to time = TD+dayDuration
		writeAdClicksCSV(TD, global_vars.dayDuration) # takes teamAssignments, userSessions, TeamAssignments from global variables
		# *APPENDS* buy clicks to "buy-clicks.log" for current players from time = TD to time = TD+dayDuration
		writeBuyClicksCSV(TD, global_vars.dayDuration) # takes teamAssignments, userSessions, TeamAssignments from global variables

		TD += global_vars.dayDuration

		# Simulate Users.
		# playingMembers 	= getPlayingTeamMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments)
		# freeMembers		= getFreeTeamMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments) #['teamid']->[userid1,...] (free users with no open sessions)
		# unassignedUsers = getUnassignedUsers(global_vars.globalTeamAssignments)
		# print global_vars.globalUSessions
		# print global_vars.globalTeamAssignments
		# print global_vars.globalTeams
		# print "Playing: " + str(playingMembers)
		# print "Free: " + str(freeMembers)
		# print "Unassigned: " + str(unassignedUsers)
		# print "All Members: " + str(allMembers)
		# print "\n\n"
		# print "START SIMULATION"
		#playingMembers 	= getPlayingTeamMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments)
		#freeMembers		= getFreeTeamMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments) #['teamid']->[userid1,...] (free users with no open sessions)
		#unassignedUsers 	= getUnassignedUsers(global_vars.globalTeamAssignments)

		simulateNextDay(playingMembers, freeMembers, unassignedUsers, TD)
		# print "END SIMULATION"
		# print global_vars.globalUSessions
		# print global_vars.globalTeamAssignments
		# print global_vars.globalTeams
		# print "Playing: " + str(playingMembers)
		# print "Free: " + str(freeMembers)
		# print "Unassigned: " + str(unassignedUsers)
		# print "All Members: " + str(allMembers)
		# print "\n\n"
		# Update the teams for next day.
		counter += 1

# Main function call hook.
if __name__ == "__main__":
	main()
