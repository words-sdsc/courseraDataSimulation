#!/usr/bin/python

# test 2 and 5

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from datetime import datetime
import numpy
import pandas as pd 

def value(item):
    return item[item.find('=')+1:]

#*********************************** test 2

df = pd.read_table('../game-clicks.log', header=None, delimiter=',',
                   converters={i:value for i in range(7)},
                   names='time clickid userid usersessionid isHit teamId teamLevel'.split())

df = df.convert_objects(convert_numeric=True)

df = df.groupby(by=['teamId','teamLevel'],as_index=False)['isHit'].sum()

print 'No of teams found = ', df["teamId"].max()

passalltests = True

for i in df["teamId"].unique().tolist():
	mx = df["teamLevel"][(df["teamId"] == i)].max()
	#print 'Max level reached by team ', i,' = ', mx, ' testing each level ...'
	for j in range(1,int(mx)):
		#>>>>>>>>> this should match what is written in game-clicks.py

		formula = ((j+0) * (j+0))   #line 39 of game-clicks.py		

		#print formula
		found = df["isHit"][(df["teamId"] == i) & (df["teamLevel"] == j)].iloc[0]

		#print found
		if(formula != found):
			passalltests = False
			print 'ERROR: teamID=',i, '  teamLevel=',j, '  formula=', formula,'  found=', found

if(passalltests):
	print "[TEST 2 PASS] Number of hits for each level match the formula in game-clicks.py"


#*********************************** test 5

df = pd.read_table('../game-clicks.log', header=None, delimiter=',',
                   converters={i:value for i in range(7)},
                   names='time clickid userid usersessionid isHit teamId teamLevel'.split())

df = df.convert_objects(convert_numeric=True)

passalltests=True
for i in df["teamId"].unique().tolist():
	mx = df["teamLevel"][(df["teamId"] == i)].max()
	#print 'Max level reached by team ', i,' = ', mx, ' testing each level ...'
	for j in range(2,1+int(mx)):
		#>>>>>>>>> this should match what is written in game-clicks.py

		#print formula
		Lold = df["time"][(df["teamId"] == i) & (df["teamLevel"] == j-1)].max()
		Lnew = df["time"][(df["teamId"] == i) & (df["teamLevel"] == j)].min()
		#print Lold, Lnew

		#print found
		if(Lold > Lnew):
			passalltests = False
			print 'ERROR: teamID=',i, '  new teamLevel=',j,  Lold, ' old> ', Lnew
if(passalltests):
	print "[TEST 5 PASS] L+1 timestamps > L timestamps"