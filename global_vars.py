# File to house all globally defined values.
# Variable to house users.

# List containing a list of users.
globalUsers = []

# List containing current active teams per time update (day).
globalTeams = []

# List containing current sessions per time update (day).
yesterday_globalUSessions 	= None
globalUSessions 			= None

# List containing current team assignments per time update (day).
yesterday_globalTeamAssignments = None
globalTeamAssignments 			= None

# Day Duration
dayDuration = None

#collection of adID and categories
adDatabase = None

#collection of buyID and prices
buyDatabase = None

#global counter for generating unique IDs (increment this after every use)
counter = 5000

# Platform distributions
platforms	= ['iphone', 'android', 'mac', 'windows', 'linux']
freq 		= [0.4, 0.35, 0.05, 0.15, 0.05]

timestamp_format = "%Y-%m-%d %H:%M:%S"

max_accuracy = 0.7
