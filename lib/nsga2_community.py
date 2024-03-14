### Include ###
## Native
from os.path	import isfile, isdir
from os			import mkdir
from time		import time, sleep
## Project
from lib.building_thread	import BuildingThread
class NSGA2Community():
	def __init__(self, buildings, dataDirectory, partitions=8, threadCount=4, flags=""):
		self.buildings			= buildings
		self.dataDirectory		= dataDirectory + "/"
		self.partitions			= partitions
		self.threadCount		= threadCount
		self.flags				= flags
		self.buildingThreads	= []
		self.finishedThreads	= []
	def run(self):
		buildingSets	= self.buildings.partition(self.partitions)
		counter			= 1
		start			= time()
		while True:
			if len(self.buildingThreads) < self.threadCount:
				if len(buildingSets) > 0:
					buildingThread	= BuildingThread(
						buildingSets.pop(),
						self.dataDirectory,
						str(counter),
						flags=self.flags
					)
					buildingThread.start()
					self.buildingThreads.append(buildingThread)
					counter += 1
				else:
					break
			runningThreads	= []
			for buildingThread in self.buildingThreads:
				if buildingThread.finished:
					self.finishedThreads.append(buildingThread)
				else:
					runningThreads.append(buildingThread)
			self.buildingThreads	= runningThreads
			# For posterity (Gogle reckons it's a good idea)
			sleep(1)
		print("Time: %s" %(time() - start))



