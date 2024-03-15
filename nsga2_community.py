### Includes ###
## Native 
from os.path				import isfile
## Project
from lib.retrofit_nsga2		import RetrofitNSGA2
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
#############################
#    The actual example     #
#############################
# Load data
buildings	= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E"])
del params["dataCode"]
community	= NSGA2Community(buildings, "shoe", 
				partitions=params["partitions"], 
				threadCount=params["threads"], 
				flags=RetrofitNSGA2.ParamsToFlagString(params))
community.run()