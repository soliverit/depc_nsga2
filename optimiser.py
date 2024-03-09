### Imports ###
## Native
from bayes_opt 			import BayesianOptimization

## Project
from lib.building_set	import BuildingSet
from lib.retrofit_nsga2	import RetrofitNSGA2
from lib.problem		import Problem
from lib.cost_problem	import CostProblem
from lib.building		import Building

def optimise(crossoverRate, crossoverETA, mutationETA):
	global nsga2
	nsga2.crossoverRate	= crossoverRate
	nsga2.crossoverETA	= crossoverETA
	nsga2.mutationETA	= mutationETA

	nsga2.prepareAlgorithm()
	nsga2.run()
	result	= nsga2.getResult()
	return - round(result["cost"] / 1000)

#############################################
#	Let's do this
#############################################
### Variables  etc ###
dataPath	= 'c:/workspaces/__sandbox__/depc/small_retrofits.csv'
### Get the data ###
buildings	= BuildingSet.LoadDataSet(dataPath)

### Retrofit filtering ###
noImpactCount	= 0
highestCost		= 0
highestRatio	= 0
targetBuildings	= buildings.getByRatings(["F", "E"])
for building in targetBuildings:
	retrofit	= building.getCheapestRetrofitToEfficiency(Building.ratingLowerBound("D"))
	## Best case stuff
	if retrofit:
		if highestCost < retrofit.cost:
			highestCost = retrofit.cost
		if highestRatio < retrofit.impactRatio:
			highestRatio	= retrofit.impactRatio
for building in buildings:
	building.filterRetrofitsByCostAndRatio(highestCost, highestRatio)
### The problem ###
problem				= CostProblem(buildings)
problem.inequality	= problem.buildings.toRatingDifference("D")
### The algorithm ###
nsga2				= RetrofitNSGA2(problem)
nsga2.generations	= 5000
### Bayes boundaries ###
params			= {
	"crossoverRate":(0.7,0.9),
	"crossoverETA": (10, 25),
	"mutationETA": (7.7, 8.25)
}
### Do the thing! ###
optimiser	= BayesianOptimization(
    f=optimise,
    pbounds=params,
    random_state=1,
)
optimiser.maximize(
    init_points=5,
    n_iter=200,
)