import types
import importlib
from glob import glob
from time import time
mealpy = importlib.import_module('mealpy')
from lib.mealpy_optimiser_base	import MealPyOptimiserBase
from depc_tools.depc_mealpy_optimisation	import DEPCMealPyOptimiser
from lib.building_set import BuildingSet
MealPyOptimiserBase.GetConstructor("OriginalICA")


dataPath 		= "./data/11k.csv"
buildings		= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E"])
buildingStats	= buildings.getCheapestToRating("D")
buildings.filterRetrofitsByImpactRatio(buildingStats["cost"] / buildingStats["points"] * 2)
buildings.filterZeroOptionBuildings()
buildings.filterHarderMeasures()
buildings.filterZeroOptionBuildings()
i = 0
del MealPyOptimiserBase.CONSTRCUTORS["OriginalHCO"]
del MealPyOptimiserBase.CONSTRCUTORS["OriginalSPBO"]
del MealPyOptimiserBase.CONSTRCUTORS["CMA_ES"]
del MealPyOptimiserBase.CONSTRCUTORS["QTable"]

for name, constructor in MealPyOptimiserBase.CONSTRCUTORS.items():
	with open("./results/all_models.csv", "a") as file:

		start = time()
		f = False
		for x in str(constructor.__module__).split("."):
			if "_based" in x:
				f = x
		i += 1
		ii = str(i) 
		# if name == "CMA_ES":
		# 	continue
		# if name == "OriginalHCO":
		# 	continue
		# if name == "OriginalSPBO":
		# 	continue
		name += ":" 
		while len(ii) != 3:
			ii += " "
		while len(name) < 18:
			name += " "
		while len(f) < 22:
			f += " "
		try:
			optimiser	= DEPCMealPyOptimiser(buildings, 
							epochs=250,
							algorithm=constructor,
							populationSize=100,
							inequality= buildingStats["points"])
			
			optimiser.solve()
			t = str(int(time() - start))
			file.write("%s,%s,%s,%s\n" %(name, f, str(round(optimiser.lastResult.target.objectives[0], 2)), t))
			print(ii + " of " + str(len(list(MealPyOptimiserBase.CONSTRCUTORS))) + " - " + name + f +  str(round(optimiser.lastResult.target.objectives[0], 2)))
		except Exception as e:
			if str(e) == "list index out of range":
				e = "No solution found"
			file.write("%s,%s,%s" %(name, f, e))
			print(ii + " of " + str(len(list(MealPyOptimiserBase.CONSTRCUTORS))) + " - " + name  + f + str(e)[0: 100])

