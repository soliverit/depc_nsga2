### Includes ###
## Native 
from xgboost				import DMatrix, train
from hyperopt.hp			import uniform, uniformint
## Project
from lib.estimator_base		import EstimatorBase
##
# XGBoost estimator: An estimator using XGBoost 2
##
class XGBoostEstimator(EstimatorBase):
	HYPEROPT_HP_TUNER_PARAMS	= {
		"learningRate":	uniform("learningRate", 0.03, 0.3),
		"rateDrop":		uniform("rateDrop", 0.01, 0.2),
		"skipDrop":		uniform("skipDrop", 0.3, 0.7),
		"maxDepth":		uniformint("maxDepth", 2, 10),
		"nRounds":		uniformint("nRounds", 700, 1200)
	}
	def __init__(self, trainData, target, trainTestSplit=0.5, booster="dart", maxDepth=6,
			  learningRate=0.1, objective="reg:squarederror", sampleType="uniform",
			  normaliseType="tree", rateDrop=0.1, skipDrop=0.5, nRounds=100, gamma=0):
		super().__init__(trainData, target, trainTestSplit=trainTestSplit)
		self.booster		= booster
		self.maxDepth		= maxDepth
		self.learningRate	= learningRate
		self.objective		= objective
		self.sampleType		= sampleType
		self.normaliseType	= normaliseType
		self.rateDrop		= rateDrop
		self.skipDrop		= skipDrop
		self.nRounds		= nRounds
		self.gamma			= gamma
	@property
	def params(self):
		params =  {
			"booster": 			self.booster,
			"max_depth": 		self.maxDepth, 
			"learning_rate":	self.learningRate,
			"objective": 		self.objective,
			"sample_type": 		self.sampleType,
			"normalize_type": 	self.normaliseType,
			"rate_drop": 		self.rateDrop,
			"skip_drop": 		self.skipDrop,
			"gamma":			self.gamma
		}
		if self.booster == "dart":
			params["skip_drop"]	= self.skipDrop
		return params
	def preprocessInputs(self, data):
		if self.target in data:
			del data[self.target]
		return DMatrix(data)
	def train(self):
		# WARNING!!! Always do params first! They change inline configs like train_test_split
		# TODO: Make params use underscore so we don't have to bridge it awkwardly
		params		= self.allParams
		data 		= DMatrix(self.trainingInputs, self.trainingTargets)
		self.model 	= train(params, data, self.nRounds)
	##
	# Extra config params for PrintModelConfig (Virtual)
	##
	def extraConfigParams(self):
		return {
			"nRounds":	self.nRounds
		}
	##
	# Apply CMD parameters (override Abstract)
	##
	def applyCMDParams(self):
		if not hasattr(__class__, "parser"):
			return
		args				= __class__.parser.parse_args()
		self.booster		= args.booster			if args.booster else self.booster
		self.maxDepth		= args.max_depth		if args.max_depth else self.maxDepth
		self.learningRate	= args.learning_rate	if args.learning_rate else self.learningRate
		self.randomState	= args.objective		if args.objective else self.objective
		self.sampleType		= args.sample_type		if args.sample_type else self.sampleType
		self.normaliseType	= args.normalise_type	if args.normalise_type else self.normaliseType
		self.rateDrop		= args.rate_drop		if args.rate_drop else self.rateDrop	
		self.skipDrop		= args.skip_drop		if args.skip_drop else self.skipDrop
		self.nRounds		= args.n_rounds			if args.n_rounds else self.nRounds
		self.gamma			= args.gamma			if args.gamma else self.gamma
	@classmethod
	def AddAdditionalCmdParams(cls):
		cls.parser.add_argument("--booster", type=str,  help="XGBoost booster type")
		cls.parser.add_argument("--max-depth", type=int,  help="")
		cls.parser.add_argument("--learning-rate", type=float,  help="Learning rate")
		cls.parser.add_argument("--objective", type=str,  help="Model objective. Determines if regressor or classifier. E.g reg:sqaurederror for regressor RMSE scored")
		cls.parser.add_argument("--sample-type", type=str,  help="Sampling method. E.g, uniform")
		cls.parser.add_argument("--normalise-type", type=str, help="Normalisation method. E.g, trees" )
		cls.parser.add_argument("--rate-drop", type=float, help="Drop rate")
		cls.parser.add_argument("--skip-drop", type=float,  help="Dart booster, skip drop probability")
		cls.parser.add_argument("--n-rounds", type=int, help="Same as n_estiamtors with GBDT")
		cls.parser.add_argument("--gamma", type=float, help="Minimum loss reduction before further dividing samples again")