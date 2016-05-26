#!/usr/bin/python

import sys
import getopt
import global_vars
from initialize import *
from ad_clicks import *
from buy_clicks import *
from game_clicks import *
import os
from random import randint

# Main function file.
def main():

	print "Initializing..."
	global_vars.globalUsers = createUserDatabase(randint(2000, 3000)) #userID = index on the list
	global_vars.globalTeams = createTeamDatabase(randint(100,200))  #teamID = index on the list
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
	for f in ["ad-clicks.log", "buy-clicks.log"]:
		if os.path.isfile(f):
			os.remove(f)

	#start time for Day = 0
	TD = datetime.datetime.now() + datetime.timedelta(days=random.uniform(2, 3))

	# SETTINGS FOR ITERATIONS #

	# Number of day iterations.
	dayIteration = 3

	# Time measure per day.
	dayMeasure = datetime.timedelta(hours=4)

	counter = 0
	while counter < dayIteration:
		for teams in global_vars.globalTeams:
			# dayDuration assumed to be in hours
			global_vars.dayDuration = dayMeasure

			# Write the game_clicks. TODO: Implement main function loop for team alteration.
			# Write one team for now. Ugly patchy access for now...
	 		totalHits= 100
			writeGameClicksForTeam(playingMembers.values()[0], totalHits, TD)

		# *APPENDS* ad clicks to "ad-clicks.log" for current players from time = TD to time = TD+dayDuration
		writeAdClicksCSV(TD, global_vars.dayDuration) # takes teamAssignments, userSessions, TeamAssignments from global variables

		# *APPENDS* buy clicks to "buy-clicks.log" for current players from time = TD to time = TD+dayDuration
		writeBuyClicksCSV(TD, global_vars.dayDuration) # takes teamAssignments, userSessions, TeamAssignments from global variables

	# Update the teams for next day.

	counter += 1

# Main function call hook.
if __name__ == "__main__":
	main()
