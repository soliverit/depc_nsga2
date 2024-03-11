### Includes ###
## Native 
from bayes_opt				import BayesianOptimization
## Project
from lib.retrofit_nsga2		import RetrofitNSGA2
from lib.building_set		import BuildingSet
from lib.cost_problem		import CostProblem

###
# Bayesian optimisation: Tune hyperparameters of NSGA-II using Bayes theorem
##
### Define stuff ###
# Get command line parameters: call "python bayes_optimiser.py -h for details"
params				= RetrofitNSGA2.ParseCMD()
# Load the dataset. Data resides in ./data_samples, the --code parameter defines the file name. E.g mid = mid.csv
buildings			= BuildingSet.LoadDataSet("./data/" + params["dataCode"] + ".csv")
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
def optimise(crossoverETA, crossoverProb, mutationETA):
	global retrofitGA	# Yes, globals are dirty! Very convnient here
	## Reconfigure the GA
	retrofitGA.crossoverETA		= crossoverETA
	retrofitGA.crossoverProb	= crossoverProb
	retrofitGA.mutationETA		= mutationETA
	# Run the GA
	retrofitGA.run()
	# Return the results. The bayes library maximises, so return a negative
	results						= retrofitGA.getResult()
	return - int(round(results["cost"] / results["points"]))

### Let's do it! ###
# Define the NSGA parameters that'are being tuned. These are for PM crossover and SBX mutation
bounds			= {
	"crossoverProb":(0.7,0.9),
	"crossoverETA": (10, 25),
	"mutationETA": (5, 10)
}
# Define the optimiser
optimiser	= BayesianOptimization(
	f=optimise,
	pbounds=bounds,
	random_state=1,
)
# Run the optimiser. There's no minimise function
optimiser.maximize(
	init_points=5,
	n_iter=200,
)


