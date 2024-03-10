### Includes ### 
## Native
import argparse
from pymoo.algorithms.moo.nsga2 	import NSGA2
from pymoo.operators.sampling.rnd	import IntegerRandomSampling
from pymoo.operators.crossover.sbx 	import SBX
from pymoo.operators.mutation.pm 	import PM
from pymoo.optimize 				import minimize
from pymoo.termination 				import get_termination
from lib.print_helper				import PrintHelper
##
# Retrofit NSGA-II
##
class RetrofitNSGA2():
	def __init__(self, problem, generations=100, population=40, children=20,
			  crossover=True, crossoverProb=0.9, crossoverETA=15.0,
			   mutationETA=15.0, verbose=False, callback=False):
		## Generations
		self.generations	= generations
		## Alogrithm and Problem
		self.algorithm		= False
		self.problem		= problem
		## Population
		self.population	= population
		self.children		= children
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
	##
	# Create a crossover model
	#
	# output:	SBX
	##
	def createCrossoverModel(self):
		return self.crossoverModel(**{"prob": self.crossoverProb, "eta": self.crossoverETA})
	##
	# Create mutation model
	# 
	# output:	PolynomialMutation (PM)
	##
	def createMutationModel(self):
		return self.mutationModel(**{"eta": self.mutationETA})
	##
	# Create algorithm
	#
	# Define the pymoo.NSGA2 model. If self.crossover = True, include crossover
	##
	def createAlgorithm(self):
		if self.crossover:
			self.algorithm	= NSGA2(
				pop_size=self.population,
				n_offsprings=self.children,
				sampling=IntegerRandomSampling(),
				crossover=self.createCrossoverModel(),
				mutation=self.createMutationModel(),
				eliminate_duplicates=True
			)
		else:
			self.algorithm	= NSGA2(
				pop_size=self.population,
				n_offsprings=self.children,
				sampling=IntegerRandomSampling(),
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
		self.lastResult	= minimize(
			self.problem,
			self.algorithm,
			get_termination("n_gen", self.generations),
			seed=1,
			verbose=self.verbose,
			**params
		)
	##
	# Get the results from the last process
	##
	def getResult(self):
		cost 	= 0.0
		points	= 0.0
		x		= self.lastResult.X
		import math
		for idx in range(len(x[-1])):
			building	= self.problem.buildings.buildings[idx]
			retrofit 	= building.getRetrofit(math.floor(x[-1][idx]))
			cost 		+= retrofit.cost
			points		+= retrofit.difference
		return {"cost": cost, "points": points}
	def printBenchmark(self):
		results	= self.problem.buildings.getCheapestToRating("D")
		print("--- Benchmark ---")
		print("Buildings: %s" %(self.problem.buildings.length))
		print("Target:    %s" %(self.problem.buildings.toRatingDifference("D")))
		print("Met points %s" %(results["metPoints"]))
		print("Cost:      %s" %(round(results["cost"])))
		print("Points:    %s" %(results["points"]))
		print("Ratio:     %s" %(round(results["cost"] / results["points"], 1)))
	def printResults(self):
		if not self.lastResult:
			print("No NSGA2 results found")
		
		result	= self.getResult()
		cost	= result["cost"]
		points	= result["points"]
		print("--- Optimised ---")
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
	@staticmethod
	def ParseCMD():
		parser = argparse.ArgumentParser(description="Domestic EPC retrofit strategy maker")
		parser.add_argument("--code", type=str, help="Set the sample_data file code. E.g '11k' = './sample_data/11k.csv'")
		parser.add_argument("--callback", help="Include callback: Basically, record history with Historian class", action="store_true")
		parser.add_argument("--summary", help="Print these parameters", action="store_true")
		parser.add_argument("--verbose", help="Enable NSGA2 console logging", action="store_true")
		parser.add_argument("--crossover",  help="I tell it to use crossover", action="store_true")
		parser.add_argument("--crossover-eta", type=float, help="Set crossover eta")
		parser.add_argument("--crossover-prob", type=float, help="Set crossover prob")
		parser.add_argument("--mutation-eta", type=float, help="Set mutation eta")
		parser.add_argument("--gen", type=int, help="Set number of generations")
		parser.add_argument("--population", type=int, help="Set population size")
		parser.add_argument("--children", type=int, help="Set number of children")
		parser.add_argument("--history-path", type=str, help="Where to write the CSV results?")
		# Parse
		args 		= parser.parse_args()
		# Set values
		dataCode 		= args.code if args.code is not None else "mid"
		nGens 			= args.gen if args.gen is not None else 100
		crossover		= args.crossover
		callback		= args.callback
		crossoverETA	= args.crossover_eta if args.crossover_eta else 15.0
		crossoverProb	= args.crossover_prob if args.crossover_prob else 0.9
		mutationETA		= args.mutation_eta if args.mutation_eta else 8.0
		population		= args.population if args.population else 40
		children		= args.children if args.children else 20
		historyPath		= args.history_path if args.history_path else False
		verbose			= args.verbose
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
			"dataCode":			dataCode,
			"historyPath":		historyPath,
			"generations":		nGens,
			"callback":			callback,
			"crossover":		crossover,
			"crossoverETA":		crossoverETA,
			"crossoverProb":	crossoverProb,
			"mutationETA":		mutationETA,
			"population":		population,
			"children":			children,
			"verbose":			verbose
		}