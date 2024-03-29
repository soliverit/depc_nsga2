### Includes ###
## Native 

from random 						import random
from os.path						import isfile
## Project
from lib.cost_problem				import CostProblem
from lib.building_set				import BuildingSet
from lib.retrofit_nsga2				import RetrofitNSGA2
from lib.historian					import Historian

#############################
#  Command line parameters  #
#############################
# Parse
params		= RetrofitNSGA2.ParseCMD()
## File path stuff
# The alias for files
dataCode	= "./data/" + params["dataCode"] 
# The input data path
dataPath	= dataCode + ".csv"
# The post-process state path. Write the BuildingSet with optimal state included
statePath	= dataCode + ".stt"
# Make sure the input actually exists
if not isfile(dataPath):
	print("Data path: " + dataPath + " not found")
	exit()
#############################
#    The actual example     #
#############################
# Load data
buildings		= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E"])
# Select the at risk buildings
buildingStats	= buildings.getCheapestToRating(params["targetRating"])
# Prepare problem
inequality		= params["inequality"] if params["inequality"] else  buildings.toRatingDifference(params["targetRating"])
buildings.filterRetrofitsByImpactRatio(buildingStats["cost"] / buildingStats["points"] * 2)
buildings.filterZeroOptionBuildings()
buildings.filterHarderMeasures()
problem		= CostProblem(buildings, inequality)

##
# Build the algorithm
#
# Note: parameters can be defined outside the constructor
# using property names. E.g, retrofitGA.generations = 1000
##
# Create initial states
bestInitialState	= buildings.getCheapestToRatingState("D")
initialStates		= []

if params["bestInitialStates"]:
	for i in range(params["population"]):
		if  params["stateIdentifier"]:
			for building in buildings:
				if random() >  0.005:
					initialStates.append(int(building.data[params["stateIdentifier"]]))
				else:
					initialStates.append(0)
		else:
			for v in bestInitialState:
				if random() >  0.3:
					initialStates.append(v)
				else:
					initialStates.append(0)
	initialStates	= np.array(initialStates)
# Build it.
retrofitGA	= RetrofitNSGA2(problem,
	generations=params["generations"],
	initialStates=initialStates,
	crossover=params["crossover"],
	crossoverETA=params["crossoverETA"],
	crossoverProb=params["crossoverProb"],
	mutationETA=params["mutationETA"],
	population=params["population"],
	children=params["children"],
	callback=Historian() if params["historyPath"] else False,
	verbose=params["verbose"]
)
if not params["silent"]:
	retrofitGA.printBenchmark()
retrofitGA.run()
if not params["silent"]:
	retrofitGA.printResults()
if params["historyPath"]:
	retrofitGA.writeHistory(params["historyPath"])
if params["writeState"]:
	retrofitGA.writeState(statePath)
