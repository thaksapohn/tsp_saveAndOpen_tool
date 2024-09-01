
import os
import platform
import tempfile
from datetime import datetime
from pprint import pprint

# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

TEMP_PATH = tempfile.gettempdir().replace('\\', '/')

try:
	from . import sqlite_base
	reload(sqlite_base)
except:
	import sqlite_base
	reload(sqlite_base)


# +------------------------------+
# +           FILE DB    	     +
# +------------------------------+
# | id | name | path | create_at |
# +------------------------------+


class SQLITE_PROJECT_DB(sqlite_base.SQLITE_BASE):
	def __init__(self):
		super(self.__class__, self).__init__()

		self.db_path = '{temp_path}/saveAndOpen_tool/project.db'.format(temp_path = TEMP_PATH)


	def parse_data(self, data = {}):
		
		result = {}

		if data:

			if data.get('path'):
				result['path'] = data.get('path')
			
			if data.get('name'):
				result['name'] = data.get('name')

			if data.get('id'):
				result['id'] = data.get('id')

			if data.get('id_data'):
				result['id'] = data.get('id_data')

		return result

	def parse_result(self, data=[]):
		result = []

		for r in data:
			parse_data = {}
			parse_data['id'] = r[0]
			parse_data['name'] = r[1]
			parse_data['path'] = r[2]

			result.append(parse_data)

		return result


	def create_project_db(self):

		if not os.path.exists(self.db_path):
			self.create(
				path=self.db_path, 
				fields=['id', 'name', 'path', 'create_at'], 
				table='project_data')

			self.close_connection()

	def delete_project_db(self):
		
		if os.path.exists(self.db_path):

			os.remove(self.db_path)


	def insert_project_data(self, name='', path='', values={}):
		'''
		|_name				ex. 'test_project'
		|_path				ex. 'T:/rnd/test_project/work'
		|_values [dict]
			|_name				ex. 'test_project'
			|_path				ex. 'T:/rnd/test_project/work'

		'''

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)
		else:
			self.create(
				path=self.db_path, 
				fields=['id', 'name', 'path', 'create_at'], 
				table='project_data')

		# parse id
		#---------
		rows = self.search(filters={}, table='project_data')
		id_data = 1
		
		if rows:
			last_row = rows[-1]
			last_id = last_row[0]
			id_data = int(last_id) + 1

		# parse date
		#-----------
		date_at = datetime.now()

		# insert row 
		#-----------
		if values:
			if not values.get('id'):
				values['id'] = id_data

			if not values.get('create_at'):
				values['create_at'] = date_at

		else:
			values = {
				'id': id_data,
				'name' : name,
				'path': path,
				'create_at': date_at }

		self.insert(table='project_data', values=values)
		self.close_connection()

	def update_project_data(self, filters={}, values={}):
		'''
		|_filters [dict]
			|_path				ex. 'T:/rnd/zeafrost/work'
			|_name				ex. 'test_project'
			|_id				ex. 1
		|_values [dict]
			|_path				ex. 'T:/rnd/zeafrost/work'
			|_name				ex. 'test_project'
		'''

		self.db_path = self.db_path.format(temp_path=TEMP_PATH)

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)
		else:
			self.create(
				path=self.db_path, 
				fields=['id', 'name', 'path', 'create_at'], 
				table='project_data')

		# parse filters
		#--------------
		filters_parse = self.parse_data(data=filters)
		values_parse = self.parse_data(data=values)

		self.update(
			table='project_data',
			values=values_parse,
			filters=filters_parse)

		self.close_connection()

	def search_project_data(self, filters={}):
		'''
		|_filters [dict]
			|_path			ex. 'T:/rnd/test_project/work'
			|_name				ex. 'test_project'
			|_id				ex. 1
		'''
		result = []
		
		self.db_path = self.db_path.format(temp_path=TEMP_PATH)

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)
		
			filters_parse = self.parse_data(data=filters)

			search_result = self.search(filters=filters_parse, table='project_data')
			self.close_connection()

			result = self.parse_result(search_result)

		return result

	def delete_project_data(self, filters={}):
		'''
		|_filters [dict]
			|_path			ex. 'T:/rnd/test_project/work'
			|_name				ex. 'test_project'
			|_id				ex. 1
		'''

		self.db_path = self.db_path.format(temp_path=TEMP_PATH)

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)

			filters_parse = self.parse_data(data=filters)
			self.delete(filters=filters_parse, table='project_data')
			



