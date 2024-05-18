### Includes ###
## Native 
from math					import floor
from numpy					import array
from random 				import random
## Project
from lib.building_set		import BuildingSet
from lib.retrofit_nsga2		import RetrofitNSGA2
from lib.cost_problem		import CostProblem
from lib.historian			import Historian
from lib.estimator_base		import EstimatorBase
from lib.estimators			import *
from lib.kmeans_clusterer	import KMeansClusterer

constructor	= EstimatorBase.GetConstructor()
params		= constructor.ParseCMD()
model		= constructor.QuickLoad(params["data"])
data		= model.data
clusterer	= KMeansClusterer(data, ["WALLS_ENERGY_EFF", "ageIndex", "ROOF_DESCRIPTION"])
clusterer.cluster()