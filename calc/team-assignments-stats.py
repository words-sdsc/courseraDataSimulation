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
	ts, team, user, assmnt = re.split(",?\s+", l, 3)
	user = user.rstrip()

	#print ts
	#print team
	#print user

	amnt.append({'ts': ts, 't': team, 'u': user, 'a': assmnt})
	
	d = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")

	if user in users:
		u = users[user]
        # consecutive assignments to same team are ok, since log
        # does not contain unassignment events.
		#if u['team'] == team:
			#print 'ERROR: user %s joined same team %s consecutively' % (user, team)

		diff = (d - u['ts']).total_seconds()
		if diff < 1 * 60:
			print 'WARNING: user %s quickly changed teams (in %d minutes)' % (user, diff / 60)

	users[user] = {'ts': d, 'team': team}

	teams.add(team)

f.close

print 'Total assignments = ' + str(len(amnt))
print 'Total users changing assignments = ' + str(len(users))
print 'Total teams involved in assignments = ' + str(len(teams))
