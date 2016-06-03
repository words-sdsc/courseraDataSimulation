import global_vars
import random
import numpy as np
import datetime

def writeAdClicksCSV(startTime, dayDuration):
	#get global variables
	teamAssignments = global_vars.globalTeamAssignments
	userSessions	= global_vars.globalUSessions
	assignmentsList = global_vars.globalTeamAssignments
	totalUsers 		= []
	adProbabilities = []

	numberOfAds = 30

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERATE ad database if global variable is None
	if(global_vars.adDatabase is None):
		adCategories = ['sports', 'fashion', 'hardware', 'electronics', 'clothing', 'games', 'automotive', 'computers', 'movies']
		pickCategories=np.random.choice(adCategories, numberOfAds)
		adDatabase = zip(range(0,numberOfAds), pickCategories) #each member is a tuple (adID, category)
		global_vars.adDatabase = adDatabase
	else:
		adDatabase = global_vars.adDatabase

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GET list1= (teamid,userid) and list2=adfactor for each user currently playing
	#get users who are playing and their ad probabilities

	addition = 0
	for s in userSessions:
		#GET ASSIGNMENT FOR THIS SESSION
		for assgn in assignmentsList:
			if(assgn['assignmentid'] == s['assignmentid']):
				teamid = assgn['teamid']
				userid = assgn['userid']
		adfactor = global_vars.globalUsers[userid]['tags']['adbeh']
		totalUsers.append((teamid, userid, s['userSessionid'])) #list
		adProbabilities.append(adfactor) #list
		addition += adfactor

	adProbabilities = [x/addition for x in adProbabilities]

	#pick 0-5% users for clicking based on their click probabilities
	factor = random.uniform(0, 0.05)
	#print factor
	if len(totalUsers) <= 0:
		return
	adUsers  = np.random.choice(range(0, len(totalUsers)), int(factor*len(totalUsers)), replace=True, p=adProbabilities).tolist()
	adclicks = []

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~GENERATE adclicks from these users
	for indx in adUsers:
		adEvent = {}
		adEvent['txid'] = global_vars.counter
		global_vars.counter += 1
		adEvent['timeStamp'] = startTime + datetime.timedelta(seconds=random.choice(xrange(0, dayDuration.seconds)))

		adEvent['teamid'] = totalUsers[indx][0]
		adEvent['userid'] = totalUsers[indx][1]
		adEvent['userSessionid'] = totalUsers[indx][2]

		pickAnAd 				= np.random.choice(len(adDatabase), 1)[0]
		adEvent['adID']   		= adDatabase[pickAnAd][0]
		adEvent['adCategory'] 	= adDatabase[pickAnAd][1]
		adclicks.append(adEvent)

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~APPEND to file
	assignLog = global_vars.ad_clicks # open("ad-clicks.csv", "a")
	for a in sorted(adclicks, key=lambda a: a['timeStamp']):
		assignLog.write("%s, %s, %s, %s, %s, %s, %s\n" %
			(a['timeStamp'].strftime(global_vars.timestamp_format), a['txid'],
			a['userSessionid'], a['teamid'], a['userid'], a['adID'], a['adCategory']))
