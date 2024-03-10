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
			csv_reader = csv.DictReader(file)
			# Iterate over each row in the CSV file
			for row in csv_reader:
				# 'row' is a list containing the values of each column in the current row
				building	= Building(row, float(row["CURRENT_ENERGY_EFFICIENCY"]))
				buildings.append(building)
		return buildings
	### Instance stuff ###
	def __init__(self):
		self.buildings	= []
		self.area 		= 0.0
	def append(self, building):
		self.buildings.append(building)
		self.area += building.area
	
	def getByRating(self, rating):
		set	= __class__()
		for building in self.buildings:
			if building.rating == rating:
				set.append(building)
		return set
	def getByRatings(self, ratings):
		set	= __class__()
		for building in self.buildings:
			for rating in ratings:
				if rating == building.rating:
					set.append(building)
					break
		return set
	def retrofitCount(self):
		count	= 0
		for building in self.buildings:
			count	+= building.retrofitCount
		return count
	def getCheapestToRating(self, rating):
		cost			= 0.0
		points			= 0.0
		metPoints		= 0.0
		highestCost		= 0.0
		highestRatio	= 0.0
		for building in self.buildings:
			points		+= building.toRating("D")
			retrofit	= building.getCheapestRetrofitToEfficiency(Building.ratingLowerBound("D"))
			## Best case stuff
			if retrofit:
				cost 		+= retrofit.cost
				metPoints	+= retrofit.difference
				ratio		= retrofit.cost / retrofit.difference
				if retrofit.cost > highestCost and ratio > highestRatio:
					highestCost	= retrofit.cost
					highestRatio = ratio
					
		return {
			"metPoints": metPoints, 
			"cost": cost, 
			"points": points,
			"highestCost": highestCost,
			"highestRatio": highestRatio
		}
	def toRatingDifference(self, rating):
		total	= 0
		for building in self.buildings:
			difference = Building.RATING_BRACKETS[rating]["lower"] - building.efficiency
			if difference > 0:
				total += difference
		return total
	### Filters ###
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
	#
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
			# StopIteration is raised to signal the end of the iteration
			raise StopIteration