class DatasetBase():
	def __init__(self):
		self.records
	### Properties ###
	@property
	def length(self):
		return len(self.records)
	### Maigc Methods ###
	def __len__(self):
		return len(self.records)
	##
	# Iterator methods: __iter__, __next__. Credit to the internet. Never wrote an iterator before
	##
	def __iter__(self):
		# This method returns an iterator object
		self._iter_index = 0
		return self
	def __next__(self):
		if self._iter_index < len(self.records):
			result = self.records[self._iter_index]
			self._iter_index += 1
			return result
		else:
			raise StopIteration
	##
	# Get building by index
	##
	def __getitem__(self, buildingID):
		return self.records[buildingID]