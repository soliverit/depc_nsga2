### Includes ###
## Native 
from xgboost				import DMatrix, train
from hyperopt.hp			import uniform, uniformint
## Project
from lib.estimator_base	import EstimatorBase
##
# XGBoost estimator: An estimator using XGBoost 2
##
class XGBoostEstimator(EstimatorBase):
	HYPEROPT_HP_TUNER_PARAMS	= {
		"learningRate":	uniform("learningRate", 0.01, 0.5),
		"rateDrop":		uniform("rateDrop", 0.01, 0.25),
		"skipDrop":		uniform("skipDrop", 0.3, 0.7),
		"maxDepth":		uniformint("maxDepth", 2, 20),
		"nRounds":		uniformint("nRounds", 500, 501)
	}
	def __init__(self, trainData, target, trainTestSplit=0.5):
		super().__init__(trainData, target, trainTestSplit=trainTestSplit)
		self.booster		= "dart"
		self.maxDepth		= 5
		self.learningRate	= 0.05
		self.objective		= "reg:squarederror"
		self.sampleType		= "uniform"
		self.normaliseType	= "tree"
		self.rateDrop		= 0.08
		self.skipDrop		= 0.4
		self.nRounds		= 2000
	@property
	def params(self):
		if self.__class__.parser and self.useCMDParams:
			properties	= vars(self.__class__.parser.parse_args())
			params = {
				"booster": 			properties["booster"],
				"max_depth": 		properties["max_depth"], 
				"learning_rate":	properties["learning_rate"],
				"objective": 		properties["objective"],
				"sample_type": 		properties["sample_type"],
				"normalize_type": 	properties["normalise_type"],
				"rate_drop": 		properties["rate_drop"],
			}
			self.nRounds	= properties["n_rounds"]
			if params["booster"] == "dart":
				params["skip_drop"]	= properties["skip_drop"]
		else:
			params =  {
				"booster": 			self.booster,
				"max_depth": 		self.maxDepth, 
				"learning_rate":	self.learningRate,
				"objective": 		self.objective,
				"sample_type": 		self.sampleType,
				"normalize_type": 	self.normaliseType,
				"rate_drop": 		self.rateDrop,
				"skip_drop": 		self.skipDrop
			}
			if params["booster"] == "dart":
				params["skip_drop"]	= self.skipDrop
		return params
	@property
	def trainingInputs(self):
		data	= self.trainingData[: int(len(self.data) * self.trainTestSplit)]
		del data[self.target]
		return data
	@property
	def testInputs(self):
		data	= self.data[int(len(self.data) * self.trainTestSplit) : ]
		del data[self.target]
		return DMatrix(data)
	def train(self):
		data 		= DMatrix(self.trainingInputs, self.trainingTargets)
		self.model 	= train(self.params, data, self.nRounds)
	@classmethod
	def AddAdditionalCmdParams(cls):
		cls.parser.add_argument("--booster", type=str, default="dart", help="XGBoost booster type")
		cls.parser.add_argument("--max-depth", type=int, default=5, help="XGBoost booster type")
		cls.parser.add_argument("--learning-rate", type=float, default=0.1, help="Learning rate")
		cls.parser.add_argument("--objective", type=str, default="reg:squarederror", help="Model objective. Determines if regressor or classifier. E.g reg:sqaurederror for regressor RMSE scored")
		cls.parser.add_argument("--sample-type", type=str, default="uniform", help="Sampling method. E.g, uniform")
		cls.parser.add_argument("--normalise-type", type=str, default="tree", help="Normalisation method. E.g, trees" )
		cls.parser.add_argument("--rate-drop", type=float, default=0.1, help="Drop rate")
		cls.parser.add_argument("--skip-drop", type=float, default=0.5, help="Dart booster, skip drop probability")
		cls.parser.add_argument("--n-rounds", type=int, default=100, help="Same as n_estiamtors with GBDT")
