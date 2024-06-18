### Includes ###
## Native 
from numpy									import array
from random 								import random
from os.path								import isfile
## Project
from depc_tools.depc_mealpy_optimisation	import DEPCMealPyOptimiser
# from lib.mealpy_optimiser_base				import MealPyOptimiserBase
from lib.building_set						import BuildingSet
from lib.retrofit_option					import RetrofitOption

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
buildings		= BuildingSet.LoadDataSet(params["data"]).getByRatings(["G", "F"])
# Select the at risk buildings
buildingStats	= buildings.getCheapestToRating("E")
# Prepare problem
inequality		= params["inequality"] if params["inequality"] else  buildings.toRatingDifference("E")
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
state					= [ int(x) for x in optimiser.lastResult.solution]
keys					= list(RetrofitOption.RETROFIT_OPTION_KEYS)
for key in keys.copy():
	keys.append(key + "_p")
result		= dict.fromkeys(RetrofitOption.RETROFIT_OPTION_KEYS,0)
result["envelopes_c"]	= 0
result["roof_c"]		= 0
result["windows_c"]		= 0
result["hotwater_c"]	= 0
for key in keys:
	result[key + "_p"]	= 0
for id in range(len(buildings)):
	building							= buildings.buildings[id]
	retrofit							= building.getRetrofit(state[id])
	option								= retrofit.description
	result[option.description]			+= retrofit.cost
	result[option.description + "_p"]	+= retrofit.difference 
	for measure in retrofit.description.measures:
		component	= building.retrofitHash[measure]
		result[measure + "_c"] += component.cost

score				= buildings.scoreState(state)
result["alias"]		= params["alias"]
result["cost"]		= score["cost"]
result["points"]	= score["points"]
result["objPoints"]	= buildingStats["points"]
result["objCost"]	= buildingStats["cost"]
result["metPoints"]	= buildingStats["metPoints"]
result["buildings"]	= buildings.length
keys				= [ "alias", "cost", "points", "objPoints", "objCost", "metPoints", "buildings"] + keys + ["envelopes_c", "roof_c", "hotwater_c", "windows_c"]
shoe 				= ",".join([str(result[key]) for key in keys])
print(shoe)

with open("./results/sets/gf-only-75-100-3k.csv", "a") as file:
	file.write(shoe + "\n")
for i in range(buildings.length):
	building	= buildings[i]
	stateID		= state[i]
	retrofit	= building.getRetrofit(stateID)
	building.data["state_retrofit_label"]	= retrofit.description.description
buildings.writeFile("./states/%s.csv" %(params["alias"]))
exit()
stateString	= ",".join([str(i) for i in state])
with open("./england_states.csv", "a") as file:
	file.write(params["alias"] + "," + stateString + "\n")
