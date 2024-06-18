### Includes ###
## Native
from argparse					import ArgumentParser
from time 						import time, sleep
from os.path					import isdir
from os							import mkdir
## Project 
from lib.mealpy_process_thread	import MealPyProcessThread
##
# MealPy Community Optimiser: Threaded ,recurrent MealPy optimisation
## 
class MealPyCommunityOptimiser():
	def __init__(self, buildings, constructor, epochs, population, processingPath, resultsPath, threads=2, partitions=2, alias="."):
		self.buildings			= buildings
		self.constructor		= constructor
		self.epochs				= epochs
		self.population			= population
		self.resultsPath		= resultsPath
		self.processingPath		= processingPath
		self.threads			= threads
		self.partitions			= partitions
		self.alias				= alias
		self.activeThreads		= []
		self.finishedThreads	= []
	def run(self):
		# Reset thread arrays
		self.buildingThreads	= []
		self.finishedThreads	= []
		# Partition data for threading
		buildingSets	= self.buildings.partition(self.partitions)
		# Alias for filenames
		counter			= 1
		# Track duration
		start			= time()
		# Make sure data directory exists
		if not isdir(self.processingPath):
			mkdir(self.processingPath)
		##
		# The thread loop: runs until everything's been processed
		##
		while True:
			##
			# Finsihed thread handling
			##
			# We'll reconstruct self.buildingThreads
			runningThreads	= []
			for buildingThread in self.buildingThreads:
				# Migrate finished threads to the finished thread list
				if buildingThread.finished:
					self.finishedThreads.append(buildingThread)
				# Otherwise, keep the thread in the active set
				else:
					runningThreads.append(buildingThread)
			self.buildingThreads	= runningThreads
			##
			# Thread queuing
			##
			if len(self.buildingThreads) < self.threads:
				##
				# Queue up and start the next thread then update the alias counter
				#
				# TODO: Flag handling sucks. Do the Flags To String in this class, not as init parameter
				##
				if len(buildingSets) > 0:
					buildingThread	= MealPyProcessThread(
						self.constructor,
						buildingSets.pop(),
						dataPath="%s%s.csv" %(self.processingPath, str(counter)),
						resultsPath=self.resultsPath,
						flags= "--alias %s --epochs %s --population %s --silent" %(self.alias + "-" + str(counter), self.epochs, self.population)
					)
					buildingThread.start()
					self.buildingThreads.append(buildingThread)
					counter += 1
				##
				# Loop exit condition: All datasets processed
				##
				elif len(self.finishedThreads) == self.partitions:
					break
			# For posterity (Gogle reckons it's a good idea)
			sleep(1)
	################################################
	# Class and static stuff
	################################################
	@staticmethod
	def ParseCMD():
		parser	= ArgumentParser()
		parser.add_argument("--data", type=str, required=True, help="Data alias: E.g '11k' points to ./data/11k.csv")
		parser.add_argument("--constructor", type=str, default="OriginalGWO",help="Which MealPy optimisation algorithm? E.g OriginalGWO")
		parser.add_argument("--population", type=int, default=50, help="Population size")
		parser.add_argument("--epochs", type=int, default=50, help="No. epochs")
		parser.add_argument("--partitions", type=int, default=2, help="No. partitions for MealPyCommunityOptimiserBase")
		parser.add_argument("--threads", type=int, default=2, help="No. threads for MealPyCommunityOptimiserBase")
		parser.add_argument("--results-path", type=str, help="Filepath to write result to.")
		parser.add_argument("--processing-path", type=str, required=True, help="Directory to put partitioned data in")
		parser.add_argument("--target", type=str, default="D", help="Filepath to write result to.")
		parser.add_argument("--silent", action="store_true", help="No console logging")
		return vars(parser.parse_args())
		