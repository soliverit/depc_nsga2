class Retrofit():
	def __init__(self, description, cost, efficiency, difference):
		self.description	= description
		self.cost			= cost
		self.efficiency		= efficiency
		self.difference		= difference
		self.impactRatio	= cost / difference if difference > 0 else 0