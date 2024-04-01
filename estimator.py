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

if not isfile(params["data"]):
	print("Error: input data path not found: %s" %(params["data"]))
# Create model
model					= constructor.QuickLoad(params["data"], params["target"])
model.trainTestSplit	= params["train_split"]
model.useCMDParams		= params["use_cmd_config"]
# Print config to console
if not params["no_summary"]:
	model.printModelConfig()
# Load data
# Train 
model.train()
# Test
print(model.test())
