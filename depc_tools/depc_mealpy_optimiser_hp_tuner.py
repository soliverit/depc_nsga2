### Includes ###
## Native

## Project
from lib.hyperopt_hp_tuner_base	import HyperoptHpTunerBase
class DEPCMealPyOptimiserHpTuner(HyperoptHpTunerBase):
	def __init__(self, model, iterations=10, parameters={}, cvSteps=1):
		super().__init__(model, iterations=iterations, parameters=parameters, cvSteps=cvSteps)
	def evaluate(self):
		self.model.solve()
		return self.model.lastResult.target.objectives[0]
	def mapHpSet(self):
		for parameter in __class__.HP_SETS[self.model.algorithm.__name__]:
			self.addParameter(parameter.name, parameter)
	####################################
	# HYPER_PARAMATER sets
	#####################################
	HP_SETS	= {
		"OriginalHGS": [HyperoptHpTunerBase.MakeUniformParameter("PUP", 0.01, 0.2), HyperoptHpTunerBase.MakeUniformIntParameter("LH", 1000, 20000)],
		"OriginalPSO": [
			HyperoptHpTunerBase.MakeUniformParameter("c1", 1, 3),
			HyperoptHpTunerBase.MakeUniformParameter("c2", 1, 3),
			HyperoptHpTunerBase.MakeUniformParameter("w", 0, 1.0),
		],
		"C_PSO": [
			HyperoptHpTunerBase.MakeUniformParameter("c1", 1, 3),
			HyperoptHpTunerBase.MakeUniformParameter("c2", 1, 3),
			HyperoptHpTunerBase.MakeUniformParameter("w_min", 0.1, 0.4),
			HyperoptHpTunerBase.MakeUniformParameter("w_min", 0.4, 2.0),
		],
		"CL_PSO": [
			HyperoptHpTunerBase.MakeUniformParameter("c_local", 1, 3),
			HyperoptHpTunerBase.MakeUniformParameter("w_min", 0, 0.5),
			HyperoptHpTunerBase.MakeUniformParameter("w_max", 0.7, 2),
			HyperoptHpTunerBase.MakeUniformParameter("max_flag", 5, 20),
		],
		"HPSO_TVAC": [
			HyperoptHpTunerBase.MakeUniformParameter("ci", 0.3, 1),
			HyperoptHpTunerBase.MakeUniformParameter("cf", 0.0, 0.3),
		], 
		"OriginalEFO": [
			HyperoptHpTunerBase.MakeUniformParameter("r_rate", 0.1, 0.6),
			HyperoptHpTunerBase.MakeUniformParameter("ps_rate", 0.5, 0.95),
			HyperoptHpTunerBase.MakeUniformParameter("p_field", 0.05, 0.3),
			HyperoptHpTunerBase.MakeUniformParameter("n_field", 0.3, 0.7)
		],
		"DevCHIO": [
			HyperoptHpTunerBase.MakeUniformParameter("r_rate", 0.05, 0.2),
			HyperoptHpTunerBase.MakeUniformIntParameter("ps_rate", 5, 20)
		],
		"OriginalGSKA": [
			HyperoptHpTunerBase.MakeUniformParameter("pb", 0.1, 0.5),
			HyperoptHpTunerBase.MakeUniformParameter("kf", 0.3, 0.8),
			HyperoptHpTunerBase.MakeUniformParameter("kg", 0.095, 0.5),
			HyperoptHpTunerBase.MakeUniformIntParameter("kr", 3, 20)
		],
		"DevBBO": [
			HyperoptHpTunerBase.MakeUniformParameter("p_m", 0.01, 0.2),
			HyperoptHpTunerBase.MakeUniformIntParameter("n_elites", 2, 30)
		],
		"OriginalHC": [
			HyperoptHpTunerBase.MakeUniformIntParameter("neighbour_size", 2, 1000)
		],
		"OriginalAVOA": [
			HyperoptHpTunerBase.MakeUniformParameter("p1", 0.1, 0.9),
			HyperoptHpTunerBase.MakeUniformParameter("p2", 0.1, 0.9),
			HyperoptHpTunerBase.MakeUniformParameter("p3", 0.1, 0.9),
			HyperoptHpTunerBase.MakeUniformParameter("alpha", 0.5, 1.5),
			HyperoptHpTunerBase.MakeUniformParameter("gamma", 0.5, 1.5)
		],
		"OriginalSMA": [
			HyperoptHpTunerBase.MakeUniformParameter("pt", 0.01, 0.2)
		],
		"DevVCS": [
			HyperoptHpTunerBase.MakeUniformParameter("lambda", 0.2, 0.65),
			HyperoptHpTunerBase.MakeUniformParameter("sigma", 0.1, 2.0)
		],
		"DevSBO": [
			HyperoptHpTunerBase.MakeUniformParameter("alpha", 0.5, 2.0),
			HyperoptHpTunerBase.MakeUniformParameter("pm", 0.01, 0.2),
			HyperoptHpTunerBase.MakeUniformParameter("psw", 0.01, 0.1)
		], 
		"OriginalSSpiderA": [
			HyperoptHpTunerBase.MakeUniformParameter("ra", 0.1, 1.0),
			HyperoptHpTunerBase.MakeUniformParameter("p_c", 0.6, 0.9),
			HyperoptHpTunerBase.MakeUniformParameter("p_m", 0.01, 0.1)
		],
		"OriginalSHADE": [
			HyperoptHpTunerBase.MakeUniformParameter("miu_f", 0.4, 0.6),
			HyperoptHpTunerBase.MakeUniformParameter("miu_cr", 0.4, 0.6)
		],
		"L_SHADE": [
			HyperoptHpTunerBase.MakeUniformParameter("miu_f", 0.4, 0.6),
			HyperoptHpTunerBase.MakeUniformParameter("miu_cr", 0.4, 0.6)
		],
		"DevTPO": [
			HyperoptHpTunerBase.MakeUniformParameter("alpha", -10, 10),
			HyperoptHpTunerBase.MakeUniformParameter("beta", -100, 100),
			HyperoptHpTunerBase.MakeUniformParameter("theta", 0, 1.0),
		],
		"OriginalICA": [
			HyperoptHpTunerBase.MakeUniformIntParameter("empire_count", 3, 10),
			HyperoptHpTunerBase.MakeUniformParameter("assimilation_coeff", 1.0, 3.0),
			HyperoptHpTunerBase.MakeUniformParameter("revolution_prob", 0.01, 0.1),
			HyperoptHpTunerBase.MakeUniformParameter("revolution_rate", 0.05, 0.2),
			HyperoptHpTunerBase.MakeUniformParameter("revolution_step_size", 0.05, 0.2),
			HyperoptHpTunerBase.MakeUniformParameter("zeta", 0.05, 0.2)
		],
		"OriginalACOR": [
			HyperoptHpTunerBase.MakeUniformIntParameter("sample_count", 2, 1000),
			HyperoptHpTunerBase.MakeUniformParameter("intent_factor",0.2, 1.0),
			HyperoptHpTunerBase.MakeUniformParameter("intent_factor",0.1, 1.0)
		],
		"OriginalBeesA": [
			HyperoptHpTunerBase.MakeUniformParameter("selected_site_ratio",0.1, 0.5),
			HyperoptHpTunerBase.MakeUniformParameter("elite_site_ratio",0.1, 0.3),
			HyperoptHpTunerBase.MakeUniformParameter("selected_site_bee_ratio",0.1, 0.5),
			HyperoptHpTunerBase.MakeUniformParameter("elite_site_bee_ratio",0.5, 0.9),
			HyperoptHpTunerBase.MakeUniformParameter("dance_radius",0.01, 1.0),
			HyperoptHpTunerBase.MakeUniformParameter("dance_reduction",0.9, 0.99)
		],
		"WMQIMRFO": [
			HyperoptHpTunerBase.MakeUniformParameter("somersault_range",1.5, 3),
			HyperoptHpTunerBase.MakeUniformParameter("pm",0.0, 1.0)
		]
	}