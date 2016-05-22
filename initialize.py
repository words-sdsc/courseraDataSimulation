#! python
# Global State Initializer Function

# initialize() #global state

		#Fill user hashmap:
				# ['userid'] -> ['nickname': '',  'twitter': '',  'dob': '',  'country': '',  'timeStamp': '', 'tags'=[gameaccuracy, purchbeh, adbeh, chatbeh] ]
				# globalUsers = createUserDatabase(minAge, maxAge, meanAge) //returns a hash map
		#Fill team hashmap: ['teamid'] -> ['name': '',  'teamCreationTime': '',  'teamEndTime': '', 'strength': '0-1']
		#Fill user-team assignment current-state hashmap ['assignmentid']->['userid': '', teamid': '',  'sessionid': '',]
		#Create sessions for each user who is playing: ['sessionid']->[ 'assignmentid': '', 'start_timeStamp': '', 'end_timeStamp': '', 'team_level': '', 'platformType': '' ]
		#Fill team current-state hashmap: ['teamid']->['level': '', 'members': [] ]
		#dayLength: Int (mins)

from datasets import *
import copy
import random
import datetime

def initializer(noOfUsers=2000):
	users=[] # list of users, where userID = index on the list

	#~~~~~~~~~~~~~~~~~~1. generate users ~~~~~~~~~~~~~~~~~~

	countries = getCountries(noOfUsers) #list
	random.shuffle(countries)
	ages = getages(18, 70, 25, noOfUsers, 30) #min (18), max (70), mean 25, sigma 30
	accuracyFactor 	= getProbabilities(.5, .4, noOfUsers) #mu 0.5, sigma 0.4
	purchaseFactor 	= getProbabilities(.5, .2, noOfUsers)
	adFactor 		= getProbabilities(.5, .5, noOfUsers)
	chatFactor 		= getProbabilities(.5, .4, noOfUsers) # = accuracyFactor
	twitterHandles	= getTwitterIDs(noOfUsers)
	nicknames		= getUserNames(noOfUsers)

	#date when user accounts started
	startdate=datetime.datetime.now() - datetime.timedelta(7300) #days=20yrs*365
	
	print('   Generating users ...')
	for i in range(0, noOfUsers):
		newUser={}

		newUser['nickname']	=nicknames[i]
		newUser['twitter']	=twitterHandles[i]
		newUser['dob']		=datetime.date.today() - datetime.timedelta(days=365*ages[i])
		newUser['country']	=countries[i]
		newUser['timeStamp']=startdate+datetime.timedelta(random.uniform(1,7300)) #days=20yrs*365
		#'tags is a list'=[gameaccuracy, purchbeh, adbeh, chatbeh]
		newUser['tags']={'gameaccuracy':round(accuracyFactor[i], 3), 
						 'purchbeh':round(purchaseFactor[i],3), 
						 'adbeh':round(adFactor[i],3), 'chatbeh':round(chatFactor[i],3) }
		users.append(newUser)

	print '  ', noOfUsers, ' users generated'

	# ['userid'] -> ['nickname': '',  'twitter': '',  'dob': '',  'country': '',  'timeStamp': '', 'tags'=[gameaccuracy, purchbeh, adbeh, chatbeh] ]


