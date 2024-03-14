from threading 	import Thread
from subprocess	import run
from os.path	import isdir
from os			import mkdir
class BuildingThread(Thread):
	def __init__(self, buildings, directory, code, flags=""):
		super().__init__()
		self.buildings	= buildings
		self.directory	= directory
		self.code		= directory + code
		self.flags		= flags
		## TODO: Refactor "./data/" out of this from the dataPath statement in
		# ./example.py (soon to be nsga2.py)
		self.filePath	= "./data/" +  directory  + code + ".csv" 
		self.finished	= False
	
	def run(self):
		if not isdir(self.directory):
			mkdir(self.directory)
		print(self.filePath)
		self.buildings.writeFile(self.filePath)
		run("python.exe nsga2.py --code %s %s" %(self.code, self.flags)) 
		self.finished = True

