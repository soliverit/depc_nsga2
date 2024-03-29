### Includes ###
## Native 

## Project
from lib.result_struct	import ResultStruct
##
# A set for ResultStructs so we can keep track of the
# Buildings the state applies to without cloning the
# BuildingSet for every ResultStruct
##
class ResultStructSet():
	##
	# params:
	#	buildings:	BuildingSet of Buildings the state ResultStruct states applies to
	##
	def __init__(self, buildings):
		self.buildings		= buildings
		self.resultStructs	= []
		self._best			= False
	##
	# Add a ResultStruct to the set. Please only add related structs!
	##
	def addResultStruct(self, resultStruct):
		self.resultStructs.append(resultStruct)
		self._best	= False
	##
	# Add ResultStruct from parameterss
	#
	# params:
	#	buildings: 	BuildingSet of related Buildings
	#	cost:		float/int cost of implementing the state
	#	points:		int EPC index point difference from as-built state
	#	states:		int[] Building Retrofit indices from NSGA-II
	#	objectivs:	float[] Objective scores from NSGA-II
	##
	def add(self, cost, points, states, objectives):
		self.addResultStruct(ResultStruct(
			cost,
			points,
			states,
			objectives
		))
		self._best	= False
	##
	# Find Best - (virtaul)
	#
	# Find the best solution. This implementation uses lowest cost, but feel
	# free to override the function with whatever.
	#
	# output:	ResultStruct best fit for the fitnes criteria
	##
	def findBest(self):
		# Return the cached result if it exists
		if self._best:
			return self._best
		# Find the best
		self._best	= self.resultStructs[0]
		for resultStruct in self.resultStructs:
			if resultStruct.cost < self._best.cost:
				self._best	= resultStruct
		return self._best
	### Magic methods ###
	##
	# Subscripted access: Read like an array
	#
	# params:
	#	idx:	int ResultStruct index
	#
	# output:	ResultSet at position idx
	##
	def __getitem__(self, idx):
		return self.resultStructs[idx]