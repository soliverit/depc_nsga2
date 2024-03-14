### Includes ###
## Native
import numpy as np
from pymoo.core.problem import ElementwiseProblem
##
# Problem: Base class for DEPC NSGA-II Problems
##
class Problem(ElementwiseProblem):
	def __init__(self, buildings, objectiveFraction=0.95):
		## Set instance stuff
		self.buildings	= buildings
		self.total		= float(sum([building.efficiency for building in buildings ]))	
		self.inequality	= self.total * objectiveFraction
		## Prepare stuff
		##
		# Prepare boundaries for target variables. If there's 10 Buildings,
		# there's 10 variables. Bounds denote Retrofit index for building.getRetrofit(id). Lower
		# bound is always 0, upper bound is building.retrofitCount
		##
		lowerBounds		= []
		upperBounds		= []
		for building in buildings:
			lowerBounds.append(0)
			upperBounds.append(building.retrofitCount - 1)
		## Super cond--- constructor stuff
		# Default number of objectives if it's not defined by the inheriting class
		if not hasattr(self, "nObjectives"):
			self.nObjectives	= 1
		# Default number of constraints if it's not defined by the inheriting class		
		if not hasattr(self, "nInequalities"):
			self.nInequalities	= 1
		# Super, man.	
		super().__init__(n_var=len(lowerBounds),
			n_obj=self.nObjectives,
			n_ieq_constr=self.nInequalities,
			xl=np.array(lowerBounds),
			xu=np.array(upperBounds),
			vtype=int
		)
	##
	# The two-objective score function
	#
	# Objectives:
	#	1: Minimise the cost 
	#
	# Constraints:
	#	1: The number of points reduced much be at least self.inequality
	##
	def _evaluate(self, x, out, *args, **kwargs):
		cost 		= 0
		difference	= 0
		i			= 0
		# Iterate over Buildings and get the Retrofit NSGA says. Sum values
		for building in self.buildings:
			retrofitID	= int(x[i])
			retrofit 	= building.getRetrofit(retrofitID)
			cost 		+= retrofit.cost
			difference	+= retrofit.difference
			i			+= 1
		target 		= 0 if self.inequality < difference else self.inequality - difference
		out["F"]	= [cost / difference, difference]
		out["G"]	= target