
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


# +------------------------------------------------------------------------------------+
# +                                     FILE DB                                        +
# +------------------------------------------------------------------------------------+
# | id | filename | description | create_at | update_at | user | path | thumbnail_path |
# +------------------------------------------------------------------------------------+


class SQLITE_FILE_DB(sqlite_base.SQLITE_BASE):
	def __init__(self, project='', path=''):
		super(self.__class__, self).__init__(path)

		self.project = project

		self.db_path = '{temp_path}/saveAndOpen_tool/files.db'.format(temp_path = TEMP_PATH)


	def parse_data(self, data = {}):
		
		result = {}

		if data:

			if data.get('filepath'):
				result['path'] = data.get('filepath')

			if data.get('path'):
				result['path'] = data.get('path')
			
			if data.get('name'):
				result['filename'] = data.get('name')

			if data.get('user'): 
				result['user'] = data.get('user')

			if data.get('id'):
				result['id'] = data.get('id')

			if data.get('id_data'):
				result['id'] = data.get('id_data')

			if data.get('description'):
				result['description'] = data.get('description')

			if data.get('comment'):
				result['description'] = data.get('comment')

			if data.get('thumbnail'):
				result['thumbnail_path'] = data.get('thumbnail')

			if data.get('thumbnail_path'):
				result['thumbnail_path'] = data.get('thumbnail_path')

			if data.get('project'):
				result['project'] = data.get('project')

			if data.get('dcc'):
				result['dcc'] = data.get('dcc')
			
		return result

	def create_file_db(self):
		"""
		The function creates a file-based database if it does not already exist.
		"""

		if not os.path.exists(self.db_path):
			self.create(
				path=self.db_path, 
				fields=['id', 'filename', 'description', 'create_at', 'update_at', 'user', 'path', 'thumbnail_path', 'project', 'dcc'], 
				table='files_data')

			self.close_connection()

	def delete_file_db(self):
		"""
		The function `delete_file_db` deletes a file specified by the `db_path` attribute if it exists.
		"""
		
		if os.path.exists(self.db_path):

			os.remove(self.db_path)

	def insert_file_data(self, filepath='', description='', thumbnail_path='',user='', project='', dcc='', values={}):
		'''
		|_filepath			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/maya/scenes/zeafrost_101_S01_0020_anm_blocking_v003.ma'
		|_thumbnail			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/.data/zeafrost_101_S01_0020_anm_blocking_v003.jpg'
		|_user				ex. 'thaksaporn'
		|_description		ex. 'file use for cache'
		|_project			ex. 'FX_TEST'
		|_dcc				ex. 'maya_2024'

		|_values [dict]
			|_filepath			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/maya/scenes/zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_thumbnail			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/.data/zeafrost_101_S01_0020_anm_blocking_v003.jpg'
			|_user				ex. 'thaksaporn'
			|_description		ex. 'file use for cache'
			|_project			ex. 'FX_TEST'
			|_dcc				ex. 'maya_2024'

		'''

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)
		else:
			self.create(
				path=self.db_path, 
				fields=['id', 'filename', 'description', 'create_at', 'update_at', 'user', 'path', 'thumbnail_path',  'project', 'dcc'], 
				table='files_data')

		# parse id
		#---------
		rows = self.search(filters={}, table='files_data')
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

			if not values.get('update_at'):
				values['update_at'] = date_at

		else:
			values = {
				'id': id_data,
				'filename' : os.path.basename(filepath),
				'description': description,
				'create_at': date_at,
				'update_at': date_at,
				'user': user,
				'path': filepath,
				'thumbnail_path': thumbnail_path,
				'project': project,
				'dcc': dcc}

		self.insert(table='files_data', values=values)
		self.close_connection()

		self.insert_recent_data(
			filepath=filepath, 
			description=description, 
			project=project, 
			dcc=dcc, 
			date=date_at)

	def update_file_data(self, filters={}, values={}):
		"""
		The function `update_file_data` updates data in a database table based on specified filters and
		values.
		
		:param filters: The `filters` parameter in the `update_file_data` method is a dictionary that can
		contain the following keys:
		:param values: The `values` parameter in the `update_file_data` function is a dictionary that
		contains data to be updated in the database table `files_data`. It includes the following keys and
		their corresponding examples:
		"""
		'''
		|_filters [dict]
			|_filepath			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/maya/scenes/zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_name				ex. 'zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_user				ex. 'thaksaporn'
			|_id				ex. 1
		|_values [dict]
			|_filepath			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/maya/scenes/zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_name				ex. 'zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_thumbnail			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/.data/zeafrost_101_S01_0020_anm_blocking_v003.jpg'
		'''

		self.db_path = self.db_path.format(temp_path=TEMP_PATH)

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)
		else:
			self.create(
				path=self.db_path, 
				fields=['id', 'filename', 'description', 'create_at', 'update_at', 'user', 'path', 'thumbnail_path',  'project', 'dcc'], 
				table='files_data')

		# parse filters
		#--------------
		filters_parse = self.parse_data(data=filters)
		values_parse = self.parse_data(data=values)

		self.update(
			table='files_data',
			values=values_parse,
			filters=filters_parse)

		self.close_connection()

	def search_file_data(self, filters={}):
		"""
		The `search_file_data` function searches for data in a database based on specified filters.
		
		:param filters: The `filters` parameter in the `search_file_data` method is a dictionary that can
		contain the following keys:
		:return: The `search_file_data` method returns a list of search results based on the provided
		filters.
		"""
		'''
		|_filters [dict]
			|_filepath			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/maya/scenes/zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_name				ex. 'zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_user				ex. 'thaksaporn'
			|_id				ex. 1
		'''
		result = []
		
		self.db_path = self.db_path.format(temp_path=TEMP_PATH)

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)
		
			filters_parse = self.parse_data(data=filters)

			result = self.search(filters=filters_parse, table='files_data')
			self.close_connection()

		return result

	def delete_file_data(self, filters={}):
		"""
		This function deletes data from a database table based on specified filters.
		
		:param filters: The `filters` parameter is a dictionary that can contain the following keys:
		"""
		'''
		|_filters [dict]
			|_filepath			ex. 'T:/rnd/zeafrost/work/shot/101/S01/0020/anm/maya/scenes/zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_name				ex. 'zeafrost_101_S01_0020_anm_blocking_v003.ma'
			|_user				ex. 'thaksaporn'
			|_id				ex. 1
		'''

		self.db_path = self.db_path.format(temp_path=TEMP_PATH)

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)

			filters_parse = self.parse_data(data=filters)
			self.delete(filters=filters_parse, table='files_data')
			

	def insert_recent_data(self, filepath='', description='', project='', dcc='', date='', values={}):

		# check table
		#------------
		self.connect(self.db_path)
		check_exists = self.check_exist_table(table='recent_data')

		if not check_exists:
			
			self.create(
				path=self.db_path, 
				fields=['id', 'filename', 'description', 'create_at', 'project', 'dcc', 'path'], 
				table='recent_data')

		self.connect(self.db_path)

		# parse id
		#---------
		rows = self.search(filters={}, table='recent_data')
		id_data = 1
		
		if rows:
			last_row = rows[-1]
			last_id = last_row[0]
			id_data = int(last_id) + 1

		if not date:
			# parse date
			#-----------
			date = datetime.now()

		# insert row 
		#-----------
		if values:
			if not values.get('id'):
				values['id'] = id_data

			if not values.get('create_at'):
				values['create_at'] = date

		else:
			values = {
				'id': id_data,
				'filename' : os.path.basename(filepath),
				'description': description,
				'create_at': date,
				'path': filepath,
				'project': project,
				'dcc': dcc}
		
		self.insert(table='recent_data', values=values)
		# self.close_connection()

	def search_recent_data(self, filters={}):

		result = []
		
		self.db_path = self.db_path.format(temp_path=TEMP_PATH)

		if os.path.exists(self.db_path):
			self.connect(path=self.db_path)
		
			filters_parse = self.parse_data(data=filters)

			result = self.search(filters=filters_parse, table='recent_data')
			self.close_connection()

		return result