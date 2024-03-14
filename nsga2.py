### Includes ###
## Native 
import argparse
import numpy as np
from os.path						import isfile
from os.path 						import isfile
## Project
from lib.building					import Building
from lib.problem					import Problem
from lib.cost_problem				import CostProblem
from lib.building_set				import BuildingSet
from lib.retrofit_nsga2				import RetrofitNSGA2
from lib.print_helper				import PrintHelper
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
buildings			= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E"])
# Select the at risk buildings
buildingStats		= buildings.getCheapestToRating("D")

# Prepare problem
inequality			= buildings.toRatingDifference("D")
buildings.filterRetrofitsByImpactRatio(600)
buildings.filterZeroOptionBuildings()
problem				= CostProblem(buildings)
problem.inequality	= inequality

##
# Prepare solution space
##
# Anything above double the base object isn't a good fit

##
# Build the algorithm
#
# Note: parameters can be defined outside the constructor
# using property names. E.g, retrofitGA.generations = 1000
##
# Create initial states
bestInitialState	= buildings.getCheapestToRatingState("D")
initialStates		= []
from random import random
if params["bestInitialStates"]:
	for i in range(params["population"]):
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
retrofitGA.printBenchmark()
retrofitGA.run()
retrofitGA.printResults()
if params["historyPath"]:
	retrofitGA.writeCSVRow(params["historyPath"])
if params["writeState"]:
	retrofitGA.writeState(statePath)
