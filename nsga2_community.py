### Includes ###
## Native 
from os.path				import isfile
from time					import time
## Project
from lib.nsga2_community	import NSGA2Community
from lib.building_set		import BuildingSet
#############################
#  Command line parameters  #
#############################
# Parse
params			= NSGA2Community.ParseCMD()

# Verify
dataPath		= "./data/" + params["dataCode"] + ".csv"
if not isfile(dataPath):
	print("Data path: " + dataPath + " not found")
	exit()
del params["dataCode"]
#############################
#    The actual example     #
#############################
# Load data
buildings	= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E"])
inequality	= buildings.toRatingDifference(params["targetRating"])
counter 	= 0
startTime	= time() 
while counter < params["recurrentSteps"]:
	community	= NSGA2Community(buildings,
					partitions=params["partitions"], 
					threadCount=params["threads"],
					inequality=inequality,
					flags=params,
					stateLabel="_" + str(counter))
	community.run()
	buildings	= community.results
	buildings.getScoreStruct("BEST_TEAM_STATE").print()
	params["stateIdentifier"] = "BEST_TEAM_STATE"
	buildings.shuffle()
	counter += 1
print("Community process time: %s" %(time() - startTime))