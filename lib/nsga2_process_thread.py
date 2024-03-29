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
class NSGA2ProcessThread(Thread):
	def __init__(self, buildings, directory, code, flags=""):
		super().__init__()
		self.buildings	= buildings			# BuildingSet
		self.directory	= directory			# string Directory where files are saved / read from
		self.code		= directory + code	# string Alias for files. E.g
		self.flags		= flags				# string nsga2.py command line parameters string
		self.finished	= False				# bool process has finished
		self.results	= False				# BuildingSet from .stt file. Same as BuildingSet NSGA2 selection in building.data
		## TODO: Refactor "./data/" out of this from the dataPath statement in
		# ./example.py (soon to be nsga2.py)
		self.directory	= "./data/" +  directory 
		self.filePath	= self.directory + code + ".csv" # string csv input file path
		self.sttPath	= self.directory +  directory  + code + ".stt" # string stt output path (just a csv with a convenient extension change)
	##
	# Run the thread process
	#
	# 1) Check if input/output directory exists. Create it if it doesn't
	# 2) Write the BuildingSet to the csv for nsga2.py
	# 3) Run ./nsga2.py
	# 4) Load the .stt output: Just the .csv with an extra column denoting the NSGA2 selection
	# 5) Flag the process as complete
	##
	def run(self):
		# Write the file for nsga2.py
		self.buildings.writeFile(self.filePath)
		# Run nsga2.py
		run("python.exe nsga2.py --code %s %s" %(self.code, self.flags)) 
		# Load the .stt file (just the csv blah blah blah...)
		self.results	= BuildingSet.LoadDataSet(self.sttPath)
		# Mark the process as complete
		self.finished 	= True

