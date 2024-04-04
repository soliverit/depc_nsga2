### Includes ###
## Native
from sklearn.ensemble	import GradientBoostingRegressor
from hyperopt.hp		import uniform, uniformint
## Project
from lib.estimator_base	import EstimatorBase
class GBDTEstimator(EstimatorBase):
	##
	# Hyperparameters definitions for Hyperopt
	##
	HYPEROPT_HP_TUNER_PARAMS	= {
		"nEstimators": 		uniformint("nEstimators", 500, 2000),
		"learningRate":		uniform("learningRate", 0.01, 0.3),
		"minSampleSplit":	uniformint("minSampleSplit", 5,40),
		"minSamplesLeaf":	uniformint("minSamplesLeaf", 5, 40)
	}
	def __init__(self, data, target, trainTestSplit=0.5, nEstimators=100, learningRate=0.1,
			  minSamplesSplit=30, minSamplesLeaf=24):
		super().__init__(data, target, trainTestSplit=trainTestSplit)
		self.nEstimators		= nEstimators
		self.learningRate		= learningRate
		self.minSamplesSplit	= minSamplesSplit
		self.minSamplesLeaf		= minSamplesLeaf
	@property
	def params(self):
		return {
			"learning_rate": 		self.learningRate,
			"n_estimators":			self.nEstimators,
			"min_samples_split":	self.minSamplesSplit,
			"min_samples_leaf":		self.minSamplesLeaf
		}
	##
	# Train the model
	##
	def train(self):
		self.model	= GradientBoostingRegressor(**self.allParams)
		self.model.fit(self.trainingInputs, self.trainingTargets)
	##
	# Apply CMD parameters to this model (override Abstract)
	##
	def applyCMDParams(self):
		if not hasattr(__class__, "parser"):
			return
		args					= __class__.parser.parse_args()
		self.learningRate		= args.learning_rate		if args.learning_rate else self.learningRate
		self.minSamplesLeaf		= args.min_samples_leaf		if args.min_samples_leaf else self.minSamplesLeaf
		self.minSamplesSplit	= args.min_samples_split	if args.min_samples_split else self.minSamplesSplit
		self.nEstimators		= args.nestimators			if args.n_estimators else self.nEstimators
	##
	# Add CMD parameters to the parser (Virtual)
	## 
	@classmethod
	def AddAdditionalCmdParams(cls):
		cls.parser.add_argument("--learning-rate", type=float, help="Learning rate")
		cls.parser.add_argument("--min-samples-split", type=int, help="Min samples split")
		cls.parser.add_argument("--min-samples-leaf", type=int, help="Min samples leaf")
		cls.parser.add_argument("--n-estimators", type=int, help="No. estimators / rounds")