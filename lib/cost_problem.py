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
	##
	# The two-objective score function
	#
	# Objectives:
	#	1: Minimise the cost to EPC point difference ratio
	#	2: Minimise the number of points reduced considerate of the constraint.
	#
	# Constraints:
	#	1: The number of points reduced much be at least self.inequality
	##
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
		# The constraint: Anything >= self.inequality is accepted
		target 		= 0 if self.inequality < difference else self.inequality - difference
		# The thing we're trying to minimise
		out["F"]	= [cost / difference, difference]
		# The constraint (inequality)
		out["G"]	= target