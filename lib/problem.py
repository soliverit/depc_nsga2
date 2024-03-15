### Includes ###
## Native
import numpy as np
from pymoo.core.problem import ElementwiseProblem
##
# Problem: Base class for DEPC NSGA-II Problems
##
class Problem(ElementwiseProblem):
	def __init__(self, buildings, inequality=0):
		## Set instance stuff
		self.buildings	= buildings		# BuildingSet
		self.inequality	= inequality	# float minimum EPC points saved. Both constraint and objective
		### Prepare stuff ###
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
		### Super cond--- constructor stuff ###
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
	# The two-objective score function (Abstract)
	#
	# Objectives:
	#	1: Minimise the cost 
	#
	# Constraints:
	#	1: The number of points reduced much be at least self.inequality
	#
	# params:
	#	x:		np.array of floored np.float64. Each a Retrofit ID for an nth Building in self.buildings
	#	out:	dictionary {"F":(array or float) ,"G": (array or float)}. F is objective scores. G is constrain scores
	#	args:	dictionary. Never used single *, don't use it here. But the NSGA2 documentation uses it
	#	kwargs:	dictionary of args. Not used but present in the documentation.
	##
	def _evaluate(self, x, out, *args, **kwargs):
		raise "Abstract Problem _evaluate method not overridden"