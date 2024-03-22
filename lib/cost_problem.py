### Imports ###
## Native

## Project
from lib.problem import Problem
from time import time
##
# Cost problem: A problem with cost inequality
##
class CostProblem(Problem):
	##
	# params:
	#	buildings:	BuildingSet
	##
	def __init__(self, buildings, inequality=0):
		## Parameters
		self.nObjectives	= 2
		## Super constructor!
		super().__init__(buildings, inequality=inequality)
		self.shoe = 0
		self.timer = False
	##
	# The two-objective score function (Overridden Abstract)
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
		i			= 0	# micro optimisation for process speed. Really micro but _evaluate's a lot
		for building in self.buildings:
			retrofitID	= int(x[i])	# Fun fact:IntegerRandomSampling is the floored X value and int floors.
			retrofit 	= building.getRetrofit(retrofitID)
			cost 		+= retrofit.cost
			difference	+= retrofit.difference
			i			+= 1
		# The thing we're trying to minimise
		out["F"]	= [cost / difference, difference]
		# The constraint: Anything >= self.inequality is accepted
		out["G"]	= 0 if self.inequality < difference else self.inequality - difference