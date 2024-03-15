### Include ###
## Native
from argparse					import ArgumentParser
from os.path					import isfile, isdir
from os							import mkdir
from time						import time, sleep
## Project
from lib.nsga2_process_thread	import NSGA2ProcessThread
from lib.building_set			import BuildingSet
from lib.retrofit_nsga2			import RetrofitNSGA2
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
	def __init__(self, buildings, dataDirectory, partitions=8, threadCount=4, inequality=False,flags=""):
		self.buildings			= buildings				# BuildingSet
		self.dataDirectory		= dataDirectory + "/"	# Directory where files are saved
		self.partitions			= partitions			# Number of BuildingSets
		self.threadCount		= threadCount			# Number of concurrent threads
		self.inequality			= inequality			# float / bool explicitly define global minimum EPC improvement constraint
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
				flags = self.flags + " --history-path ./test/shoe/%s.csv" %(str(counter))
				if self.inequality:
					flags += " --inequality %s" %(int(self.inequality / self.partitions))
				if len(buildingSets) > 0:
					buildingThread	= NSGA2ProcessThread(
						buildingSets.pop(),
						self.dataDirectory,
						str(counter),
						flags=flags
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
		print("WARNING!!!! You're writing to and from a dictionary with key control. Will break Retrofit relationships")
		self.results	= buildingSet
	##
	# Parse command line arguments: Extends RetrofitNSGA2.ParseCMD()
	##
	@staticmethod
	def ParseCMD():
		parser = ArgumentParser(description="Domestic EPC retrofit strategy maker")
		parser.add_argument("--code", type=str, help="Set the sample_data file code. E.g '11k' = './sample_data/11k.csv'")
		parser.add_argument("--summary", help="Print these parameters", action="store_true")
		parser.add_argument("--verbose", help="Enable NSGA2 console logging", action="store_true")
		parser.add_argument("--silent", help="Don't write results to console", action="store_true")
		parser.add_argument("--crossover",  help="I tell it to use crossover", action="store_true")
		parser.add_argument("--crossover-eta", type=float, help="Set crossover eta")
		parser.add_argument("--crossover-prob", type=float, help="Set crossover prob")
		parser.add_argument("--mutation-eta", type=float, help="Set mutation eta")
		parser.add_argument("--gen", type=int, help="Set number of generations")
		parser.add_argument("--population", type=int, help="Set population size")
		parser.add_argument("--children", type=int, help="Set number of children")
		parser.add_argument("--best-initial-states", help="Use cheapest building-locked as the intial states", action="store_true")
		parser.add_argument("--write-state", help="Append results to the BuildingSet and write new file", action="store_true")
		parser.add_argument("--history-path", type=str, help="Where to write the CSV results?")
		parser.add_argument("--target-rating", type=str, help="Minimum EPC rating that defines the GA constraint")
		parser.add_argument("--threads", type=int, help="Number of concurrent RetrofitNSGA2 threads")
		parser.add_argument("--partitions", type=int, help="Number of BuilingSet subsets processed by the threads")
		parser.add_argument("--recurrent-steps", type=int, help="How many recurrent stages. How many times to run the output through NSGA2Community")
		parser.add_argument("--inequality", type=int, help="Explicity set minimum EPC point improvement. Default to --target [A-F]")
		
		# Parse
		args 		= parser.parse_args()
		# Set values
		dataCode 			= args.code if args.code is not None else "mid"
		nGens 				= args.gen if args.gen is not None else 100
		crossover			= args.crossover
		crossoverETA		= args.crossover_eta if args.crossover_eta else 15.0
		crossoverProb		= args.crossover_prob if args.crossover_prob else 0.9
		mutationETA			= args.mutation_eta if args.mutation_eta else 8.0
		population			= args.population if args.population else 40
		children			= args.children if args.children else 20
		historyPath			= args.history_path if args.history_path else False
		targetRating		= args.target_rating if args.target_rating else "D"
		threads				= args.threads if args.threads else 2
		partitions			= args.partitions if args.partitions else 2
		recurrentSteps		= args.recurrent_steps if args.recurrent_steps else 1
		verbose				= args.verbose
		writeState			= args.write_state
		silent				= args.silent
		bestInitalStates	= args.best_initial_states
		inequality			= args.inequality if args.inequality else False

		# Print config
		return {
			"dataCode":				dataCode,
			"historyPath":			historyPath,
			"generations":			nGens,
			"crossover":			crossover,
			"crossoverETA":			crossoverETA,
			"crossoverProb":		crossoverProb,
			"mutationETA":			mutationETA,
			"population":			population,
			"children":				children,
			"verbose":				verbose,
			"bestInitialStates":	bestInitalStates,
			"writeState":			writeState,
			"silent":				silent,
			"targetRating":			targetRating,
			"threads":				threads,
			"partitions":			partitions,
			"recurrentSteps":		recurrentSteps,
			"inequality":			inequality
		}
	@staticmethod
	def ParamsToFlagString(flags):
		flagString = RetrofitNSGA2.ParamsToFlagString(flags)
		if "stateIdentifier" in flags:
			flagString += " --state-identifier %s" %(flags["stateIdentifier"])
		return flagString

