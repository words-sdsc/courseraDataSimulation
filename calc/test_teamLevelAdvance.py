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
	#names='teamId name teamCreationTime teamEndTime strength currentLevel'.split())
#teamdf = teamdf.convert_objects(convert_numeric=True)

passalltests = True

levdf = pd.read_csv('../level-events.csv', sep=',')

sesdf = pd.read_csv('../user-session.csv', sep=',')

print '\nNo of level increases found in level-events.csv = ', len(levdf[levdf['eventType'] == 'end'])

for teamId in sorted(levdf['teamId'].unique()):
	#print 'Checking team', teamId
	maxLevel = int(levdf[levdf['teamId'] == teamId]['teamLevel'].max())
	if not math.isnan(maxLevel):
		#print '  max level is', maxLevel

		for level in range(2,maxLevel):
			#print 'check', level

			# check max session time for at level-1 is less than min start time at level
			endTimePrevLevel = sesdf[(sesdf['teamId'] == teamId) & (sesdf['teamLevel'] == (level-1)) & (sesdf['sessionType'] == 'end')]['timestamp'].max()
			startTimeLevel = sesdf[(sesdf['teamId'] == teamId) & (sesdf['teamLevel'] == level) & (sesdf['sessionType'] == 'start')]['timestamp'].min()
			#print 'end', endTimePrevLevel, 'start', startTimeLevel
			if endTimePrevLevel > startTimeLevel:
				print 'ERROR, team', teamId, 'session timestamps wrong for level', level, 'max end=', endTimePrevLevel, 'min start=', startTimeLevel
				passalltests = False

#print df

if passalltests:
	print('[TEST 1 PASS] Sessions closed for team members after level advancement.\n')
