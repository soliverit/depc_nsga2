##
# A simple struct for NSGA-II results
##
class ResultStruct():
	##
	# params:
	#	cost:		float/int cost of implementing all selected measures
	#	points:		int points improvement from baseline
	#	states:		int[] Retrofit states for the Buildings from NSGA-II
	#	objectives:	float[] objective scores from NSGA-II
	##
	def __init__(self, cost, points, states, objectives):
		self.cost		= cost			# float
		self.points		= points		# int
		self.score		= cost / points	# float 
		self.states		= states		# int[]
		self.objectives	= objectives	# float[]