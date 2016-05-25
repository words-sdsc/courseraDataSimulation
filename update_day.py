import global_vars

# Team assignment buffer used for housing all team writes.
teamAssignBuffer = []

# Contains Level Events format for flushing.
levelUpBuffer = []

# Contains data to write for ENDING teams.
teamBuffer = []

# Contains user session info to write to file.
userSessionBuffer = []

def simulateNextDay():
	levelUp()
	userMovement()

	# Flush the buffers for writing.
	flushWriteTeams()
	flushTeamAssign()
	flushLevelUp()
	flushUserSession()


# Moves users left and right.
def userMovement():
	checkTeamEmpty()

# Function to check if given team is empty, if so, write to buffer.
def checkTeamEmpty(team):

# Function to check if a team has leveled up from previous day.
def levelUp():

# Write the teams buffer.
def flushWriteTeams():

	teamBuffer = []

# Write the assign teams buffer.
def flushTeamAssign():

	teamAssignBuffer = []

# Write the level up buffer.
def flushLevelUp():

	levelUpBuffer = []

# Writes the user session buffer.
def flushUserSession():

	userSessionBuffer = []
