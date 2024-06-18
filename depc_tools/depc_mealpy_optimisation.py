### Include ###
## Native 
# from mealpy.swarm_based.GWO	import OriginalGWO
from mealpy					import IntegerVar
## Project
from lib.mealpy_optimiser_base	import MealPyOptimiserBase

class DEPCMealPyOptimiser(MealPyOptimiserBase):
	def __init__(self, data, epochs=100, minMax="min", population=50, 
			  algorithm=False,inequality=-1, customParams={}):
		super().__init__(data, epochs=epochs, population=population, algorithm=algorithm, customParams=customParams, inequality=inequality, minMax=minMax, varType=IntegerVar	)
		self.customParams["obj_weights"]	= [1.0, 1.0]
	@property	# Overriden Abstract 
	def upperBounds(self):
		return [building.retrofitCount - 1 for building in self.data]
	@property	# Forwarder for project context
	def buildings(self):
		return self.data
	##
	# Update a hyperparameter (Duck typing magic)
	#
	# HyperoptHpTunerBase has a method that updates hyperparameters. In some cases,
	# it can just call setattr, like with NSGA-II, since the object has members that
	# define the hyperparameters. However, this object doesn't know the hyperparameters
	# because it doesn't extend MealPy constructors, it is passed one an a member. So, 
	# we can't define the parameters as members. Instead, we use self.customParams.
	#
	# We can't use setattr() because it can't tell the difference between internal and 
	# external declarations, so we use self.customParams to store hyperparameters.
	#
	# So... defining this method HyperoptHpTunerBase to use this method instead of setattr().
	##
	def updateHyperparameter(self, key, value):
		self.customParams[key]	= value
	def penalty(self, value):
		if self.inequality	== -1:
			return 0
		return 0 if self.inequality < value else self.inequality - value
	def score(self, solution):	# Overriden Abstract
		cost 		= 0
		difference	= 0
		# windowCount	= 0
		for i in range(len(self.data)):
			retrofit 	= self.buildings[i].getRetrofit(int(solution[i]))
			cost 		+= retrofit.cost
			difference	+= retrofit.difference
			# if retrofit.hasHotwater:
			# 	windowCount	+= 1
		return [cost / difference, self.penalty(difference)]
		# return [cost / difference, self.penalty(difference), (	float(windowCount) / len(self.data)) * 100]