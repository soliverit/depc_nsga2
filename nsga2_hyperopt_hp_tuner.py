### Includes ###
## Native 
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
## Project
from lib.retrofit_nsga2		import RetrofitNSGA2
from lib.building_set		import BuildingSet
from lib.cost_problem		import CostProblem

###
# Bayesian optimisation: Tune hyperparameters of NSGA-II using Bayes theorem
##
### Define stuff ###
# Get command line parameters: call "python bayes_optimiser.py -h for details"
params			= RetrofitNSGA2.ParseCMD()
# Load the dataset. Data resides in ./data_samples, the --code parameter defines the file name. E.g mid = mid.csv
buildings		= BuildingSet.LoadDataSet("./data/" + params["dataCode"] + ".csv")
buildingStats	= buildings.getCheapestToRating(params["targetRating"])
buildings.filterRetrofitsByImpactRatio(buildingStats["cost"] / buildingStats["points"] * 2)
buildings.filterZeroOptionBuildings()
buildings.filterHarderMeasures()
# Define the problem
problem				= CostProblem(buildings)
problem.inequality	= problem.buildings.toRatingDifference("D")
# Define the GA. We'll reuse this instead of creating a fresh model for every evaluation
retrofitGA	= RetrofitNSGA2(problem,
	generations=params["generations"],
	crossover=True,	# It tunes crossover params
	crossoverETA=params["crossoverETA"],
	crossoverProb=params["crossoverProb"],
	mutationETA=params["mutationETA"],
	population=params["population"],
	children=params["children"],
	verbose=params["verbose"]
)

### Define evaluation function
def optimise(params):
	global retrofitGA	# Yes, globals are dirty! Very convnient here
	## Reconfigure the GA
	retrofitGA.crossoverETA		= params["crossoverETA"]
	retrofitGA.crossoverProb	= params["crossoverProb"]
	retrofitGA.mutationETA		= params["mutationETA"]
	# Run the GA
	retrofitGA.run()
	# Return the results. The bayes library maximises, so return a negative
	results						= retrofitGA.results.findBest()
	return round(results.score/ results.points)

### Let's do it! ###
# Define the NSGA parameters that'are being tuned. These are for PM crossover and SBX mutation
bounds	= {
	"crossoverProb":	hp.uniform("crossoverProb", 0.7,0.9),
	"crossoverETA":		hp.uniform("crossoverETA", 5, 20),
	"mutationETA": 		hp.uniform("mutationETA", 3, 10)
}
# Define the optimiser

# Define the optimization algorithm
algo = tpe.suggest

# Initialize a Trials object to track the progress
trials = Trials()

# Run the optimization
best = fmin(optimise, bounds, algo=algo, max_evals=200, trials=trials)

print("Best parameters:", best)

