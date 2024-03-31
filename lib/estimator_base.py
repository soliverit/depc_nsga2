### Include ###
## Native
from importlib			import import_module
from inspect			import getmembers, isclass, getmodule
from argparse			import ArgumentParser
from pandas				import read_csv
from sklearn.metrics 	import r2_score, mean_absolute_error, mean_squared_error

## Project
from lib.print_helper	import PrintHelper
##
# Estiamtor base: A class for interchangeable supervised learning models
##
class EstimatorBase():
	CONSTRUCTORS				= {}
	HYPEROPT_HP_TUNER_PARAMS	= {}
	##
	# Get constructor of EstimatorBase child class. E.g, XGBoosterEstimator
	##
	@staticmethod
	def GetConstructor():	
		parser	= ArgumentParser("")
		parser.add_argument("--constructor", type=str, default="XGBoostEstimator", help="Anything from ./lib/estimators/ that doesn't have base in the name.")
		args = parser.parse_known_args()
		constructor = vars(args[0])["constructor"]
		if len(__class__.CONSTRUCTORS) == 0:
			module	= import_module("lib.estimators")
			for name, obj in getmembers(module):
				if isclass(obj) and issubclass(obj, __class__):
					__class__.CONSTRUCTORS[name] = obj
		return __class__.CONSTRUCTORS[constructor]
	@classmethod
	def QuickLoad(cls, path, target):
		return cls(read_csv(path), target)
	##
	# params:
	#	trainData:			DataFrame
	#	target:				string feature name (of column in trainData)
	#	trainTestSplit:		float 0 < x < 1 split of data for training and testing. x = train size
	##
	def __init__(self, trainData, target, trainTestSplit=0.5):
		self.data		= trainData
		self.target			= target
		self.trainTestSplit	= trainTestSplit
		self.model			= False
	##
	# Get training data  with target
	##
	@property
	def trainingData(self):
		return self.data[: int(len(self.data) * self.trainTestSplit)]
	@property
	def testData(self):
		return self.data[int(len(self.data) * self.trainTestSplit) : ]
	@property
	def trainingInputs(self):
		data	= self.trainingData[: int(len(self.data) * self.trainTestSplit)]
		del data[self.target]
		return data
	@property
	def testInputs(self):
		data	= self.trainingData[int(len(self.data) * self.trainTestSplit) : ]
		del data[self.target]
		return data
	@property
	def trainingTargets(self):
		return self.data[self.target].values[:  int(len(self.data) * self.trainTestSplit)]
	@property
	def testTargets(self):
		return self.data[self.target].values[ int(len(self.data) * self.trainTestSplit) : ]
	def train(self):
		raise "%s doesn't override abstract train method of EstimatorBase" %(__class__.__name__)
	def params(self):
		raise "%s doesn't override abstract params method of EstimatorBase" %(__class__.__name__)
	def toDataFrame(self, data):
		return data	# TODO: Virtual method for XGB using a custom data handler
	def test(self):
		if not self.model:
			self.train()
		predictions	= self.predict(self.testInputs)
		return {
			"r2":	r2_score(predictions, self.testTargets),
			"rmse":	mean_squared_error(predictions, self.testTargets) ** 0.5,
			"mae":	mean_absolute_error(predictions, self.testTargets)
		}
	def predict(self, data):
		return self.model.predict(data)
	def r2(self, data, targets):
		return r2_score(self.predict(data), targets)
	def rmse(self, data, targets):
		return mean_squared_error(self.predict(data), targets) ** 0.5
	def mae(self, data, targets):
		return mean_absolute_error(self.predict(data), targets)
	################
	# Argument parsing
	################
	@classmethod
	def PrintConfig(cls):
		config	= vars(cls.parser.parse_args())
		length	= 0
		for key in list(config):
			if length < len(key):
				length = len(key)
		for key in list(config):
			print(PrintHelper.PadArray([key, config[key]], length + 1))	
	##
	# The Parser method for all children
	##
	@classmethod
	def ParseCMD(cls):
		cls.parser	= ArgumentParser("Estimator arg parser")
		cls.AddAdditionalCmdParams()
		cls.parser.add_argument("--data", type=str, default="./data/estimator_depc_example.csv",  help="Path to .csv file or whatever if you're using something like xgboos with custom data handlers")
		cls.parser.add_argument("--target", type=str, default="CURRENT_ENERGY_EFFICIENCY", help="Name of the feature we're trying to estimate")
		cls.parser.add_argument("--train-split", type=float, default=0.5, help="Test train split: 0 < split < 1")
		cls.parser.add_argument("--no-summary",  default=False, help="Print estimator config.", action="store_true")
		cls.parser.add_argument("--constructor", type=str, default="XGBoostEstimator", help="Estimator constructor name: Anything from ./lib/estimators/")
		return vars(cls.parser.parse_args())