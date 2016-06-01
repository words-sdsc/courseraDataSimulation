#!/usr/bin/python

# TEST 3: At a given time, a user can only be assigned to one team

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from datetime import datetime
import numpy
import pandas as pd   

def value(item):
    return item[item.find('=')+1:]

#***********************************STEP1: group by time

df = pd.read_table('../team-assignments.log', header=None, delimiter=',',
                   converters={i:value for i in range(7)},
                   names='time team userid assignmentid'.split())

df = df.convert_objects(convert_numeric=True)

#all members of new user-team assignment datastructure are flushed at same timestamp
df = df.groupby(by=['time'],as_index=False)['assignmentid'].count()

print("\n----------------Count of Team-assignments formed at same time stamp: ")
print(df[df['assignmentid'] > 1])

#***********************************STEP2: read the file again and group by time, team, user

df = pd.read_table('../team-assignments.log', header=None, delimiter=',',
                   converters={i:value for i in range(7)},
                   names='time team userid assignmentid'.split())

df = df.convert_objects(convert_numeric=True)

#when a user is assigned to a team with same timestamp - that's an error
df = df.groupby(by=['time','team','userid'],as_index=False)['assignmentid'].count()

print("\n----------------Group by time, team, userid and count >1")
check = df[df['assignmentid'] > 1]

if not check.empty:
    print('[ERROR]: Found multiple user-team assignments with same time stamp!')
else:
	print('[TEST 3 PASS] No two user-team assignments have same timestamp\n')


