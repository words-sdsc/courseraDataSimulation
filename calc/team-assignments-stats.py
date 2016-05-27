#!/usr/bin/python

from datetime import datetime
import numpy
import re
import time

amnt = []
users = {}
teams = set()

f = open("../team-assignments.log")
for l in f:
	#print l
	ymd, hms, team, user = re.split("\s+,?", l, 3)
	user = user.rstrip()

	amnt.append({'ts': ymd + ' ' + hms, 't': team, 'u': user})
	
	d = datetime.strptime(ymd + ' ' + hms, "%Y-%m-%d %H:%M:%S")

	if user in users:
		u = users[user]
		if u['team'] == team:
			print 'ERROR: user %s joined same team %s consecutively' % (user, team)

		diff = (d - u['ts']).total_seconds()
		if diff < 10 * 60:
			print 'WARNING: user %s quickly changed teams (in %d minutes)' % (user, diff / 60)

	users[user] = {'ts': d, 'team': team}

	teams.add(team)

f.close

print 'Total assignments = ' + str(len(amnt))
print 'Total users changing assignments = ' + str(len(users))
print 'Total teams involved in assignments = ' + str(len(teams))
