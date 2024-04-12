### Includes ###
## Native 
from numpy									import array
from random 								import random
from os.path								import isfile
## Project
from depc_tools.depc_mealpy_optimisation	import DEPCMealPyOptimiser
# from lib.mealpy_optimiser_base				import MealPyOptimiserBase
from lib.building_set						import BuildingSet

#############################
#  Command line parameters  #
#############################
# Parse
params		= DEPCMealPyOptimiser.ParseCMD()
## File path stuff
# The input data path
# Make sure the input actually exists
if not isfile(params["data"]):
	print("Data path: " + params["data"] + " not found")
	exit()

#############################
#    The actual example     #
#############################
# Load data
buildings		= BuildingSet.LoadDataSet(params["data"]).getByRatings(["G", "F", "E"])
# Select the at risk buildings
buildingStats	= buildings.getCheapestToRating("D")
# Prepare problem
inequality		= params["inequality"] if params["inequality"] else  buildings.toRatingDifference("D")
buildings.filterRetrofitsByImpactRatio(buildingStats["cost"] / buildingStats["points"] * 2)
buildings.filterZeroOptionBuildings()
buildings.filterHarderMeasures()
DEPCMealPyOptimiser.MapConstructors()
if "silent" not in params:
	print("Cost:          %s" %(round(buildingStats["cost"])))
	print("Target points: %s" %(buildingStats["points"]))
	print("Met points:    %s" %(buildingStats["metPoints"]))
	print("Target ratio:  %s" %(round(buildingStats["cost"] / buildingStats["metPoints"], 2)))
# Make the thing
constructor	= DEPCMealPyOptimiser.CONSTRCUTORS[params["constructor"]]
optimiser	= DEPCMealPyOptimiser(buildings, 
	inequality=	inequality,
	epochs=		params["epochs"],
	population=	params["population"],
	algorithm=	constructor
)

optimiser.solve()
print("%s: %s" %(constructor.__name__, optimiser.lastResult.target.objectives[0] ))
if params["results_path"]:
	with open(params["results_path"], "a") as file:
		file.write("%s,%s\n" %(optimiser.lastResult.target.objectives[0], params["data"]))