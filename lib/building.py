### Imports ###
## Native
from math					import floor
## Project
from lib.retrofit_option 	import RetrofitOption
from lib.retrofit			import Retrofit
class Building():
	##
	# Static stuff
	##
	## Members
	RATING_BRACKETS	= {
		"A": {"lower": 92, "upper": 999},
		"B": {"lower": 81, "upper": 91},
		"C": {"lower": 69, "upper": 80},
		"D": {"lower": 55, "upper": 68},
		"E": {"lower": 39, "upper": 54},
		"F": {"lower": 21, "upper": 38},
		"G": {"lower": -999, "upper": 20},
	}
	## Methods
	@staticmethod
	def ratingLowerBound(rating):
		return __class__.RATING_BRACKETS[rating]["lower"]
	@staticmethod
	def ratingUpperBound(rating):
		return __class__.RATING_BRACKETS[rating]["upper"]
	##
	# Instance stuff
	##
	def __init__(self, data, efficiency):
		## Set variables
		self.data		= data
		self.rating		= self.data["CURRENT_ENERGY_RATING"]
		self.area		= float(self.data["TOTAL_FLOOR_AREA"])
		self.efficiency	= efficiency
		self.retrofits	= []
		## Parse retrofits
		# As-built (do nothing)
		retrofit	= Retrofit(
			RetrofitOption.AS_BUILT,
			0,
			0,
			0
		)
		# Building-specific 
		self.addRetrofit(retrofit)
		for key in RetrofitOption.RETROFIT_OPTION_KEYS:
			retrofitOption	= RetrofitOption.RETROFIT_OPTION_DICTIONARY[key]
			efficiency		= floor(float(self.data[retrofitOption.efficiencyKey]))
			# Skip Retrofits that do less than 1 index point of improvement
			if efficiency != -1 and efficiency > self.efficiency:
				cost		= float(self.data[retrofitOption.costKey])
				retrofit	= Retrofit(
					retrofitOption,
					cost,
					round(efficiency),
					round(efficiency - self.efficiency)
				)
				if retrofit.impactRatio < 600:
					self.addRetrofit(retrofit)
		self.retrofits	= sorted(self.retrofits, key=lambda x: x.impactRatio)
	def toRating(self, rating):
		target	= Building.RATING_BRACKETS[rating]["lower"]
		if self.efficiency < target:
			return target - self.efficiency
		return 0
	##
	# Get Retrofit by index
	##
	def getRetrofit(self, id):
		return self.retrofits[id]
	##
	# Add Retrofit: TODO: Check uniqueness
	##
	def addRetrofit(self, retrofit):
		self.retrofits.append(retrofit)
	##
	# Remov Retrofits with a cost and ratio greater than the inputs
	#
	def filterRetrofitsByImpactRatio(self, threshold):
		retrofits	= []
		for retrofit in self.retrofits:
			if retrofit.impactRatio < threshold:
				retrofits.append(retrofit)
		self.retrofits	= retrofits
	# Params:
	#	cost:	float highest acceptable cost
	#	ratio:	float highest acceptable ratio
	##
	def filterRetrofitsByCostAndRatio(self, cost, ratio):
		retrofits	= []
		for retrofit in self.retrofits:
			if retrofit.cost < cost or retrofit.impactRatio < ratio:
				retrofits.append(retrofit)
		self.retrofits	= retrofits
	### Properties
	##
	# Get number of retrofits, including as-built
	##
	@property
	def retrofitCount(self):
		return len(self.retrofits)
	### Retrofit stuff ###
	##
	# Find cheapest option to get to the target efficiency.
	#
	# Params:
	#	efficiency:	int minimum EPC efficiency
	#
	# Output:
	#	Retrofit the cheapest to meet the efficiency OR bool False, no Retrofit found
	##
	def getCheapestRetrofitToEfficiency(self, efficiency):
		result	= False
		cost 	= 9999999999999
		for retrofit in self.retrofits:
			if retrofit.efficiency >= efficiency and retrofit.cost <  cost:
				result	= retrofit
				cost	= retrofit.cost
		return result
	##
	# Get the self.retrofits ID of the cheapest Retrofit to get to the minimum EPC points (efficiency)
	#
	# params:
	#	efficiency:	float/int of minimum EPC efficiency to be achieved
	#
	# output:	int self.retrofits array index
	##
	def getCheapestRetrofitToEfficiencyID(self, efficiency):
		retrofitID	= 0
		cost 	= 9999999999999
		for idx in range(len(self.retrofits)):
			retrofit	= self.retrofits[idx]
			if retrofit.efficiency >= efficiency and retrofit.cost <  cost:
				retrofitID	= idx
		return retrofitID