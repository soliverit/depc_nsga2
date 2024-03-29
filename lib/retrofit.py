##
# Struct for Retrofit information
##
class Retrofit():
	def __init__(self, description, cost, efficiency, difference):
		self.description	= description									# RetrofitOption
		self.cost			= cost											# float cost
		self.efficiency		= efficiency									# int EPC efficiency
		self.difference		= difference									# int difference between Building's and this Retrofit's rating
		self.impactRatio	= cost / difference if difference > 0 else 0	# float cost to difference ratio
	### Forwarding methods ###
	##
	# Get number of measures in this Retrofit:
	#
	# Output:	int Number of measures as defined by the RetrofitOption
	##
	@property
	def measureCount(self):
		return self.description.measureCount
	@property
	def hasRoof(self):
		return self.description.hasRoof
	@property
	def hasHotwater(self):
		return self.description.hasHotwater
	@property
	def hasEnvelopes(self):
		return self.description.hasEnvelopes
	@property
	def hasWindows(self):
		return self.description.hasWindows
	@property
	def name(self): #TODO: Change so .name is also on RetrofitOption
		return self.description.description 