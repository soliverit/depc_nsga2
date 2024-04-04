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
### Let's do it! ###
# Create a base estimator
model					= constructor.QuickLoad(params["data"], params["target"])
model.trainTestSplit	= params["train_split"]
model.useCMDParams		= False
# Define the optimiser
def optimise(params):
	global model # Yeah, yeah. Boo global. Saves reloading the data everytime
	for key in list(model.__class__.HYPEROPT_HP_TUNER_PARAMS):
		##
		# Optimisation libraries usually pass float for regardless of the parameter
		# type. Sometimes, they convert to int, if required, during iterations but 
		# forget to when they return the selected parameters.
		#
		# NSGA-II is especially bad. During optimisation, it provides floored floats, then
		# unrounded floats in the final population. Using round() gets the wrong result
		# because int() is equivalent to int(floor(i)). 
		#
		# Anyway, that's why we're doing it here.
		## 
		value = int(params[key]) if int(params[key]) == params[key] else params[key]
		setattr(model, key, value)
	model.train()
	return model.test()["rmse"]

# Run the optimization
best = fmin(
	optimise, 
	constructor.HYPEROPT_HP_TUNER_PARAMS, 
	algo=tpe.suggest,
	max_evals=100, 
	trials=Trials()
)
# Print the parameters so it wasn't for nothing
print("Best parameters:", best)
# Apply parameters and run the model
optimise(best)
model.train()
print(model.test())

