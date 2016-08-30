#!/usr/bin/python

# TEST 3: At a given time, a user can only be assigned to one team

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from datetime import datetime
import numpy
import pandas as pd   

#***********************************STEP1: group by time

df = pd.read_csv('../team-assignments.csv', sep=',')

#all members of new user-team assignment datastructure are flushed at same timestamp
df = df.groupby(by=['timestamp'],as_index=False)['assignmentId'].count()

#print("\n----------------Count of Team-assignments formed at same time stamp: ")
#print(df[df['assignmentId'] > 1])

#***********************************STEP2: read the file again and group by time, team, user

df = pd.read_csv('../team-assignments.csv', sep=',')

#when a user is assigned to a team with same timestamp - that's an error
df = df.groupby(by=['timestamp','team','userId'],as_index=False)['assignmentId'].count()

#print("\n----------------Group by time, team, userId and count >1")
check = df[df['assignmentId'] > 1]

if not check.empty:
    print('[ERROR]: Found multiple user-team assignments with same time stamp!')
else:
	print('[TEST 3 PASS] No two user-team assignments have same timestamp\n')


