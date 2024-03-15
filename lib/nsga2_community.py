### Include ###
## Native
from os.path					import isfile, isdir
from os							import mkdir
from time						import time, sleep
## Project
from lib.nsga2_process_thread	import NSGA2ProcessThread
from lib.building_set			import BuildingSet
##
# NSGA2 Community: Threading-based  stratified optimisation
##
class NSGA2Community():
	##
	# params:
	#	buildings:		BuildingSet
	#	dataDirectory:	string where files will be saved and parsed from. Please don't use ./data directly
	# 	partitions:		integer number of BuildingSet subset
	#	threadCount:	integer number of concurrent threads
	#	flags:			string command line arguments for nsga2.py
	## 
	def __init__(self, buildings, dataDirectory, partitions=8, threadCount=4, flags=""):
		self.buildings			= buildings				# BuildingSet
		self.dataDirectory		= dataDirectory + "/"	# Directory where files are saved
		self.partitions			= partitions			# Number of BuildingSets
		self.threadCount		= threadCount			# Number of concurrent threads
		self.flags				= flags					# nsga2.py flags
		self.buildingThreads	= []					# Active NSGA2ProcessingThread
		self.finishedThreads	= []					# Finished NSGA2ProcessingThread
	##
	# Do the stratified NSGA2 optimisation.
	#
	# Splits self.builings into self.partitions subset then processes them in parallel
	# with self.threadCount concurrent threads.
	#
	# Output: 	BuildingSet of all buildings with a property in the data dictioanry
	#			call BEST_TEAM_STATE that denotes the Retrofit retrieve by
	#			building.getRetrofitByID() that was selected by NSGA2.	
	##
	def run(self):
		buildingSets	= self.buildings.partition(self.partitions)
		counter			= 1
		start			= time()
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
			if len(self.buildingThreads) < self.threadCount:
				##
				# Queue up and start the next thread then update the alias counter
				##
				if len(buildingSets) > 0:
					buildingThread	= NSGA2ProcessThread(
						buildingSets.pop(),
						self.dataDirectory,
						str(counter),
						flags=self.flags
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
		##
		# Merge the results
		##
		buildingSet	= BuildingSet()
		for thread in self.finishedThreads:
			buildingSet.merge(thread.results)
		
		struct = buildingSet.getScoreStruct("BEST_TEAM_STATE")
		struct.print()
		print("Time: %s" %(time() - start))
		print("WARNING!!!! You're writing to and from a dictionary with key control. Will break Retrofit relationships")
		return buildingSet


