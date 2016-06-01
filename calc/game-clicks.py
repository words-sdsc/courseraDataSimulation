#!/usr/bin/python

from datetime import datetime
import numpy
import re
import time

#f = open("../level-events.log")
#for l in f:
	#2016-06-06 09:17:38 eventid=12, teamid=123, level=1, eventType=end
#	l = l.rstrip()
#	ymd, hms, eventid, teamid, level, etype = re.split("\s+,?", l, 5)

#	print etype
#f.close

team = {}

line = 1
f = open("../game-clicks.log")
for l in f:
	#time=2016-06-02T02:15:02, clickid=21, userid=115, usersessionid=6323, isHit=0, teamId=7, teamLevel=1
	l = l.rstrip()
	ts, clickid, userid, sessid, ishit, teamid, teamlevel = re.split(",\s+", l, 6)
	d = datetime.strptime(ts, "time=%Y-%m-%dT%H:%M:%S")
	
	if teamid not in team:
		team[teamid] = { 'level': teamlevel }
	elif team[teamid]['level'] > teamlevel:
		print 'ERROR level decreased for ' + teamid + ' on line ' + str(line)
	elif team[teamid]['level'] < teamlevel:
		#print 'level increased for ' + teamid + ' on line ' + str(line)
		team[teamid]['level'] = teamlevel

	line += 1

f.close

