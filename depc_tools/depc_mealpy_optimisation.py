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
	def penalty(self, value):
		if self.inequality	== -1:
			return 0
		return 0 if self.inequality < value else self.inequality - value
	def score(self, solution):	# Overriden Abstract
		cost 		= 0
		difference	= 0
		for i in range(len(self.data)):
			retrofit 	= self.buildings[i].getRetrofit(int(solution[i]))
			cost 		+= retrofit.cost
			difference	+= retrofit.difference
		return [cost / difference, self.penalty(difference)]