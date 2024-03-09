### Includes ###
## Native 
import csv
import time
from pymoo.algorithms.moo.nsga2 	import NSGA2
from pymoo.operators.crossover.sbx 	import SBX
from pymoo.operators.mutation.pm 	import PM
from pymoo.operators.sampling.rnd 	import IntegerRandomSampling
from pymoo.optimize 				import minimize
from pymoo.termination 				import get_termination
## Project
from lib.building					import Building
from lib.problem					import Problem
from lib.cost_problem				import CostProblem
from lib.building_set				import BuildingSet
from lib.retrofit_nsga2				import RetrofitNSGA2
from lib.print_helper				import PrintHelper





#############################################
#	Let's do this
#############################################
### Variables  etc ###
dataPath	= 'c:/workspaces/__sandbox__/depc/mid_retrofits.csv'
### Get the data ###
buildings	= BuildingSet.LoadDataSet(dataPath)
### Print Problem stats ###
cost 			= 0.0
metPoints		= 0.0
allPoints		= 0.0
noImpactCount	= 0
highestCost		= 0
highestRatio	= 0
targetBuildings	= buildings.getByRatings(["F", "E"])
for building in targetBuildings:
	allPoints	+= building.toRating("D")
	retrofit	= building.getCheapestRetrofitToEfficiency(Building.ratingLowerBound("D"))
	## Best case stuff
	if retrofit:
		cost 		+= retrofit.cost
		metPoints	+= retrofit.difference
		if highestCost < retrofit.cost:
			highestCost = retrofit.cost
		if highestRatio < retrofit.impactRatio:
			highestRatio	= retrofit.impactRatio
	## Average stuff
		
for building in buildings:
	building.filterRetrofitsByCostAndRatio(highestCost, highestRatio)
print(buildings.length)
buildings.filterZeroOptionBuildings()
print(buildings.length)



###################		
### The problem ###
problem				= CostProblem(buildings)
problem.inequality	= problem.buildings.toRatingDifference("D")
print("--- Objective ---")
padSize	= 14
print(PrintHelper.padArray(["Buildings:", targetBuildings.length], padSize))	
print(PrintHelper.padArray(["Target:", problem.inequality], padSize))	
print("--- Cheapest at risk ---")
print(PrintHelper.padArray(["Cost:", cost], padSize))
print(PrintHelper.padArray(["Points:", metPoints], padSize))
print(PrintHelper.padArray(["Points all:", allPoints], padSize))
print(PrintHelper.padArray(["Ratio:", round(cost / metPoints, 2)], padSize))
print(PrintHelper.padArray(["Ratio all:", round(cost / allPoints, 2)], padSize))


# exit()
# print(problem.total)
# print(problem.maxReduction())
# print(problem.total - problem.maxReduction())
# print(problem.maxReduction() / problem.total)
# exit()
### Define the algorithm and termination criterion ###
## Algorithm
algorithm = NSGA2(
	pop_size=200,
	n_offsprings=80,
	sampling=IntegerRandomSampling(),
	crossover=SBX(prob=0.7257, eta=15.),
	mutation=PM(eta=12.014),
	eliminate_duplicates=True
)
### Termination ###
termination = get_termination("n_gen", 5000)

### Do the thing ###
start	= time.time()
res = minimize(
	problem,
	algorithm,
	termination,
	seed=1,
	save_history=False,
	verbose=False
)
X = res.X
F = res.F


cost	= 0.0
points	= 0.0
import math
for idx in range(len(X[-1])):
	x			= math.floor(X[-1][idx])
	building	= problem.buildings.buildings[idx]
	retrofit 	= building.getRetrofit(x)
	cost 		+= retrofit.cost
	points		+= retrofit.difference
print("--- Optimised ---")
print("Cost:   %s" %(round(cost)))
print("Points: %s" %(round(points)))
print("Ratio:  %s" %(round(cost / points, 2)))
print("Time:   %s" %(round(time.time() - start)))
