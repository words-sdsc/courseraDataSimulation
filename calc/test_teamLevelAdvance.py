#!/usr/bin/python

# TEST 1

import math
import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from datetime import datetime
import numpy
import pandas as pd 

def value(item):
    return item[item.find('=')+1:]

#*********************************** test 1

#teamdf = pd.read_table('../team.csv', header=None, delimiter=',',
	#converters={i:value for i in range(6)},
	#names='teamid name teamCreationTime teamEndTime strength currentLevel'.split())
#teamdf = teamdf.convert_objects(convert_numeric=True)

passalltests = True

levdf = pd.read_table('../level-events.csv', header=None, delimiter=',',
	converters={i:value for i in range(5)},
	names='time eventid teamid level eventType'.split())
levdf = levdf.convert_objects(convert_numeric=True)

sesdf = pd.read_table('../user-session.csv', header=None, delimiter=',',
	converters={i:value for i in range(8)},
	names='userSessionid userid teamid assignmentid startTimeStamp endTimeStamp team_level platformType'.split())
sesdf = sesdf.convert_objects(convert_numeric=True)

print '\nNo of level increases found in level-events.csv = ', len(levdf[levdf['eventType'] == 'end'])

for teamid in sorted(levdf['teamid'].unique()):
	#print 'Checking team', teamid
	maxLevel = levdf[levdf['teamid'] == teamid]['level'].max()
	if not math.isnan(maxLevel):
		#print '  max level is', maxLevel

		for level in range(2,maxLevel):
			#print 'check', level

			# check max session time for at level-1 is less than min start time at level
			endTimePrevLevel = sesdf[(sesdf['teamid'] == teamid) & (sesdf['team_level'] == (level-1))]['endTimeStamp'].max()
			startTimeLevel = sesdf[(sesdf['teamid'] == teamid) & (sesdf['team_level'] == level)]['startTimeStamp'].min()
			if endTimePrevLevel > startTimeLevel:
				print 'ERROR, team', teamid, 'session timestamps wrong for level', level, 'max end=', endTimePrevLevel, 'min start=', startTimeLevel
				passalltests = False

#print df

if passalltests:
	print('[TEST 1 PASS] Sessions closed for team members after level advancement.\n')
