### Imports ###
## Native
import csv
## Project
from lib.building	import Building
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
	def getCheapestToRatingState(self, rating):
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
	
	### Maigc... Methods ###
	def __iter__(self):
		# This method returns an iterator object
		self._iter_index = 0
		return self

	def __next__(self):
		# This method defines how to retrieve the next element in the iteration
		if self._iter_index < len(self.buildings):
			result = self.buildings[self._iter_index]
			self._iter_index += 1
			return result
		else:
			# Let the caller know the iteration is over
			raise StopIteration
	##
	# Get building
	##
	def __getitem__(self, buildingID):
		return self.buildings[buildingID]