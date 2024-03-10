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
				self.addRetrofit(retrofit)
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
	##
	def filterRetrofitsByCostAndRatio(self, cost, ratio):
		retrofits	= []
		for retrofit in self.retrofits:
			if retrofit.cost < cost or retrofit.impactRatio < ratio:
				retrofits.append(retrofit)
		self.retrofits	= retrofits
	##
	#
	##
	def filterByRatioCountOrder(self):
		retrofits = [[],[], [], []]
		for retrofit in self.retrofits:
			if retrofit.measureCount == 0:
				continue
			retrofits[retrofit.measureCount - 1].append(retrofit)
		for rowID1 in range(3):
			row1	= retrofits[rowID1]
			for rowID2 in range(3 - rowID1):
				row2	= retrofits[rowID2 + rowID1]
				for retrofitID in range(len(row1)):
					retrofit1	= row1[retrofitID]
					retrofit2	= row2[retrofitID]
				for rID in range(len(row2)):
					if retrofit1.cost < retrofit2.cost and retrofit1.difference <= retrofit2.difference:
						print("%s %s %s %s" %(retrofit1.cost, retrofit2.cost, retrofit1.cost, retrofit2.cost))
						
			

	##
	# Get number of retrofits, including as-built
	##
	@property
	def retrofitCount(self):
		return len(self.retrofits)
	### Retrofit stuff ###
	##
	# Find cheapest option to get to the target efficiency
	##
	def getCheapestRetrofitToEfficiency(self, efficiency):
		result	= False
		cost 	= 9999999999999
		for retrofit in self.retrofits:
			if retrofit.efficiency >= efficiency and retrofit.cost <  cost:
				result	= retrofit
				cost	= retrofit.cost
		return result