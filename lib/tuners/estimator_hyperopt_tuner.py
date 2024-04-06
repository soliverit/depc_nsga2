### Includes ###
## Native
from hyperopt		import tpe, Trials
## Project
from lib.hyperopt_hp_tuner_base	import HyperoptHpTunerBase
##
# Hyperopt hp tuning for estimators
##
class EstimatorHyperoptTuner(HyperoptHpTunerBase):
	def __init__(self, model, iterations=10, parameters={}, algorithm=tpe.suggest, trials=Trials(), cvSteps=1):
		super().__init__(model, iterations=iterations, parameters=parameters, algorithm=algorithm, trials=trials, cvSteps=cvSteps)
	def evaluate(self):
		self.model.train()
		return self.model.test()["rmse"]
	def intermediaryModelChanges(self):
		self.model.shuffleData()

		

		
