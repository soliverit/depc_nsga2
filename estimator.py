### Includes ###
## Native
from pandas								import read_csv
from os.path							import isfile
## Project	
from lib.estimator_base					import EstimatorBase	
from lib.estimators.xgboost_estimator	import XGBoostEstimator

######
# Get the Estimator class: Taken from --constructor flag. Default XGBoostEstimator
constructor	= EstimatorBase.GetConstructor()
# Parse the rest of the CMD flags, including class-specific parameters
params	= constructor.ParseCMD()
# Print config to console
if not params["no_summary"]:
	constructor.PrintConfig()
# Load data
if not isfile(params["data"]):
	print("Error: input data path not found: %s" %(params["data"]))
data				= read_csv(params["data"])
# Create model
model				= constructor(data, params["target"])
model.useCMDParams	= params["use_cmd_config"]
# Train 
model.train()
# Test
print(model.test())
