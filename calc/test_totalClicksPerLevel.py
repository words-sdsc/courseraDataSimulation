#!/usr/bin/python

# TEST 2 
# TEST 5

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from datetime import datetime
import numpy
import pandas as pd 

#*********************************** test 2

df = pd.read_csv('../game-clicks.csv', sep=',')

df = df.groupby(by=['teamId','teamLevel'],as_index=False)['isHit'].sum()

print 'No of teams found in game-clicks.csv = ', df["teamId"].max()

passalltests = True

for i in df["teamId"].unique().tolist():
	mx = df["teamLevel"][(df["teamId"] == i)].max()
	#print 'Max level reached by team ', i,' = ', mx, ' testing each level ...'
	for j in range(1,int(mx)):
		#>>>>>>>>> this should match what is written in game-clicks.py

		formula = ((j+7) * (j+7))   #line 39 of reqTotalHits from game-clicks.py		

		#print formula
		found = df["isHit"][(df["teamId"] == i) & (df["teamLevel"] == j)].iloc[0]

		#print found
		if(formula != found):
			passalltests = False
			print 'ERROR: teamId=',i, '  teamLevel=',j, '  formula=', formula,'  found=', found

if(passalltests):
	print "[TEST 2 PASS] Number of hits for each level match the formula in game-clicks.py"


#*********************************** test 5

df = pd.read_csv('../game-clicks.csv', sep=',')

passalltests=True
for i in df["teamId"].unique().tolist():
	mx = df["teamLevel"][(df["teamId"] == i)].max()
	#print 'Max level reached by team ', i,' = ', mx, ' testing each level ...'
	for j in range(2,1+int(mx)):
		#>>>>>>>>> this should match what is written in game-clicks.py

		#print formula
		Lold = df["timestamp"][(df["teamId"] == i) & (df["teamLevel"] == j-1)].max()
		Lnew = df["timestamp"][(df["teamId"] == i) & (df["teamLevel"] == j)].min()
		#print Lold, Lnew

		#print found
		if(Lold > Lnew):
			passalltests = False
			print 'ERROR: teamID=',i, '  new teamLevel=',j,  Lold, ' old> ', Lnew
if(passalltests):
	print "[TEST 5 PASS] L+1 timestamps > L timestamps"
