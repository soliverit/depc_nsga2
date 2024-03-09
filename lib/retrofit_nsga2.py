### Includes ### 
## Native
from pymoo.algorithms.moo.nsga2 	import NSGA2
from pymoo.operators.sampling.rnd	import IntegerRandomSampling
from pymoo.operators.crossover.sbx 	import SBX
from pymoo.operators.mutation.pm 	import PM
from pymoo.optimize 				import minimize
from pymoo.termination 				import get_termination
##
# Retrofit NSGA-II
##
class RetrofitNSGA2():
	def __init__(self, problem):
		## Generations
		self.generations	= 100
		## Alogrithm and Problem
		self.algorithm		= False
		self.problem		= problem
		## Population
		self.populationSize	= 40
		self.childCount		= 40
		## Crossover parameters
		self.crossover		= True
		self.crossoverRate	= 0.9
		self.crossoverETA	= 15
		self.crossoverModel	= SBX
		## Mutation parameters
		self.mutationETA	= 15
		self.mutationModel	= PM
		## Sampler parameters
		self.sampler		= IntegerRandomSampling()

	def createCrossoverModel(self):
		return self.crossoverModel(**{"prob": self.crossoverRate, "eta": self.crossoverETA})
	def createMutationModel(self):
		return self.mutationModel(**{"eta": self.mutationETA})
	def prepareAlgorithm(self):
	
		self.algorithm	= NSGA2(
			pop_size=self.populationSize,
			n_offsprings=self.childCount,
			sampling=IntegerRandomSampling(),
			crossover=self.createCrossoverModel(),
			mutation=self.createMutationModel(),
			eliminate_duplicates=True
		)
	def run(self):
		if not self.algorithm:
			self.prepareAlgorithm()
		self.lastResult	= minimize(
			self.problem,
			self.algorithm,
			get_termination("n_gen", self.generations),
			seed=1,
			save_history=False,
			verbose=False
		)
	def getResult(self):
		cost 	= 0.0
		points	= 0.0
		x		= self.lastResult.X
		for idx in range(len(x[-1])):
			building	= self.problem.buildings.buildings[idx]
			retrofit 	= building.getRetrofit(round(x[-1][idx]))
			cost 		+= retrofit.cost
			points		+= retrofit.difference
		return {"cost": cost, "points": points}
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
