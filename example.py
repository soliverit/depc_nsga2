### Includes ###
## Native 
import argparse
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
params			= RetrofitNSGA2.ParseCMD()
# Verify
dataPath		= "./data/" + params["dataCode"] + ".csv"
if not isfile(dataPath):
	print("Data path: " + dataPath + " not found")
	exit()
#############################
#    The actual example     #
#############################
# Load data
buildings			= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E", "D"])
# Prepare problem
problem				= CostProblem(buildings)
problem.inequality	= problem.buildings.toRatingDifference("D")
##
# Build the algorithm
#
# Note: parameters can be defined outside the constructor
# using property names. E.g, retrofitGA.generations = 1000
##
retrofitGA	= RetrofitNSGA2(problem,
	generations=params["generations"],
	crossover=params["crossover"],
	crossoverETA=params["crossoverETA"],
	crossoverProb=params["crossoverProb"],
	mutationETA=params["mutationETA"],
	population=params["population"],
	children=params["children"],
	callback= Historian() if params["callback"] else False,
	verbose=params["verbose"]
)
retrofitGA.printBenchmark()
retrofitGA.run()
retrofitGA.printResults()
if params["historyPath"]:
	retrofitGA.writeHistory(params["historyPath"])
