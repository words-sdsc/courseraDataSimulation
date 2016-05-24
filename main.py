#!/usr/bin/python

import sys
import getopt
import global_vars
from initialize import *
from ad_clicks import *
from game_clicks import *

# Main function file.
def main():
	print "Initializing..."
	global_vars.globalUsers = createUserDatabase(2000) #userID = index on the list
	global_vars.globalTeams = createTeamDatabase(100)  #teamID = index on the list
	global_vars.globalTeamAssignments = asssignUsersTOteams(global_vars.globalUsers, global_vars.globalTeams)
	global_vars.globalUSessions = initializeUserSessions(global_vars.globalTeamAssignments, global_vars.globalTeams)

	#auxillary functions:
	playingMembers 	= getPlayingMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments) # ['teamid']->[userid1, userid2,...] (have open sessions)
	allMembers  	= getAllMembers(global_vars.globalTeamAssignments) #['teamid']->[userid1, userid2,...] (all members)

	#start time for Day = 0
	TD = datetime.datetime.now() + datetime.timedelta(days=random.uniform(2, 3))

	# dayDuration assumed to be in hours
	dayDuration = datetime.timedelta(hours=4)

	# Write the game_clicks. TODO: Implement main function loop for team alteration.
	# Write one team for now. Ugly patchy access for now...
 	totalHits= 100
	writeGameClicksForTeam(playingMembers.values()[0], totalHits, TD)

	#WRITE ad clicks for current players from time = TD to time = TD+dayDuration
	writeAdClicksCSV(TD, dayDuration) # takes teamAssignments, userSessions from global variables

# Main function call hook.
if __name__ == "__main__":
	main()
