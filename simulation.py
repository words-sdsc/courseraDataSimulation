#! python


#initialize global state

#Fill user hashmap: ['userid'] -> ['nickname': '',  'twitter': '',  'dob': '',  'country': '',  'timeStamp': '']

#Fill team hashmap: ['teamid'] -> ['name': '',  'teamCreationTime': '',  'teamEndTime': '']

#Fill user-team assignment current-state hashmap ['assignmentid']->['userid': '', teamid': '',  'sessionid': '',]

#Create sessions for each user who is playing: ['sessionid']->[ 'assignmentid': '', 'start_timeStamp': '', 'end_timeStamp': '', 'team_level': '', 'platformType': '' ]

#Fill team current-state hashmap: ['teamid']->['level': '', 'members': [] ]




# for every team T 
		# decide team levels at the end of this day

		# for each level L crossed today: 

			# C = number of clicks needed at this level
			# pick 'x' users from T who will generate these hits
			# fill the 'GameClicks' file with rows for each hit

			# pick 'y' users from T who will click on Ads
			# fill the AdClicks file with rows for each click

			# pick 'z' users from T who will make purchases
			# fil the InAppPurchases file with rows for each click

			# update global state for next day
				# create new teams
				# end old teams
				# change user-team assignment