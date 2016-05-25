import global_vars
import random
import numpy as np
import datetime

def writeBuyClicksCSV(startTime, dayDuration):
	#get users who are playing and their buying probabilities
	teamAssignments = global_vars.globalTeamAssignments
	userSessions	= global_vars.globalUSessions
	assignmentsList = global_vars.globalTeamAssignments
	totalUsers 		= []
	buyProbabilities = []

	#numberOfItems = 30

	# price distributions for each platform
	platformBuyPriceDist = { 'iphone': [.05, .05, .20, .25, .30, .15],
		'mac': [.15, .15, .15, .30, .15, .10],
		'android' : [.40, .25, .15, .10, .05, .05 ],
		'windows': [ .60, .15, .10, .05, .05, .05 ],
		'linux': [.75, .05, .05, .05, .05, .05] }

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERATE buy database if global variable is None
	if(global_vars.buyDatabase is None):
		# NOTE: if you change the number of elements in buyPrices,
		# need to change all the distributions in platformBuyPriceDist.
		buyPrices = [0.99, 1.99, 2.99, 4.99, 9.99, 19.99]
		#pickCategories=np.random.choice(buyPrices, numberOfItems)
		buyDatabase = zip(range(0,len(buyPrices)), buyPrices) #each member is a tuple (buyID, category)
		global_vars.buyDatabase = buyDatabase
	else:
		buyDatabase = global_vars.buyDatabase

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GET list1= (teamid,userid) list2=buyfactor for each user currently playing

	addition = 0
	for s in userSessions:
		#GET ASSIGNMENT FOR THIS SESSION
		for assgn in assignmentsList:
			if(assgn['assignmentid'] == s['assignmentid']):
				teamid = assgn['teamid'] 
				userid = assgn['userid']
		buyfactor = global_vars.globalUsers[userid]['tags']['purchbeh']
		totalUsers.append((teamid, userid, s['userSessionid'], s['platformType'])) #list
		buyProbabilities.append(buyfactor) #list
		addition += buyfactor

	buyProbabilities = [x/addition for x in buyProbabilities]

	#pick 30% users for clicking based on their click probabilities
	factor = random.uniform(0, 0.3)
	#print factor	
	buyUsers = np.random.choice(range(0, len(totalUsers)), factor*len(totalUsers), replace=True, p=buyProbabilities).tolist()
	buyclicks = []

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERATE buyclicks from these users
	for indx in buyUsers:
		buyEvent = {}
		buyEvent['timeStamp'] = startTime + datetime.timedelta(hours=random.uniform(0, dayDuration.seconds // 3600))
		buyEvent['teamid'] = totalUsers[indx][0]
		buyEvent['userid'] = totalUsers[indx][1]
		platform = totalUsers[indx][3]
		pickABuy = np.random.choice(len(buyPrices), 1, p=platformBuyPriceDist[platform])[0]
		buyEvent['buyID'] = buyDatabase[pickABuy][0]
		buyEvent['buyPrice'] = buyDatabase[pickABuy][1]
		buyEvent['userSessionid'] = totalUsers[pickABuy][2]
		buyclicks.append(buyEvent)
		#print '%s %s' % (platform, buyEvent['buyPrice'])

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~APPEND to file
	buyLog = open("buy-clicks.log", "a")
	for b in sorted(buyclicks, key=lambda a: a['timeStamp']):
		buyLog.write("%s, userSessionid=%s, team=%s, userid=%s, buyID=%s, price=%s\n" %
			(b['timeStamp'].strftime(global_vars.timestamp_format), b['userSessionid'],
			b['teamid'], b['userid'], b['buyID'], b['buyPrice']))
	buyLog.close()

