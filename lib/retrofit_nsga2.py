### Includes ### 
## Native
from argparse						import ArgumentParser
from time							import time
from csv							import DictWriter
from pymoo.algorithms.moo.nsga2 	import NSGA2
from pymoo.operators.sampling.rnd	import IntegerRandomSampling
from pymoo.operators.crossover.sbx 	import SBX
from pymoo.operators.mutation.pm 	import PM
from pymoo.optimize 				import minimize
from pymoo.termination 				import get_termination
from math							import floor
## Project
from lib.print_helper				import PrintHelper
from lib.result_struct_set			import ResultStructSet
##
# Retrofit NSGA-II
##
class RetrofitNSGA2():
	def __init__(self, problem, generations=100, population=40, children=20,
			  crossover=True, crossoverProb=0.9, crossoverETA=15.0,
			   mutationETA=15.0, verbose=False, callback=False, initialStates=False):
		## Generations
		self.generations	= generations
		## Alogrithm and Problem
		self.algorithm		= False
		self.problem		= problem
		## Population
		self.population		= population
		self.children		= children
		self.initialStates	= initialStates if initialStates is False else IntegerRandomSampling()
		## Crossover parameters
		self.crossover		= crossover
		self.crossoverProb	= crossoverProb
		self.crossoverETA	= crossoverETA
		self.crossoverModel	= SBX
		## History
		self.callback		= callback
		self.verbose		= verbose
		## Mutation parameters
		self.mutationETA	= mutationETA
		self.mutationModel	= PM
		## Sampler parameters
		self.sampler		= IntegerRandomSampling()
		## ResultStructSet holder. I hate _* vars, but it works best for this
		self._results		= False
	##
	# Create a crossover model
	#
	# output:	SBX
	##
	def createCrossoverModel(self):
		return self.crossoverModel(prob=self.crossoverProb, eta=self.crossoverETA)
	##
	# Create mutation model
	# 
	# output:	PolynomialMutation (PM)
	##
	def createMutationModel(self):
		return self.mutationModel(eta=self.mutationETA)
	##
	# Create algorithm
	#
	# Define the pymoo.NSGA2 model. If self.crossover = True, include crossover
	##
	def createAlgorithm(self):
		# TODO: Replace conditional with **args
		if self.crossover:
			self.algorithm	= NSGA2(
				pop_size=self.population,
				n_offsprings=self.children,
				sampling=self.initialStates if self.initialStates else IntegerRandomSampling(),
				crossover=self.createCrossoverModel(),
				mutation=self.createMutationModel(),
				eliminate_duplicates=True
			)
		else:
			self.algorithm	= NSGA2(
				pop_size=self.population,
				n_offsprings=self.children,
				sampling=self.initialStates,
				mutation=self.createMutationModel(),
				eliminate_duplicates=True
			)
	##
	# Run the pymoo.NSGA2 optimiser
	##
	def run(self):
		# Make the algorithm
		self.createAlgorithm()
		# Run it and store results
		params = {}
		if self.callback:
			params["callback"]	= self.callback
		
		start		= time()
		self.lastResult	= minimize(
			self.problem,
			self.algorithm,
			get_termination("n_gen", self.generations),
			seed=1,
			verbose=self.verbose,
			**params
		)
		self.time	= time() - start
	##
	# Get the ResultStructSet fro the last run(). Build it if necessary
	#
	# output:	ResultStructSet
	##
	@property
	def results(self):
		if self._results:
			self._results 
		self._results	= ResultStructSet(self.problem.buildings.clone())
		for i in range(len(self.lastResult.X)):
			cost 	= 0.0
			points	= 0.0
			for idx in range(len(self.lastResult.X[i])):
				building	= self.problem.buildings.buildings[idx]
				retrofit 	= building.getRetrofit(floor(self.lastResult.X[i][idx]))
				cost 		+= retrofit.cost
				points		+= retrofit.difference
			self._results.add(cost, points, self.lastResult.X[i],self.lastResult.F[i])
		return self._results
	def getResult(self, idx):
		self.results[idx]
	##
	# Print Problem summary and Benchmark
	#
	# The Benchmark: Our base target is to meet the cheapest possible strategy
	# for all Buildings worse than the target. Primarily, we're interested in 
	# the cost to point difference ratio, though the number of points targeted
	# and number met by the cheapest Retrofit selection are also useful.
	##
	def printBenchmark(self):
		results	= self.problem.buildings.getCheapestToRating("D")
		print("--- Benchmark ---")
		print("Buildings:      %s" %(self.problem.buildings.length))
		print("Target:         %s" %(self.problem.inequality))
		print("Met points      %s" %(results["metPoints"]))
		print("Cost:           %s" %(round(results["cost"])))
		print("Effective cost: %s" %(round(results["cost"] * (results["points"] / results["metPoints"]))))
		print("Points:         %s" %(results["points"]))
		print("Ratio:          %s" %(round(results["cost"] / self.problem.inequality, 1)))
	##
	# I'm not even documenting this one. Does what it says on the tin
	##
	def printResults(self):
		if not self.lastResult:
			print("No NSGA2 results found")
		
		print("--- Optimised ---")
		print("Time:   %s" %(self.time))
		result	= self.results.findBest()
		cost	= result.cost
		points	= result.points
		print("Cost:   %s" %(round(cost)))
		print("Points: %s" %(round(points)))
		print("Ratio:  %s" %(round(cost / points, 2)))
		
	def writeHistory(self, path):
		if not path:
			print("Error: Can't save history: No save path set")
			return
		with open(path, "w") as file:
			for optimal in self.callback.optimals:	
				file.write(",".join([str(val) for val in optimal])+ "\n")
	def writeCSVRow(self, path):
		results	= self.getResult()
		with open(path, "a") as file:
			file.write(",".join([
				str(self.problem.buildings.length),
				str(results["cost"]),
				str(results["points"]),
				str(results["cost"] / results["points"]),
				str(self.generations),
				str(self.population),
				str(self.children),
				str(self.mutationETA),
				str(self.crossover),
				str(self.crossoverProb) if self.crossover else "--",
				str(self.crossoverETA) if self.crossover else "--",
				str(self.time),
				"sorted",
			]) + "\n")
	def writeState(self, path):
		bestLastResult	= self.lastResult.X[-1]
		for i, building in enumerate(self.problem.buildings):
			building.data["BEST_TEAM_STATE"] = floor(bestLastResult[i])
		with open(path, "w") as csvfile:
			columnNames	= list(self.problem.buildings[0].data)
			writer = DictWriter(csvfile, fieldnames=columnNames)
			writer.writeheader()
			for building in self.problem.buildings:
				writer.writerow(building.data)

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
		parser.add_argument("--state-identifier", type=str, help="A CSV column name that indicates a Retrofit ID used for creating the initial population. In conjunction with --best-initial-states")
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
		verbose				= args.verbose
		writeState			= args.write_state
		silent				= args.silent
		bestInitalStates	= args.best_initial_states
		stateIdentifier		= args.state_identifier if args.state_identifier else False
		inequality			= args.inequality if args.inequality else False
		# Print config
		if args.summary:
			print(PrintHelper.padArray(["Data code", dataCode], 16))
			print(PrintHelper.padArray(["Generations", nGens], 16))
			print(PrintHelper.padArray(["Crossover", crossover], 16))
			if crossover:
				print(PrintHelper.padArray(["Crossover ETA", crossoverETA], 16))
				print(PrintHelper.padArray(["Crossover prob", crossoverProb], 16))
			print(PrintHelper.padArray(["Mutation ETA", mutationETA], 16))
			print(PrintHelper.padArray(["Population size", population], 16))
			print(PrintHelper.padArray(["No. children", children], 16))
			if historyPath:
				print(PrintHelper.padArray(["Results path", historyPath], 16))
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
			"stateIdentifier":		stateIdentifier,
			"inequality":			inequality
		}
	@staticmethod
	def ParamsToFlagString(params):
		flagString	= ""
		if "dataCode" in params:
			flagString += "--code %s" %(params["dataCode"])
		if "historyPath" in params:
			flagString += " --history-path %s" %(params["historyPath"])
		if "generations" in params:
			flagString += " --gen %s" %(params["generations"])
		if "children" in params:
			flagString += " --children %s" %(params["children"])
		if "crossover" in params:
			flagString += " --crossover"
		if "crossoverETA" in params:
			flagString += " --crossover-eta %s" %(params["crossoverETA"])
		if "crossoverProb" in params:
			flagString += " --crossover-prob %s" %(params["crossoverProb"])
		if "mutationETA" in params:
			flagString += " --mutation-eta %s" %(params["mutationETA"])
		if "bestInitialStates" in params and params["bestInitialStates"]:
			flagString += " --best-initial-states"
		if "writeState" in params:
			flagString	+= " --write-state"
		if "silent" in params and params["silent"]:
			flagString	+= " --silent"
		if "targetRating" in params:
			flagString	+= " --target-rating %s" %(params["targetRating"])
		if "inequality" in params:
			flagString	+= " --inequality %s" %(params["inequality"])
		return flagString