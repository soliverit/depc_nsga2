### Includes ###

## Project 
from lib.active_record.dataset		import Dataset
from lib.active_record.record		import Record
from lib.active_record.state		import State
from lib.active_record.state_record	import StateRecord
##
# Data management with SQL
##
class Dataset():
	def __init__(self, data):
		self.data	= data
	### SQL stuff ###
	@staticmethod
	def Save(name, data)