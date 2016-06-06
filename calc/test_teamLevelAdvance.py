#!/usr/bin/python

# TEST 1

import math
import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from datetime import datetime
import numpy
import pandas as pd 

#*********************************** test 1

#teamdf = pd.read_table('../team.csv', header=None, delimiter=',',
	#converters={i:value for i in range(6)},
	#names='teamid name teamCreationTime teamEndTime strength currentLevel'.split())
#teamdf = teamdf.convert_objects(convert_numeric=True)

passalltests = True

levdf = pd.read_csv('../level-events.csv', sep=', ')

sesdf = pd.read_csv('../user-session.csv', sep=', ')

print '\nNo of level increases found in level-events.csv = ', len(levdf[levdf['eventType'] == 'end'])

for teamid in sorted(levdf['teamid'].unique()):
	#print 'Checking team', teamid
	maxLevel = levdf[levdf['teamid'] == teamid]['level'].max()
	if not math.isnan(maxLevel):
		#print '  max level is', maxLevel

		for level in range(2,maxLevel):
			#print 'check', level

			# check max session time for at level-1 is less than min start time at level
			endTimePrevLevel = sesdf[(sesdf['teamid'] == teamid) & (sesdf['team_level'] == (level-1)) & (sesdf['type'] == 'end')]['timestamp'].max()
			startTimeLevel = sesdf[(sesdf['teamid'] == teamid) & (sesdf['team_level'] == level) & (sesdf['type'] == 'start')]['timestamp'].min()
			#print 'end', endTimePrevLevel, 'start', startTimeLevel
			if endTimePrevLevel > startTimeLevel:
				print 'ERROR, team', teamid, 'session timestamps wrong for level', level, 'max end=', endTimePrevLevel, 'min start=', startTimeLevel
				passalltests = False

#print df

if passalltests:
	print('[TEST 1 PASS] Sessions closed for team members after level advancement.\n')
