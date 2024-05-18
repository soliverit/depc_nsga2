### Includes ###
## Native 
from time		import time

# from mealpy									import BBO, BBOA, SMA, VCS, SBO, GWO
## Project
from depc_tools.depc_mealpy_optimisation		import DEPCMealPyOptimiser
from depc_tools.depc_mealpy_optimiser_hp_tuner	import DEPCMealPyOptimiserHpTuner
from lib.building_set							import BuildingSet

dataPath 		= "./data/large.csv"
buildings		= BuildingSet.LoadDataSet(dataPath).getByRatings(["G", "F", "E"])
buildingStats	= buildings.getCheapestToRating("D")
buildings.filterRetrofitsByImpactRatio(buildingStats["cost"] / buildingStats["points"] * 2)
buildings.filterZeroOptionBuildings()
buildings.filterHarderMeasures()
buildings.filterZeroOptionBuildings()
from mealpy.bio_based.EOA	import OriginalEOA
customParams	= {
	"p_c":	0.9,
    "p_m": 0.1,
    "n_best": 2,
    "alpha": 0.98,
    "beta": 0.9,
    "gama": 0.9
}

# TLO, HGSO (single int hp)
# QSA, SCA, ESOA, FBIO, CGO, AO, EVO, NRO, SHIO, TSO, SOS, RUN, INFO, TSA, SPBO, FOX SSDO CircleSA (zero params) 
# SARO (half pop hp),
# WHO (too many params)
from mealpy_optimiser		import HGS, HHO, WOA, ALO, PSO, GWO, EOA, ESOA, EFO, HGSO, TLO, QSA, CHIO
from mealpy_optimiser		import GSKA, FBIO, SMA, WHO, BBO, GBO, HC, SCA, AVOA, CGO, EVO, NRO, SMA, VCS, SBO
from mealpy_optimiser		import ABC, SSpiderA, SHADE, TPO, TSO, SOS, RUN, INFO, CEM, TSA, CircleSA, SHIO
from mealpy_optimiser		import CA, ICA, LCO, SARO, SPBO, SSDO, FOX, FA, ACOR, BeesA, AO, BBOA, MFO, MRFO

classes	= [
	QSA.ImprovedQSA, GWO.OriginalGWO, GWO.GWO_WOA, GWO.RW_GWO,
	SCA.OriginalSCA, SCA.DevSCA, ESOA.OriginalESOA, FBIO.OriginalFBIO, FBIO.DevFBIO,
	CGO.OriginalCGO, AO.OriginalAO, EVO.OriginalEVO, NRO.OriginalNRO, SHIO.OriginalSHIO,
	TSO.OriginalTSO, SOS.OriginalSOS, RUN.OriginalRUN, INFO.OriginalINFO, TSA.OriginalTSA, 
	SPBO.OriginalSPBO, SPBO.DevSPBO, FOX.OriginalFOX, SSDO.OriginalSSDO, CircleSA.OriginalCircleSA
]
# classes = [
# 	HGS.OriginalHGS, PSO.OriginalPSO, #PSO.C_PSO, 
# 	PSO.CL_PSO, PSO.HPSO_TVAC, EFO.OriginalEFO,  
# 	CHIO.DevCHIO, 	GSKA.OriginalGSKA, BBO.DevBBO, 
# 	HC.OriginalHC, 	AVOA.OriginalAVOA,	SMA.OriginalSMA, 
# 	VCS.DevVCS,	SBO.DevSBO, SSpiderA.OriginalSSpiderA, 
# 	SHADE.OriginalSHADE, SHADE.L_SHADE, ICA.OriginalICA,
# 	ACOR.OriginalACOR, BeesA.OriginalBeesA, MRFO.WMQIMRFO
# ]

print("Cost:          %s" %(round(buildingStats["cost"])))
print("Target points: %s" %(buildingStats["points"]))
print("Met points:    %s" %(buildingStats["metPoints"]))
print("Target ratio:  %s" %(round(buildingStats["cost"] / buildingStats["metPoints"], 2)))
cont = False
for algorithm in classes:
	print(algorithm.__name__)
	if algorithm.__name__ == "OriginalSCA":
		cont = True
		continue
	if not cont:
		continue
	# Get best HPs
	
	## Generate results
	for pop in [50, 100]:
		for epochs in [100, 250, 400]:
			optimiser	= DEPCMealPyOptimiser(buildings, 
				epochs=epochs,
				algorithm=algorithm,
				populationSize=pop,
				inequality= buildingStats["points"])
		### GO
			t	= time()
			name							= algorithm.__name__.replace("Original", "")
			optimiser.solve()
			with open("./results/single.csv", "a") as file:
				file.write("%s,%s,%s,%s,%s,%s,%s,%s\n" %(
					name,  
					epochs,
					pop,
					dataPath.replace("./data/", ""),
					buildings.length,
					round(buildingStats["cost"] / buildingStats["metPoints"], 2),
					round(time() - t,2),  
					optimiser.lastResult.target.objectives[0], 
					))
			
from math import ceil

state	= [int(x) for x in optimiser.lastResult.solution]
print(optimiser.data.scoreState(state))


exit()
###############################################################################
# Hey folks. Let's implement an SVR estimator and Hyperopt hyperparameter tuner
# to tune it.
#
# Steps:
#	1) Implement SVR using EstimatorBase
#	2) Implement Hyperopt hyperparameter tuner for EstimatorBase models
#	3) Make sure it runs
###############################################################################
##
# SVR
##
### Includes ###
## Native 
from sklearn.svm		import SVR
from pandas				import read_csv
## Project
from lib.estimator_base	import EstimatorBase
##
# Define the class
##
class SVREstimator(EstimatorBase):
	def __init__(self, data, target, trainTestSplit=0.5, customParams={}, C=1, epsilon=0.1):
		super().__init__(data, target, trainTestSplit=trainTestSplit, customParams=customParams)
		self.C					= C
		self.epsilon			= epsilon
		self.applyScaler		= True
		self.applyNormaliser	= True
	@property
	def params(self):
		return {"C": self.C, "epsilon": self.epsilon}
	def train(self):
		self.model	= SVR(**self.allParams)
		self.model.fit(self.trainingInputs, self.trainingTargets)
##
# Test the model
##
data	= read_csv("./data/estimator_depc_example.csv")
model	= SVREstimator(data, "CURRENT_ENERGY_EFFICIENCY")
model.train()
results	= model.test()
print(results)
###
# Parameter tuner
###
### Includes ###
## Native 

## Project
from lib.hyperopt_hp_tuner_base	import HyperoptHpTunerBase
##
# Define the class
##
class SVRTuner(HyperoptHpTunerBase):
	def __init__(self, model, iterations=10, parameters={}, cvSteps=2):
		super().__init__(model, iterations=iterations, parameters=parameters, cvSteps=cvSteps)
	def evaluate(self):
		self.model.train()
		return self.model.test()["rmse"]
##
# Test
##
tuner	= SVRTuner(model, cvSteps=2)
tuner.addUniformIntParameter("C", 1, 50)
tuner.addUniformParameter("epsilon", 0.01, 0.1)
tuner.tune()