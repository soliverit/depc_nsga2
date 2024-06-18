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
buildings		= BuildingSet.LoadDataSet(params["data"]).getByRatings(["G", "F", "E"])
### For debugging
bPartitions	= round(buildings.length / 5000.0)
# Select the at risk buildings
buildingStats	= buildings.getCheapestToRating("D")
# Prepare problem
inequality		= params["inequality"] if params["inequality"] else  buildings.toRatingDifference("D")
buildings.filterRetrofitsByImpactRatio(buildingStats["cost"] / buildingStats["points"] * 2)
buildings.filterZeroOptionBuildings()
buildings.filterHarderMeasures()
###
from pandas import read_csv
data	= read_csv("./england.csv")
states	= []
from csv import reader
with open("england_states.csv") as file:
	reader = reader(file)
	for row in reader:
		for x in range(len(row) - 1):
			x += 1
			row[x]	= int(row[x])
		states.append(row)
#

if bPartitions < 1:
	bPartitions	= 1
path	= params["data"].replace("c:/workspaces/__sandbox__/depc_england/", "").replace("/retrofits.csv","")
count	= 0
for x in data["Code"]:
	if path in x:
		count	+= 1
sCount	= 0
dStates	= []
for row in states:
	if path in row[0]:
		sCount	+= 1
		dStates.append(row)
if sCount != bPartitions:
	exit()
dStates = sorted(dStates, key=lambda x: int(x[0].split("-")[-1]))
state	=  [item for sublist in dStates for item in sublist]
state.pop(0) # Get rid of label	
print("%s, %s" %(buildings.length, len(state)))
exit()
score	= buildings.scoreState(state)

print("%s, %s" %(score, score["cost"] / score["points"]))