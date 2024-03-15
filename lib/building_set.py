### Imports ###
## Native
import csv
## Project
from lib.building		import Building
from lib.score_struct	import ScoreStruct
class BuildingSet():
	### Static stuff ###
	## Methods 
	@staticmethod
	def LoadDataSet(path):
		buildings	= __class__()
		with open(path, 'r') as file:
			csvReader = csv.DictReader(file)
			# Iterate over each row in the CSV file
			for row in csvReader:
				# 'row' is a list containing the values of each column in the current row
				building	= Building(row, float(row["CURRENT_ENERGY_EFFICIENCY"]))
				buildings.append(building)
		return buildings
	### Instance stuff ###
	def __init__(self):
		self.buildings	= []
		self.area 		= 0.0
	##
	# Write to file
	##
	def writeFile(self, path):
		with open(path, "w") as csvfile:
			columnNames	= list(self.buildings[0].data)
			writer = csv.DictWriter(csvfile, fieldnames=columnNames)
			writer.writeheader()
			for building in self.buildings:
				writer.writerow(building.data)
	##
	# Add a building to the set
	#
	# Params:
	#  building:	Building
	#	
	# Output:	BuildingSet
	##
	def append(self, building):
		self.buildings.append(building)
		self.area += building.area
	##
	# Create a new set of Buildings with the target rating (A - G)
	#
	# Params:
	# rating:	String EPC rating A through G
	#
	# Output:	BuildingSet
	##
	def getByRating(self, rating):
		set	= __class__()
		for building in self.buildings:
			if building.rating == rating:
				set.append(building)
		return set
	##
	# Create a new set of Buildings with one of the target ratings (A - G)
	#
	# Params:
	# rating:	[]String EPC ratings A through G
	#
	# Output:	BuildingSet
	##
	def getByRatings(self, ratings):
		set	= __class__()
		for building in self.buildings:
			for rating in ratings:
				if rating == building.rating:
					set.append(building)
					break
		return set
	##
	# Get the number of Retrofits for all Buildings
	#
	# Output:	Integer Retrofit count, including do-nothing
	##
	def retrofitCount(self):
		count	= 0
		for building in self.buildings:
			count	+= building.retrofitCount
		return count
	##
	#
	##
	def partition(self, count):
		sets = [BuildingSet() for x in range(count)]
		counter = count
		for building in self.buildings:
			sets[counter % count].append(building)
			counter += 1
		return sets
	##
	# Find cheapest to target rating Retrofits and aggregate findings.
	#
	# For each Building: If the Building is worse than the target rating,
	# find the cheapest measure that brings it to at least the target. If it 
	# doesn't have one, skip the Building. Aggregate the costs and EPC points
	#
	# Output:	Hash{
	#			cost:		float Sum of identified Retrofit implemnetation costs
	#			points:		int Target points reduction (all worse building regardless of if Retrofit is found)
	#			metPoints:	int Points actually reduce by the identified Retrofits
	# 		}
	#
	# Params:
	# rating:	String EPC rating A through G
	#
	# Output:	BuildingSet
	##
	def getCheapestToRating(self, rating):
		cost			= 0.0
		points			= 0.0
		metPoints		= 0.0
		for building in self.buildings:
			# Get score, skip buildings that are at least the target rating
			pointDiff	= building.toRating("D")
			if pointDiff == 0:
				continue
			points		+= pointDiff
			## Look for the cheapest, if any, Retrofit for the building
			retrofit	= building.getCheapestRetrofitToEfficiency(Building.ratingLowerBound("D"))
			if retrofit:
				cost 		+= retrofit.cost
				metPoints	+= retrofit.difference
				ratio		= retrofit.cost / retrofit.difference
		return {
			"metPoints": metPoints, 
			"cost": cost, 
			"points": points
		}
	##
	# Create an array of the indices of the Cheapest Retrofit that brings Building not
	# at the target rating. Remaining Building get 0 index, the do-nothing or as-built Retrofit
	#
	# params:
	#	rating:	char target EPC rating.
	#
	# output:	array of Retrofit indices denoting cheapest to rating states.
	##
	def getCheapestToRatingState(self, rating):
		rating	= rating.upper()
		state	= []
		for building in self.buildings:
			# Get score, skip buildings that are at least the target rating
			pointDiff	= building.toRating("D")
			if pointDiff == 0:
				state.append(0)
			## Look for the cheapest, if any, Retrofit for the building
			stateID	= building.getCheapestRetrofitToEfficiencyID(Building.ratingLowerBound("D"))
			if stateID:
				state.append(stateID)
			else:
				state.append(stateID)
		return state
	##
	# Take an array denoting a BuildingState like that created by self.getCheapestToRatingState(rating)
	#
	# params:
	#	state:	array of BuildingSet, Building Retrofit array indices.
	#
	# output:	dictionary {"cost": float, "points": float} cost of all Retrofit and Difference in EPC points.
	##
	def scoreState(self, state):
		cost	= 0
		points	= 0
		for building in self.buildings:
			retrofit	= building.getCheapestRetrofitToEfficiency(Building.ratingLowerBound("D"))
			if retrofit:
				cost 	+= retrofit.cost
				points	+= retrofit.difference
		return {"cost": cost, "points": points}
	##
	# Get the number of EPC points required to raise all Buildings to the target rating.
	#
	# params:
	#	rating:	String EPC rating (A through G)
	#
	# Output:	Int total EPC points
	##
	def toRatingDifference(self, rating):
		total	= 0
		for building in self.buildings:
			difference = Building.RATING_BRACKETS[rating]["lower"] - building.efficiency
			if difference > 0:
				total += difference
		return total
	##
	# Create the ScoreStruct from the results based on a key in self.data
	#
	# params:
	#	key:	string column name for self.data. Must be added by another process such as in nsga2.py writeStateFile
	#
	# output:	ScoreStruct representing best state identified by NSGA2
	##
	def getScoreStruct(self, key):
		scoreStruct	= ScoreStruct()
		for building in self.buildings:
			retrofit				= building.getRetrofit(int(building.data[key]))
			scoreStruct.cost		+= retrofit.cost
			scoreStruct.points		+= retrofit.efficiency
			scoreStruct.difference	+= retrofit.difference
		return scoreStruct
	##
	# Merge set (Shallow clone for read-only stuff (or whatever, am no your mum.))
	##
	def merge(self, otherSet):
		for building in otherSet:
			self.append(building)
			
	### Filters ###
	##
	# Filter Retrofits by impact ratio
	##
	def filterRetrofitsByImpactRatio(self, threshold):
		for building in self.buildings:
			building.filterRetrofitsByImpactRatio(threshold)
	##
	# Remove buildings with no impactful Retrofits
	##
	def filterZeroOptionBuildings(self):
		buildings = []
		for building in self:
			if building.retrofitCount > 1:	# All buildings have zero-impact measure
				buildings.append(building)
		self.buildings	= buildings
	##
	# Filter Retrofits with a cost and ratio greater than the inputs
	##
	def filterRetrofitsByCostAndRatio(self, cost, ratio):
		for building in self.buildings:
			building.filterRetrofitsByCostAndRatio(cost, ratio)	
	### Properties ###
	@property
	def length(self):
		return len(self.buildings)
	### Maigc Methods ###
	##
	# Iterator methods: __iter__, __next__. Credit to the internet. Never wrote an iterator before
	##
	def __iter__(self):
		# This method returns an iterator object
		self._iter_index = 0
		return self
	def __next__(self):
		if self._iter_index < len(self.buildings):
			result = self.buildings[self._iter_index]
			self._iter_index += 1
			return result
		else:
			raise StopIteration
	##
	# Get building by index
	##
	def __getitem__(self, buildingID):
		return self.buildings[buildingID]