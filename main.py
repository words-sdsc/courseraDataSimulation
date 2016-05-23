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
	global_vars.globalTeamAssignments = asssignUsersTOteams(userDatabaseList, teamDatabaseList)
	global_vars.globalUSessions = initializeUserSessions(assignmentsList, teamDatabaseList)

	#auxillary functions:
	playingMembers 	= getPlayingMembers(global_vars.globalUSessions, global_vars.globalTeamAssignments) # ['teamid']->[user1, user2,...] (have open sessions)
	allMembers  	= getAllMembers(global_vars.globalTeamAssignments) #['teamid']->[user1, user2,...] (all members)

# Main function call hook.
if __name__ == "__main__":
	main()
