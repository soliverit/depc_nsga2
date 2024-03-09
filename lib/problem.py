### Includes ###
## Native
import numpy as np
from pymoo.core.problem import ElementwiseProblem

class Problem(ElementwiseProblem):

	def __init__(self, buildings, objectiveFraction=0.95):
		## Set instance stuff
		self.buildings	= buildings
		
		self.total		= float(sum([building.efficiency for building in buildings ]))	
		self.inequality	= self.total * objectiveFraction
		## Prepare stuff
		lowerBounds		= []
		upperBounds		= []
		for building in buildings:
			lowerBounds.append(0)
			upperBounds.append(building.retrofitCount - 1)
		## Super cond--- constructor stuff
		if not hasattr(self, "nObjectives"):
			self.nObjectives	= 1
		if not hasattr(self, "nInequalities"):
			self.nInequalities	= 1
		
		super().__init__(n_var=len(lowerBounds),
			n_obj=self.nObjectives,
			n_ieq_constr=self.nInequalities,
			xl=np.array(lowerBounds),
			xu=np.array(upperBounds),
			vtype=int
		)
	def addBuilding(self, building):
		self.buildings.append(building)
	def maxReduction(self):
		reduction = 0
		for building in self.buildings:
			maxReduction	= 0
			for idx in range(building.retrofitCount):
				if building.getRetrofit(idx).difference > maxReduction:
					maxReduction = building.getRetrofit(idx).difference
			reduction += maxReduction
		return reduction
	def toEDifference(self):
		difference	= 0.0
		for building in self.buildings:
			difference	+= building.toE
		return difference
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
		out["F"]	= [cost]
		out["G"]	= target