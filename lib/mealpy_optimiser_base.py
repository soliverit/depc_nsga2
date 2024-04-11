### Includes ###
## Native 
from typing 	import Any
# from mealpy		import IntegerVar
from importlib	import import_module
from pkgutil	import walk_packages
from argparse	import ArgumentParser
class MealPyOptimiserBase():
	CONSTRCUTORS = {}
	def __init__(self, data, epochs=100, minMax="min", varType=False, algorithm=False, 
			  customParams={}, inequality=-1, populationSize=50, logPath=None):
		self.data			= data				# DatasetBase 
		self.epochs			= epochs			# int number of epoch	
		self.minMax			= minMax			# string [min]imise or [max]imise
		self.varType		= varType			# MealPy variable type. Typically IntegerVar or FloatVar
		self.logPath		= logPath			# string path for log file
		self.lastResult		= False				# Agent or whatever comes from the solver
		self.inequality		= inequality		# int/float penalty objective
		self.populationSize	= populationSize	# int population size
		self.customParams	= customParams		# Dict of extra problem parameters. E.g obj_weights for multi-objective
		self.lastResult		= False				# Last result from optimisation
		self.algorithm		= algorithm			# The MealPy "magic" alogrithm of your choice. MUST DEFINE
	@property
	def lowerBounds(self):
		return [0.0 for i in range(self.data.length)]
	@property
	def upperBounds(self):
		raise Exception("%s doesn't override upperBounds property" %(__class__.__name__))
	@property
	def problem(self):
		return {
			"obj_func": self.score,
			"bounds":	self.varType(lb=self.lowerBounds, ub=self.upperBounds),
			"minmax":	self.minMax,
			"log_to":	self.logPath
		}
	@property
	def completeProblem(self):
		problem	= self.problem
		for key, value in self.customParams.items():
			problem[key]	= value
		return problem
	def score(self, solution):
		raise Exception("%s doesn't override score()" %(__class__.__name__))
	# def solve(self):
	# 	raise Exception("%s doesn't override .solve()" %(__class__.__name__))
	def solve(self):
		self.solver			= self.algorithm(epoch=self.epochs, pop_size=self.populationSize)
		self.lastResult 	=  self.solver.solve(self.completeProblem)
	### Magic methods ###
	def __setattr__(self, name, value):
		if "customParams" not in self.__dict__:
			self.__dict__["customParams"]	= {}
		if name in self.__dict__["customParams"]: 
			self.__dict__["customParams"][name]	= value
		else:
			self.__dict__[name]	= value
	################################################
	# Class and static stuff
	################################################
	@staticmethod
	def GetConstructor(code):
		# Only load once
		if not __class__.CONSTRCUTORS:
			# Dynamically import the target package
			package = import_module("mealpy")
			# Walk through all modules and submodules in the package
			for _, module_name, _ in walk_packages(package.__path__, "mealpy" + '.'):
				# Import the module
				module = import_module(module_name)
				# Inspect the module for classes
				for attribute_name in dir(module):
					attribute = getattr(module, attribute_name)
					if isinstance(attribute, type) and "_based" in str(attribute.__module__):
						__class__.CONSTRCUTORS[attribute.__name__] = attribute
		return __class__.CONSTRCUTORS[code]
	@staticmethod
	def ParseCMD():
		parser	= ArgumentParser()
		parser.add_argument("--code", type=str, default="11k", help="Data alias: E.g '11k' points to ./data/11k.csv")
		parser.add_argument("--constructor", type=str, default="OriginalGWO",help="Which MealPy optimisation algorithm? E.g OriginalGWO")
		parser.add_argument("--population", type=int, default=50, help="Population size")
		parser.add_argument("--epochs", type=int, default=50, help="No. epochs")
		parser.add_argument("--partitions", type=int, default=2, help="No. partitions for MealPyCommunityOptimiserBase")
		