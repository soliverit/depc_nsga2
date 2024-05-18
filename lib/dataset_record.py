class DatasetRecordBase():
	def __init(self, object):
		self.object	= object
	@property
	def stateCount(self):
		return self.object.stateCount