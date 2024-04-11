### Include ###
## Native 
from mealpy.swarm_based.GWO	import OriginalGWO, RW_GWO
## Project
from lib.mealpy_optimiser_base	import MealPyOptimiserBase
class SwarmBased(MealPyOptimiserBase):
	def __init__(self, data, epochs=100, minMax="min", populationSize=50, algorithm=OriginalGWO, varType=IntegerVar, inequality=-1, randomWalk=False):
		super().__init__(data, epochs=epochs, populationSize=populationSize, algorithm=algorithm, inequality=inequality, minMax=minMax, varType=varType	)
		self.customParams["obj_weights"]	= [1.0, 1.0]
	@property
	def upperBounds(self):
		return [building.retrofitCount - 1 for building in self.data]
	@property
	def buildings(self):
		return self.data
	def score(self, solution):
		# Calculate score values
		cost 		= 0
		difference	= 0
		for i in range(len(self.data)):
			retrofit 	= self.buildings[i].getRetrofit(int(solution[i]))
			cost 		+= retrofit.cost
			difference	+= retrofit.difference
		return [cost / difference, self.penalty(difference)]