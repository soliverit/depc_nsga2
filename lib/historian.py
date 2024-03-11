
### Includes ###
## Native
from pymoo.core.callback import Callback
## Project

##
# Historian: The lightweight NSGA2 history recorder
#
# NSGA2 minimise's save_history is slow, eats memory, and tracks a lot of 
# information we're not interested in. Historian only records the F values
# for each generation.
#
# Historian doesn't need to know how many objectives there are to record the results.
##
class Historian(Callback):
	def __init__(self):
		super().__init__()
		self.optimals	= []
	##
	# All we're interested in is the optimised Objectives' values. In the case of 
	# the example, the cost to point difference ratio and point difference
	##
	def notify(self, algorithm):
		self.optimals.append(algorithm.opt[0].F)