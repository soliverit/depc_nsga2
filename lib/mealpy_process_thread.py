### Includes ###
## Native
from threading 			import Thread
from subprocess			import run
from os.path			import isdir
from os					import mkdir
## Project 
from lib.building_set	import BuildingSet
##
# NSGA2ProcessThread
#
# A class for threaded nsga2.py processing. Use this to run nsga2.py n the background
##
class MealPyProcessThread(Thread):
	##
	# params:
	#	buildings:		BuildingSet
	#	directory:		string path to processing folder
	#	code:			string alias for files
	#	iteration:		int recurrent stage ID
	#	flags:			string of CMD flags for ./nsga2.py		
	#
	def __init__(self, constructor, buildings, dataPath, resultsPath, flags=""):
		super().__init__()
		self.buildings		= buildings		# BuildingSet
		self.constructor	= constructor	# mealpy.Optimiser (a think, anything mealpy with a solve() )
		self.dataPath		= dataPath		# string csv input fi 
		self.resultsPath	= resultsPath	# string path to csv where results will be written
		self.finished		= False			# bool process has finished
		self.flags			= flags			# string additional flags for mealpy_optimiser.py
	##
	# Run the thread process
	#
	# 1) Check if input/output directory exists. Create it if it doesn't
	# 2) Write the BuildingSet to the csv for nsga2.py
	# 3) Run ./mealpy_optimiser.py
	# 5) Flag the process as complete
	##
	def run(self):
		# Write the file for mealpy_optimiser.py
		self.buildings.writeFile(self.dataPath)
		# Run mealpy_optimiser.py
		run("python.exe mealpy_optimiser.py --constructor %s --data %s --results-path %s %s" %(self.constructor.__name__, self.dataPath, self.resultsPath, self.flags)) 
		# Mark the process as complete
		self.finished 	= True

