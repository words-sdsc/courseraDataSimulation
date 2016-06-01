#!/usr/bin/python

# TEST 2 
# TEST 5

import warnings
warnings.filterwarnings("ignore", category=FutureWarning) 

from datetime import datetime
import numpy
import pandas as pd 

def value(item):
    return item[item.find('=')+1:]

#*********************************** test 1

df = pd.read_table('../level-events.log', header=None, delimiter=',',
                   converters={i:value for i in range(5)},
                   names='time eventid teamid level eventType'.split())


df = df.convert_objects(convert_numeric=True)

#print df

#df = df.groupby(by=['teamId','teamLevel'],as_index=False)['isHit'].sum()

print '\nNo of level increases found in level-events.log = ', len(df[df['eventType'] == 'end'])

passalltests = True
