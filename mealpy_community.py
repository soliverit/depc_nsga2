### Includes ###
## Native 
from os.path					import isfile, isdir
from os							import mkdir
from time						import time
## Project
from lib.mealpy_community_optimiser	import MealPyCommunityOptimiser
from lib.mealpy_optimiser_base		import	MealPyOptimiserBase
from lib.building_set				import BuildingSet	
#############################
#  Command line parameters  #
#############################
MealPyOptimiserBase.MapConstructors()
# Parse

params		= MealPyCommunityOptimiser.ParseCMD()
dataPath	= params["data"]
buildings	= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E"])
inequality	= buildings.toRatingDifference(params["target"])
optimiser	= MealPyCommunityOptimiser(
	buildings=		buildings,
	constructor=	MealPyOptimiserBase.CONSTRCUTORS[params["constructor"]],
	epochs=			params["epochs"],
	population=		params["population"],
	resultsPath=	params["results_path"],
	partitions=		params["partitions"],
	threads=		params["threads"],
	processingPath=	params["processing_path"]
)

# Verify
#############################
#    The actual example     #
#############################
startTime	= time() 
optimiser.run()
print("Community process time: %s" %(time() - startTime))