import sys
import getopt
from initialize import *

def main():
	print "Initializing..."
	userDatabaseList = createUserDatabase(2000) #userID = index on the list
	teamDatabaseList = createTeamDatabase(100)  #teamID = index on the list
	assignmentsList = asssignUsersTOteams(userDatabaseList, teamDatabaseList)
	userSessionsList = initializeUserSessions(assignmentsList, teamDatabaseList)

	#helper functions:
	playingMembers 	= getPlayingMembers(userSessionsList, assignmentsList) # ['teamid']->[user1, user2,...] (have open sessions)
	allMembers  	= getAllMembers(assignmentsList) #['teamid']->[user1, user2,...] (all members)

if __name__ == "__main__":
	main()
