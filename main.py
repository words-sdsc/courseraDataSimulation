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

def sortLogFile(name):
	f = open(name, 'r')
	lines = f.readlines()
	f.close()
	f = open(name, 'w')
	lines.sort()
	for l in lines:
		f.write(l)
	f.close()

# Main function file.
def main():

	#Remove old csv files
	for f in ["ad-clicks.csv","buy-clicks.csv","game-clicks.csv","team-assignments.csv","users.csv", "user-session.csv", "level-events.csv", "team.csv"]:
		if os.path.isfile(f):
			os.remove(f)

	# print "Initializing..."
	openAllFiles()

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

	#____[4] unassigned users : returns a set of unassigned users
	unassignedUsers = getUnassignedUsers(global_vars.globalTeamAssignments)

	# SETTINGS FOR ITERATIONS #

	# Number of day iterations.
 	dayIteration = 100
	
    #start time for Day = 0
    #set start time to be dayIteration days from now in the past.
	TD = datetime.datetime.now() - datetime.timedelta(days=dayIteration)#+ datetime.timedelta(days=random.uniform(2, 3))
 
	# Time measure per day.
	global_vars.dayDuration = datetime.timedelta(minutes=30)

	print "..."
	# Loops for day simulation.
	counter = 0
	while counter < dayIteration:
		if((counter+1) %25 == 0):
			print "Day : " + str(counter + 1) + " out of " + str(dayIteration)
		teamCounter = 0

		for key, teams in playingMembers.iteritems():
			#if teamCounter % 50 == 0:
			#	print "Generating team: " + str(teamCounter)

			# Write the game_clicks.
			# Write one team for now.
			writeGameClicksForTeam(key, teams, TD)
			teamCounter += 1

		# *APPENDS* ad clicks to "ad-clicks.csv" for current players from time = TD to time = TD+dayDuration
		writeAdClicksCSV(TD, global_vars.dayDuration) # takes teamAssignments, userSessions, TeamAssignments from global variables
		# *APPENDS* buy clicks to "buy-clicks.csv" for current players from time = TD to time = TD+dayDuration
		writeBuyClicksCSV(TD, global_vars.dayDuration) # takes teamAssignments, userSessions, TeamAssignments from global variables

		TD += global_vars.dayDuration

		# Simulate Users.
		# print global_vars.globalUSessions
		# print global_vars.globalTeamAssignments
		# print global_vars.globalTeams
		# print "Playing: " + str(playingMembers)
		# print "Free: " + str(freeMembers)
		# print "Unassigned: " + str(unassignedUsers)
		# print "All Members: " + str(allMembers)
		# print "\n\n"
		# print "START SIMULATION"

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

	closeAllFiles()
	sortLogFile('game-clicks.csv')
	


# Main function call hook.
if __name__ == "__main__":
	main()
