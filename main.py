#!/usr/bin/python

import sys
import getopt
import global_vars
from initialize import *

# Main function file.
def main():
	

	print "Initializing..."
	global_vars.globalUsers = createUserDatabase(2000) #userID = index on the list
	global_vars.globalTeams = createTeamDatabase(100)  #teamID = index on the list
	global_vars.globalTeamAssignments = asssignUsersTOteams(global_vars.globalUsers, global_vars.globalTeams)
	global_vars.globalUSessions = initializeUserSessions(global_vars.globalTeamAssignments, global_vars.globalTeams)

	#auxillary functions:
	playingMembers 	= getPlayingMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments) # ['teamid']->[user1, user2,...] (have open sessions)
	allMembers  	= getAllMembers(global_vars.globalTeamAssignments) #['teamid']->[user1, user2,...] (all members)

	#start time for Day = 0
	TD = datetime.datetime.now() + datetime.timedelta(days=random.uniform(2, 3))

	#
	dayDuration = datetime.timedelta(hours=4) 


# Main function call hook.
if __name__ == "__main__":
	main()
