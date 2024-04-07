### Include ###
## Native 
from mealpy.swarm_based.GWO	import OriginalGWO, RW_GWO
from mealpy					import IntegerVar
## Project
from lib.mealpy_optimisers.mealpy_swarm_optimiser_base	import MealPySwarmOptimiserBase
class DEPCMealPyOptimiser(MealPySwarmOptimiserBase):
	def __init__(self, data, epochs=100, minMax="min", populationSize=50, 
			  algorithm=OriginalGWO,inequality=-1, customParams={}):
		super().__init__(data, epochs=epochs, populationSize=populationSize, algorithm=algorithm, customParams=customParams, inequality=inequality, minMax=minMax, varType=IntegerVar	)
		self.customParams["obj_weights"]	= [1.0, 1.0]
	@property	# Overriden Abstract 
	def upperBounds(self):
		return [building.retrofitCount - 1 for building in self.data]
	@property
	def buildings(self):
		return self.data
	def score(self, solution):	# Overriden Abstract
		# Calculate score values
		cost 		= 0
		difference	= 0
		for i in range(len(self.data)):
			retrofit 	= self.buildings[i].getRetrofit(int(solution[i]))
			cost 		+= retrofit.cost
			difference	+= retrofit.difference
		return [cost / difference, self.penalty(difference)]