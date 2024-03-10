### Imports ###
## Native

## Project
from lib.problem import Problem

##
# Cost problem: A problem with cost inequality
##
class CostProblem(Problem):
	def __init__(self, buildings, objectiveFraction=0.95):
		## Parameters
		self.nObjectives	= 2
		## Super constructor!
		super().__init__(buildings, objectiveFraction)
		
	def _evaluate(self, x, out, *args, **kwargs):
		cost 		= 0
		difference	= 0
		i			= 0
		for building in self.buildings:
			retrofitID	= int(x[i])
			retrofit 	= building.getRetrofit(retrofitID)
			cost 		+= retrofit.cost
			difference	+= retrofit.difference
			i			+= 1
		
		target 		= 0 if self.inequality < difference else self.inequality - difference
		out["F"]	= [cost / difference, difference]
		out["G"]	= target