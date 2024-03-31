### Includes ###
## Native 
from os.path			import isfile
from pandas				import read_csv
from hyperopt 			import fmin, tpe, Trials
## Project
from lib.estimator_base	import EstimatorBase
from lib.estimators		import *

# Get constructor. Reads from CMD --constructor arg. Default XGBoostEstimator
constructor	= EstimatorBase.GetConstructor()
params		= constructor.ParseCMD()
# Load data:
if not isfile(params["data"]):
	print("Error: data path doesn't exist: %s" %(params["data"]))
	exit()
data	= read_csv(params["data"])
### Let's do it! ###
# Create a base estimator
model				= constructor(data, params["target"])
model.useCMDParams	= False
# Define the optimiser
def optimise(params):
	global model # Yeah, yeah. Boo global. Saves reloading the data everytime
	for key in list(model.__class__.HYPEROPT_HP_TUNER_PARAMS):
		setattr(model, key, params[key])
	model.train()
	rmse	=  model.test()["rmse"]
	print(rmse)
	return rmse
# Define the optimization algorithm
algo = tpe.suggest

# Initialize a Trials object to track the progress
trials = Trials()

# Run the optimization
best = fmin(optimise, constructor.HYPEROPT_HP_TUNER_PARAMS, algo=algo, max_evals=100, trials=trials)

print("Best parameters:", best)

