### Includes ###
## Native 
from bayes_opt				import BayesianOptimization
## Project
from lib.nsga2_community	import NSGA2Community
from lib.building_set		import BuildingSet
from lib.cost_problem		import CostProblem

###
# Bayesian optimisation: Tune hyperparameters of NSGA-II using Bayes theorem
##
### Define stuff ###
# Get command line parameters: call "python bayes_optimiser.py -h for details"
params				= NSGA2Community.ParseCMD()
params["stateIdentifier"] = "BEST_TEAM_STATE"
# Load the dataset. Data resides in ./data_samples, the --code parameter defines the file name. E.g mid = mid.csv
buildings			= BuildingSet.LoadDataSet("./data/" + params["dataCode"] + ".csv")
del params["dataCode"]
# Define the problem
problem				= CostProblem(buildings)
problem.inequality	= problem.buildings.toRatingDifference("D")
# Define the GA. We'll reuse this instead of creating a fresh model for every evaluation

### Define evaluation function
def optimise(crossoverETA, crossoverProb, mutationETA):
	global params, buildings	# Yes, globals are dirty! Very convnient here
	params["crossoverETA"]	= crossoverETA
	params["crossoverProb"]	= crossoverProb
	params["mutationETA"]	= mutationETA
	## Reconfigure the GA
	retrofitGA	= NSGA2Community(
		buildings,
		inequality=problem.inequality,	# the CostProblem def of this is redudant for NSGA2Community
		partitions=params["partitions"],
		threadCount=params["threads"],
		flags=params
	)
	# Run the GA
	retrofitGA.run()
	# Return the results. The bayes library maximises, so return a negative
	return - retrofitGA.results.getScoreStruct("BEST_TEAM_STATE").ratio

### Let's do it! ###
# Define the NSGA parameters that'are being tuned. These are for PM crossover and SBX mutation
bounds			= {
	"crossoverProb":(0.7,0.9),
	"crossoverETA": (5, 12),
	"mutationETA": (1, 5)
}
# Define the optimiser
optimiser	= BayesianOptimization(
	f=optimise,
	pbounds=bounds,
	random_state=1,
)
# Run the optimiser. There's no minimise function
optimiser.maximize(
	init_points=20,
	n_iter=200,
)


