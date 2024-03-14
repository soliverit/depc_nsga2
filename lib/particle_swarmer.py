from pyswarms.base.base_discrete	import DiscreteSwarmOptimizer
class ParticleSwarmer(DiscreteSwarmOptimizer):
	def __init__(self, buildings, nParticles, dimensions=1, initPos=None, velocityClump=None, vhStrategy="unmodified",
			  ftolIter=1):
		
		self.buildings		= buildings
		self.stateBounds	= {}
		for building in self.buildings:
			print(building.data["BUILDING_REFERENCE_NUMBER"])
		{
			"lower": [ 0 for x in range(buildings.length)],
			"upper": [ building.retrofitCount - 1 for building in self.buildings]
		}
		super().__init__(nParticles, dimensions,
			binary=False,
			options=self.stateBounds,
			velocity_clamp=velocityClump,
			init_pos=initPos,
			ftol=int,
			ftol_iter=1
		)
	def optimize(self):
		pass