import psycopg2
import decimal
import re
import sys
import os
from random import choice

from .props import *
from lib.print_helper import *

class ActiveRecord():
	proxy_table_class		= None
	debug_mode 				= False
	read_only				= False
	last_queries 			= dict()
	table_definitions 		= dict()
	table_current_step_id 	= dict()
	random_selected_ids		= dict()
	next_cache_size 		= False
	next_cache 				= []
	next_filter				= " 1=1"
	default_filter			= False
	pluralise 				= True
	default_selects			= "*"
	choose_cache_size		= 100
	choose_cache			= []
	choose_cache_filter		= " 1 = 1 "
	import_column_matcher	= re.compile("^[a-z]|_[a-z]")
	relations				= {}
	modules					= {}
	tableClasses			= {}
	@classmethod
	def connect(self, username, databaseName, password, host="localhost", port=5432):
		self.conn = psycopg2.connect(
			user=username, host=host, database=databaseName, password=password, port=port
		)
	# # Connect to remote database.
	conn = False
	# conn = psycopg2.connect(
		# host="localhost",
		# database='main',
		# user='postgres',
		# password='t4ba78iop',
		# port=5432)


	def __init__(self, props):
		if isinstance(props, list):
			tempProps = dict()
			for item in props:
				tempProps[item[0]] = item[1]
			props = tempProps
		for col in self.table_definitions[self.table_name()]:
			if col.name not in props:
				props[col.name] = None		
		self.properties = Props(props)

	def __getitem__(self,name):
		return self.__getattr__(name)
	#Sigh, Python sucks: Pickle needs this but since we use Props()
	#for properties it doesn't handle the set implicitly
	def __getstate__(self):
		output = dict(properties=dict())
		for k, v in self.__dict__["properties"].properties.items():
			output["properties"][k] = v
		return output
	def __setstate__(self,d):
		self.__dict__ = d
	# Dotted attribute access.
	def __getattr__(self, name):
		if name not in self.__dict__["properties"]:
			if name not in self.__dict__:
				return None
			return getattr(self, name)
		return getattr(self, "properties")[name]

	def __setitem__(self,name, value):
		self.__setattr__(name,value)
	# Dotted attribute setting.
	def __setattr__(self, name, value):
		if name == "properties":
			self.__dict__["properties"] = value
			return
		if name in getattr(self, "properties"):
			self.__dict__["properties"][name] = value
			return
		self.__dict__[name] = value
		
	def __str__(self):
		output = ""
		for key in self.table_definitions[self.table_name()]:
			newKey = str(key.name)
			while len(newKey) < 25:
				newKey += " "
			output += newKey + str(self[key.name]) + "\n"

		return output
	def save(self):
		if self.read_only:
			raise Exception("%s in READ_ONLY mode" %(self.table_name()))
		params = ""
		inserts = ""
		if not self["id"]:
			for k, v in  self.__dict__["properties"].properties.items():
				if v.value is not None:
					params += " " +  __class__.to_value_string(v.value) + ","#(str(v.value.replace("'", "''")) if v.type is not str else "'" + v.value + "'") + ","
					inserts += k + ","
		else:
			for k, v in self.__dict__["properties"].properties.items():
				if k != "id":
					if v.value == None:
						value = "NULL"
					else:
						value = v.value
					params += " \"" + k + "\"=" + (str(value) if v.type is not str else "'" + value + "'") + ","
		cur = self.conn.cursor()
		if self["id"]:
			query = "UPDATE %s SET %s WHERE id = %s" %(self.table_name(), params[:-1], self.id)
		else:
			query = "INSERT INTO %s (%s) VALUES (%s) RETURNING id;" %(self.table_name(), inserts[:-1], params[:-1])
		if self.debug_mode:
			PrintHelper.print(query, "ActiveRecord(%s) debug mode:" %(self.table_name()))
		cur.execute(query)
		self.conn.commit()
		if not self["id"]:
			self.id= cur.fetchone()[0]
	@classmethod
	def find_or_create_by(self, params):
		#Attempt to find existing and return it
		record = self.find_by(params)
		if record:
			return record
		#No project found
		return self.create(params)
	@classmethod
	def create(self,params):
		if self.read_only:
			raise Exception("%s in READ_ONLY mode" %(self.table_name()))
		#Build query, exit if it's got invalid property keys
	
		query = self.params_to_insert_query(params)
		if not query:
			return False
		#Insert
		if self.debug_mode:
			PrintHelper.print(query, "ActiveRecord(%s) debug mode:" %(self.table_name()))
		cur = self.conn.cursor()
		cur.execute(query)
		try:
			self.conn.commit()
		except psycopg2.InternalError as e:
			self.conn.rollback()
		#Create new record and set id
		newRecord = self(params)

		newRecord.id = int(cur.fetchone()[0])
		
		return newRecord
	
	@classmethod
	def choose(self):
		if len(self.choose_cache) == 0:
			self.choose_cache = self.find_all_by(self.choose_cache_filter, limit=self.choose_cache_size)
		return choice(self.choose_cache)
	@classmethod
	def multiInsert(self,records):
		if self.read_only:
			raise Exception("%s in READ_ONLY mode" %(self.table_name()))
		query = "INSERT INTO %s" %(self.table_name())
		if self.debug_mode:
			PrintHelper.print("Multi-insert of %s records" %(len(records)),  "ActiveRecord(%s) debug mode:" %(self.table_name()))
		cols = []
		for cell in records[0]:
			if type(cell) == str:
				cols.append(cell)
			else:
				cols.append(cell[0])
		query += "(%s) VALUES " %(",".join(cols))
		values = []
		for row in records:
			temp = []
			if type(row) == dict:
				for column, value in row.items():
					temp.append(self.to_value_string(value))
			else:
				for cell in row:
					temp.append(self.to_value_string(cell[1]))
			values.append("(%s)" %(",".join(temp)))
		query += ",".join(values) + ";"
		cur = self.conn.cursor()
		cur.execute(query)
		self.conn.commit()
	@classmethod
	def params_to_insert_query(self,params):
		inserts = ""
		values = ""
		tempParams = params
		if not isinstance(tempParams, Props):
			tempParams = Props(dict())
			if isinstance(params,dict):
				for k, v in params.items():
					tempParams[k] = str(v)
			else:
				for item in params:
					tempParams[item[0]] = item[1]
		params = tempParams
		for k, v in tempParams.properties.items():
			match = False
			for col in self.table_definitions[self.table_name()]:
				if col.name == k:
					inserts += "\"" + k + "\","
					values += ("'" + str(v) + "'" if col.type != "float32" and col.type != "int32" else str(v)) + ","
					match = True
					break	
			if match is False:
				return False
		return "INSERT INTO %s (%s) VALUES (%s)" %(self.table_name(), inserts[:-1], values[:-1]) + " RETURNING id;"
	@classmethod
	def random(self, conditions= False):
		conds = False
		if self.table_name() not in self.random_selected_ids:
			self.random_selected_ids[self.table_name()] = []
		else: 
			conds = "id NOT IN (%s) " %(",".join(self.random_selected_ids[self.table_name()]))
		if conditions:
			if not conds:
				conds  = conditions
			else:
				conds += " AND %s" %(conditions)
		row = self.find_by(conds, sort=" RANDOM() ") if conds else self.find_by("1 = 1",  sort = " RANDOM()")
		self.random_selected_ids[self.table_name()].append(str(row.id))
		return row
	#Return the results from your last query. Excluding .next()
	@classmethod
	def get_results(self):
		if self.table_name() in self.last_queries:
			return self.last_queries[self.table_name()]
		return []

	@staticmethod
	def to_value_string(val):
		if Prop("test",val).type is not str:
			return "%s" %(val)
		return "'%s'" %(str.replace(val, "'", "''"))
	@staticmethod
	def convert_filter_object(obj):
		if isinstance(obj, str):
			return obj
		temp = []
		for p in obj:
			#Arrays
			if not isinstance(p, str):
				#Not NULL
				if p[1]:
					temp.append("%s = %s" % (p[0], ActiveRecord.to_value_string(p[1])))
				else:	
					temp.append("%s IS NULL" % (p[0]))
			else:
				temp.append(p)
		return temp		
	# Temp method with greedy search.
	@classmethod
	def find_dict_by(self, p, limit=False):
		temp = self.convert_filter_object(p)
		r = self.cursor_to_dict_list(self.query_table( False, temp, limit=limit))
		return r[0] if len(r) > 0 else None

	@classmethod
	def find_all_dict_by(self, p, limit=False):
		temp = self.convert_filter_object(p)
		return self.cursor_to_dict_list(self.query_table( False, temp, limit=limit))

		# return lst
	@classmethod
	def find_all_by(self, p, limit=False, sort=False):
		temp = self.convert_filter_object(p)
		r = self.cursor_to_dict_list(self.query_table( False, temp, limit=limit, sort=sort))
		lst = list()
		for a in r:
			lst.append(self(a))
		return lst

	# @classmethod
	# def find_all_by(self,p):
		# temp = self.convert_filter_object(p)
		# r = self.cursor_to_dict_list(self.query_table( False, temp))
		# lst = list()
		# for a in r:
			# lst.append(self(a))
		# return lst

	@classmethod
	def find_by(self,p, sort=False):
		temp = self.convert_filter_object(p)
		r = self.cursor_to_dict_list(self.query_table( False, temp, 1, sort=sort))
		return self(r[0]) if len(r) != 0 else None

	#With great power comes great responsibility
	# Return every record from a table
	@classmethod
	def get_all(self, limit=False, sort=False):
		self.last_queries[self.table_name()] = self.cursor_to_dict_list(
		self.query_table( False, False, limit=limit, sort=sort))
		return self.last_queries[self.table_name()]

	#Returns the next record in the database one at a time
	# returns false at the end of the table
	@classmethod
	def next(self):
		record = False
		if self.next_cache_size is not False:
			if not self.next_cache:
				self.next_cache = self.cursor_to_dict_list(self.query_table([],[self.next_filter,"id > %s" % (self.table_current_step_id[self.table_name()])], self.next_cache_size, "id ASC"))
			if self.next_cache:
				record = self(self.next_cache[0])
				self.next_cache.pop(0)
				self.table_current_step_id[self.table_name()] = record.id
		else:
			res = self.cursor_to_dict_list(
				self.query_table([],[self.next_filter,"id > %s" % (self.table_current_step_id[self.table_name()])], 1, "id ASC"))
			if len(res)== 1:
				record = self(res[0])
				self.table_current_step_id[self.table_name()] = record.id
		return record
	#Skip n records and set the current table step to the next id
	@classmethod
	def offset_next(self, count):
		res = self.cursor_to_dict_list(
		self.query_table([],["id = (SELECT id FROM inp_models OFFSET %s LIMIT 1)" %(count)], 1, "id ASC"))
		if len(res)== 1:
			record = self(res[0])
			self.table_current_step_id[self.table_name()] = res[0]["id"]
			return record
		return False
		#Reset .next() query counter
	@classmethod
	def reset(self):
		self.table_current_step_id[self.table_name()] = 0
	@staticmethod
	def getClassFromTableName(name):
		return __class__.tableClasses[name]
		#PREP method: Pulls database table definitions for the structure and constraints
	@staticmethod
	def loadModules():
		for file in os.listdir("lib/active_record_models"):
			if ".py" in file:
				name = file.split(".")[0]
				nameSegments = name.split("_")
				className 	= ""
				for segment in nameSegments:
					className += segment[0].upper() + segment[1:]
				__class__.modules[name] = getattr(__import__("lib.active_record_models." + name, fromlist=[""]), className)

	@classmethod
	def load(self, autoloader=False):
		if not self.conn:
			print("Error: Connection has not been established. Call self.conn(n,d,p,..). Exiting")
			exit()
		if autoloader:
			__class__.loadModules()
		for cls in self.__subclasses__():
			self.tableClasses[cls.table_name] = cls
			for cl in cls.__subclasses__():
				self.tableClasses[cl.table_name()] = cl
				self.table_definitions[cl.table_name()] = self.list_to_columns(
					self.reduce_cursor_to_simple_list(cl.get_columns()))
				self.table_current_step_id[cl.table_name()] = 0
			self.table_definitions[cls.table_name()] = self.list_to_columns(self.reduce_cursor_to_simple_list(cls.get_columns()))
			self.table_current_step_id[cls.table_name()] = 0
		
	@classmethod
	def loadDependencies(self):
		for column in self.table_definitions[self.table_name()]:
			if column.name[-3:] == "_id":
				nameSegments = column.name.split("_")[0:-1]
				libName		= "_".join(nameSegments)
				className 	= ""
				for segment in nameSegments:
					className += segment[0].upper() + segment[1:]
				
			
		# exit()
	# #Turn class name into table name
	@classmethod
	def table_name(self, forceSingular=False):
		name = self.proxy_table_class.__name__ if  self.proxy_table_class else self.__name__ 
		name =  re.sub("(?!^[A-Z])([A-Z])", "_\\1", name).lower()
		if self.pluralise and not forceSingular:
			name = name + "s"
		return name
	@classmethod
	def relation_id_name(self):
		return self.table_name(forceSingular=True) + "_id"

	@classmethod
	# Get list of columns for a given table with passed caveats and sorts
	def get_columns(self, sort=" 1 ", conds=False):
		# Translate conditions list
		condString = self.to_condition_string(conds)

		# Create cursor and execute query
		cur = self.conn.cursor()
		cur.execute("""SELECT column_name,
						CASE
						WHEN data_type = 'numeric'
						THEN 'float32'
						WHEN data_type = 'integer'
						THEN 'int32'
						ELSE 's128'
						END ndarray_type
						FROM information_schema.columns
						WHERE table_name = '%s' AND %s ORDER BY %s;"""
						% (self.table_name(), condString, sort))
		return cur

	@classmethod
	def naked_select(self, selects,conds,limit,sort):
		temp = self.convert_filter_object(p)
		r = self.cursor_to_dict_list(self.query_table( False, temp))
		output = list()
		for row in r:
			output.append(self(row))
		return output
		
	@classmethod
	# Generic, single table query method with selection and conditions lists.
	def query_table(self, selects, conds, limit=False, sort=False):
			# table 	-> name of table.
			# selects 	-> list of operations.
			# conds 	-> list of conditionals on selects.
			# limit 	-> number of records to return
			# sort		-> sort order for return (some_column [ASC | DESC], some_other_column [ASC | DESC])

		# Translate conditions list
		condString = self.to_condition_string(conds) if not isinstance(conds, str) else conds
		# Translate selection list
		if selects:
			selectString = self.to_selects(selects)
		else:
			selectString = self.default_selects
		sort = " ORDER BY %s" % (sort) if sort else ""
		# Limit
		lim = "LIMIT %s" % (limit) if limit else ""
		# print(condString)
		# Create cursor and execute query.
		cur = self.conn.cursor()
		query = """SELECT %s
			FROM %s
			WHERE %s
			%s
			%s""" % (selectString, self.table_name(), condString, sort, lim)
		if ActiveRecord.debug_mode:
			PrintHelper.print(query, "ActiveRecord(%s) debug mode:" %(self.table_name()))
		cur.execute(query)

		return cur
	
	@classmethod
	# Translate list of strings to Sql (AND) conditions
	def to_condition_string(self,conds):

		# Placeholder
		condString = ""

		# If a list has been passed build condition string
		if isinstance(conds, list):
			# Skip initial AND.
			condString += conds[0]
			conds.pop(0)

			# Do the rest (AND)
			for cond in conds:
				condString += " AND " + cond
		if self.default_filter:
			if condString:
				condString += " AND " + self.default_filter
			else:
				condString = self.default_filter
		if not condString:
			condString = "true"
		return condString


	@classmethod
	# Translate list to selection string
	def to_selects(self,selects):

		# If a list is passed, build the string
		if isinstance(selects, list) and len(selects) > 0:
			return ",".join(selects)
		# Debatably dirty: Default to select all
		else:
			return "*"


	@classmethod
	# Translate cursor to simple list removing dud records
	def reduce_cursor_to_simple_list(self, results):
		# List for broken entries, each entry is a list of empty cell ids
		brokenEntries = []
		# List of complete entries
		workingEntries = []
		# With every entry
		for row, entry in enumerate(results.fetchall()):
			# Temp list
			simpleRow = []
			# Self explanatory, really
			success = True

		# With each cell(column)
			for cell in entry:
				# If it's an empty cell,bail out
				if cell is None:
					success = False
					break
				else:
					simpleRow.append(float(cell) if type(cell) is decimal.Decimal else cell)
				# Append clean row to results list.
			if success:
				workingEntries.append(simpleRow)
		return workingEntries


	# Translate Psycopg cursor to dictionary list
	@staticmethod
	def cursor_to_dict_list(cursor):
		lst = list()
		keys = cursor.description
		for record in cursor.fetchall():
			r = dict()
			for i, key in enumerate(keys):
				r[key.name] = record[i]
			lst.append(r)
		return lst


		# Create column class for the table_definitions list.
	@staticmethod
	def list_to_columns(cols):
		res = list()
		for col in cols:
			res.append(Column(col[0], col[1]))
		return res
	def print(self):
		print("Printing " + self.table_name() + " record " + str(self.id))
		for k, v in self.properties.properties.items():
			print(k + "\t" + str(v.value))

# Simple class for table columns
class Column():
	def __init__(self, name, type):
		self.name = name
		self.type = type



