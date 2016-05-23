#! python
# Driver Program
# import 

# >>>>>>>>>>>>>>>>>>>>Alok
# initialize() #global state

		#Fill user hashmap:
				# ['userid'] -> ['nickname': '',  'twitter': '',  'dob': '',  'country': '',  'timeStamp': '', 'tags'=[gameaccuracy, purchbeh, adbeh, chatbeh] ]
				# globalUsers = createUserDatabase(minAge, maxAge, meanAge) //returns a hash map
		#Fill team hashmap: ['teamid'] -> ['name': '',  'teamCreationTime': '',  'teamEndTime': '', 'strength': '0-1']
		#Fill user-team assignment current-state hashmap ['assignmentid']->['userid': '', teamid': '',  'startTimeStamp': '',]
		#Create sessions for each user who is playing: ['sessionid']->[ 'assignmentid': '', 'startTimeStamp': '', 'endTimeStamp': '', 'team_level': '', 'platformType': '' ]
		#Fill team current-state hashmap: ['teamid']->['level': '', 'members': [] ]
		#dayLength: Int (mins)

# for each day in D
	# for every team T 
			# decide team levels at the end of this day
				#endOfDayLevel = howManyLevelsToday(l: thisLevel, T:Team)
						#last level is unfinished
						#end = f(no of sessions in T, x, strength)

			# for each level L crossed today: 'time=TD'

				# C = number of clicks needed at this level
				# >>>>>>>>>>>>>>>>>>>>Charles
				# pick 'x' users from T who will generate these hits
				# fill the 'GameClicks' file with rows for each hit
					# users = getGameClicksUsers(T: Team, N: Int, TD: Time) //return a list of users from playing ones

				# >>>>>>>>>>>>>>>>>>>>Alok
				# fill the AdClicks file with rows for each click - based on user tags
					# users = getAdClickUsers(T: Team, TD: Time)  //return a list of users from playing ones

				# >>>>>>>>>>>>>>>>>>>>Dan
				# fill the InAppPurchases file with rows for each click - based on user tags
					# users = getPurchasesUsers(T: Team, TD: Time) //return a list of pairs (user, price)

				# >>>>>>>>>>>>>>>>>>>>Dan
				# fill the Chat table with users from team T - based on user tags
					#fillChatTable(T, maxMentions: Int, TD: Time)

				# >>>>>>>>>>>>>>>>>>>>Charles
				# update global state for next day
					# call f(p: Int, TD: Time) = updates user team assignments for next day ()
									# create new teams
									# end old teams
									# change p% of user assignments
					# change user-team assignment
					# update sessions

				#TD=TD+dayDuration


