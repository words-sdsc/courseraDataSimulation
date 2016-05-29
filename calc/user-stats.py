#!/usr/bin/python

from datetime import datetime
import numpy
import re
import time

user = {}
age = []

f = open("../users.log")
for l in f:
	#print l
	ymd, hms, id, nick, twit, dob, country = re.split("\s+,?", l, 6)
	user[id] = {
		'ts': ymd + ' ' + hms, 'nick': nick, 'twitter': twit,
		'dob': dob, 'country': country 
	}
	d = datetime.strptime(dob, 'dob=%Y-%m-%d')
	age.append(d)
f.close


age.sort()

now = datetime.now()

print 'Total users = ' + str(len(user))

times = [time.mktime(t.timetuple()) for t in age]
avg = datetime.fromtimestamp(numpy.average(times))
print 'Avg DOB = %s, %d years old' % (avg, now.year - avg.year,)

std = datetime.fromtimestamp(numpy.std(times))
print 'StdDev DOB %d years' % (std.year - datetime.fromtimestamp(0).year)

print 'Min DOB = %s, %d years old' % (age[0], now.year - age[0].year)
print 'Max DOB = %s, %d years old' % (age[len(age)-1], now.year - age[len(age)-1].year)
