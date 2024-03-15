##
# A cheeky struct for aggregated Retrofit results
##
class ScoreStruct():
	def __init__(self):	
		self.cost		= 0.0	# flaot cost of all Retrofits
		self.points		= 0.0	# float points of EPC ratings of retrofitted Building[]
		self.difference	= 0.0	# float difference in points between lodged Building and Retrofit energy efficiency
	##
	# Ratio: Cost / difference
	##
	@property
	def ratio(self):
		return self.cost / self.difference
	##
	# Debugging or something? Print with this.
	##
	def print(self):
		print("Cost:       %s" %(self.cost))
		print("Points:     %s" %(self.points))
		print("Difference: %s" %(self.difference))
		print("Cost:       %s" %(self.ratio))