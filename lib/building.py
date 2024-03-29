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
		self.data			= data									# {} miscellaneous from .csv: default string
		self.rating			= self.data["CURRENT_ENERGY_RATING"]	# char current EPC rating
		self.area			= float(self.data["TOTAL_FLOOR_AREA"])	# float net internal area
		self.efficiency		= efficiency							# float/int current EPC index
		self.retrofits		= []									# Retrofit[]
		self.retrofitHash 	= {}
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
			retrofit	= Retrofit(
				retrofitOption,
				float(self.data[retrofitOption.costKey]),
				round(efficiency),
				round(efficiency - self.efficiency)
			)
			self.addRetrofit(retrofit)
		self.retrofits	= sorted(self.retrofits, key=lambda x: x.impactRatio)
	##
	# Determine the number of EPC index points the building's rating needs to be increased
	# by to bring it's rating to the target rating
	#
	# Params:
	#	rating:	char rating [A through F] target EPC rating
	#
	# Output:	int difference between target and existing. If result < 0, returns 0
	##
	def toRating(self, rating):
		target	= Building.RATING_BRACKETS[rating]["lower"]
		if self.efficiency < target:
			return target - self.efficiency
		return 0
	##
	# Get Retrofit by index
	#
	# Params:
	#	id:	int Retrofit array index
	##
	def getRetrofit(self, id):
		return self.retrofits[id]
	##
	# Add Retrofit: TODO: Check uniqueness
	#
	# Params:
	#	retrofit:	Retrofit that should be for this Building
	##
	def addRetrofit(self, retrofit):
		# We only want to keep sensible Retrofits in the set
		if retrofit.efficiency != -1:
			if retrofit.efficiency > self.efficiency: 
				self.retrofits.append(retrofit)
			# We keep everything in case we need it because even though
			# some Retrofit have a point difference < 1 in isolation, they
			# might have a synergistic relationship with others. It's EPC, 
			# so counterintuitive synergies aren't off the table.
			self.retrofitHash[retrofit.name]	= retrofit
	##
	# Remov Retrofits with a cost and ratio greater than the inputs
	#
	# Params:
	#	threshold:	float cost / point difference max value. Delete Retrofit if higher
	#
	def filterRetrofitsByImpactRatio(self, threshold):
		retrofits	= []
		for retrofit in self.retrofits:
			if retrofit.impactRatio < threshold:
				retrofits.append(retrofit)
		self.retrofits	= retrofits
	##
	# Filter Retrofits with a cost and cost / point difference ratio greater than input parameters
	#
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
	# Filter harder Retrofits: Measures you wouldn't select because better options exist.
	#
	# If a Retrofit has more RetrofitOptions than another and it's cost is higher and point difference
	# lower, then it's a worse option - why would you implement two measures for less impact and higher cost.
	#
	# Note: There are alternative ways to approach this. Maybe mark as a virtual method for anyone else.
	##
	def filterHarderMeasures(self):
		# Clone the Retrofits so we don't mess with the sort order 
		retrofits = list(self.retrofits)
		# Sort so we can say that retrofit2 will always have the same or more measures than retrofit1
		retrofits.sort(key=lambda retrofit: retrofit.measureCount)
		# Where the bad Retrofits go to die
		forRemoval	= list()
		# Do with every Retrofit.
		for retrofit1ID in range(self.retrofitCount):
			retrofit1	= retrofits[retrofit1ID]
			# Do with all Retrofits from retrofit1 through to the end of the set
			for retrofit2ID in range(self.retrofitCount - retrofit1ID):
				retrofit2	= retrofits[retrofit2ID + retrofit1ID]
				# If the Retrofit has more measures, costs more and has less or equal point difference. Remove it
				if retrofit1.measureCount < retrofit2.measureCount and retrofit1.cost <= retrofit2.cost and retrofit1.difference >= retrofit2.difference:
					forRemoval.append(retrofit2)
		# Get unique Retrofits for removal
		forRemoval		= set(forRemoval)
		# Filter out worthless measures
		self.retrofits	= [retrofit for retrofit in self.retrofits if retrofit not in forRemoval]

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
		cost 		= 9999999999999
		for idx in range(len(self.retrofits)):
			retrofit	= self.retrofits[idx]
			if retrofit.efficiency >= efficiency and retrofit.cost <  cost:
				retrofitID	= idx
				cost 		= retrofit.cost
		return retrofitID