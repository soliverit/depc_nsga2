### Includes ###
## Native
from sklearn.neural_network import MLPClassifier,MLPRegressor
from sklearn.preprocessing	import Normalizer, StandardScaler
from sklearn.pipeline 		import make_pipeline
### Project
from lib.estimator_base		import EstimatorBase
##
# MLP Estimator - Multilayer-perceptron regression, probably classification
#
# A wrapper for sklearn's MLP. Does regression, probably does classification
# but I haven't tried that, yet.
##
class MLPEstimator(EstimatorBase):
	def __init__(self, data, target, trainTestSplit=0.5, scaler=StandardScaler(), normaliser=Normalizer(),
			  maxIterations=1000, randomState=1, solver="adam", alpha=0.005, layers=False, customParams={},
			  mlpType=MLPRegressor):
		super().__init__(data, target, trainTestSplit=trainTestSplit, scaler=scaler, normaliser=normaliser, customParams=customParams)
		self.maxIterations	= maxIterations	# int max iterations
		self.randomState	= randomState	# int random seed
		self.solver			= solver		# string solver. E.g adam, LBFGS, or stochastic gradient descent
		self.alpha			= alpha			# float regularisation coefficient
		self.mlpType		= mlpType		# MLPRegressor or MLPClassifer
		# Assume 2x features, single layer unless explictly defined
		self.layers	= layers if layers else (len(data.columns) * 2 - 2,)
		# Tell self.preprocessInputs to apply the scaler and normaliser
		self.applyScaler		= True		# bool apply scaler during preprocessing inputs
		self.applyNormaliser	= True		# bool apply normaliser during preprocessing inputs
	##
	# Get params: (override Abstract)
	#
	# output:	dict of parameters defined by instance members
	##
	@property
	def params(self):
		return {
			"hidden_layer_sizes":	self.layers,
			"max_iter":				self.maxIterations,
			"solver":				self.solver,
		}
	##
	# Train model (override Abstract)
	##
	def train(self):
		data	= self.trainingInputs
		# Fit and apply scale and normaliser if they exist
		if self.applyScaler:
			data	= self.scaler.fit_transform(data)
		if self.applyNormaliser:
			data	= self.normaliser.fit_transform(data)
		# Prepare the model
		self.model	= self.mlpType(**self.allParams)
		# Fit the model
		self.model.fit(data, self.trainingTargets)
	##
	# Apply CMD parameters (override Abstract)
	##
	def applyCMDParams(self):
		if not hasattr(__class__, "parser"):
			return
		args				= __class__.parser.parse_args()
		self.alpha			= args.alpha			if args.alpha else self.alpha
		self.solver			= args.solver			if args.solver else self.solver
		self.maxIterations	= args.max_iterations	if args.max_iterations else self.maxIterations
		self.randomState	= args.random_state		if args.random_state else self.randomState

	##
	# Additional CMD arguments (Virtual)
	#
	# Add class-specific CMD arguments to the ArgumentParser.
	##
	@classmethod
	def AddAdditionalCmdParams(cls):
		cls.parser.add_argument("--alpha", type=float, help="Alpha regularisation coefficient")
		cls.parser.add_argument("--solver", type=str,  help="Optimisation algorithm: adam, lbfgs, sgd, rmsprop etc")
		cls.parser.add_argument("--max-iterations", type=int, help="No. iterations")
		cls.parser.add_argument("--random-state", type=int, help="Random seed")