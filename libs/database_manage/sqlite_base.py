
import sqlite3
import os


class SQLITE_BASE(object):
	def __init__(self, path=''):

		self.db_path = path
		self.connection = ''
		self.cursor = ''

		if self.db_path:
			self.connection = sqlite3.connect(self.db_path)
			self.cursor = self.connection.cursor()

	def __str__(self):
		return self.db_path

	def __repr__(self):
		return self.db_path

	def create(self, path='', fields=[], table=''):
		'''
		fields [list]
			|_ index 0 is a integer primary key
		'''
		field_text = 'CREATE TABLE {} '.format(table)
		index = 0
		for filed in fields:

			if index == 0:
				field_text += '([{}] INTEGER PRIMARY KEY, '.format(filed)

			elif not filed == fields[-1]:
				field_text += '{}, '.format(filed)

			else:
				field_text += '{})'.format(filed)

			index += 1
		
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))

		if field_text:
			# create file db
			# ---------------
			self.connection = sqlite3.connect(path)
			self.cursor = self.connection.cursor()
			self.cursor.execute(field_text)
			self.connection.commit()

	def connect(self, path=''):

		if os.path.exists(path):

			if path.endswith('.db'):

				self.connection = sqlite3.connect(path)
				self.cursor = self.connection.cursor()

	def close_connection(self):

		self.connection.close()

	def insert(self, values={}, table=''):
		'''
		values [dict]
			|_ key in values is a name field in table
		table [str]
			|_ table name
		'''
		if values and table:
			
			value_txt = ''
			column_txt = []
			data = []

			value_key = list(values.keys())
			for value in values.keys():

				if value == value_key[0]:
					value_txt += '(?, '
					data.append(values[value])

				elif value == value_key[-1]:
					value_txt += '?)'
					data.append(values[value])

				else:
					value_txt += '?, '
					data.append(values[value])

				column_txt.append(value)

			head_txt = 'insert into {} {} values '.format(table, tuple(column_txt))
			value_txt = head_txt + value_txt

			if self.connection:
				# print(value_txt)
				# print(data)
				self.cursor.execute(value_txt, data)
				self.connection.commit()

	def search(self, filters={}, table=''):
		'''
		filters [dict]
			|_ key in values is a name field in table
		table [str]
			|_ table name
		'''
		result = []
		if table:
			where_txt = 'SELECT * FROM {} '.format(table)
			data = []
			
			if filters:

				filter_key = list(filters.keys())
				for f in filter_key:

					if f == filter_key[0]:
						where_txt += 'WHERE {}=? '.format(f)
						data.append(filters[f])

					else:
						where_txt += 'AND {}=? '.format(f)
						data.append(filters[f])

			if self.connection:
				self.cursor.execute(where_txt, data)
				result = self.cursor.fetchall()

		# print(result)
		return result

	def update(self, table='', values={}, filters={}):
		'''
		table [str]
			|_ table name
		values [dict]
			|_ key in values is a name field in table [new value]
		filters [dict]
			|_ key in values is a name field in table [old value]
		'''
		if table and values and filters:
			set_txt = 'UPDATE {} '.format(table)
			where_txt = ''
			data = []

			value_key = list(values.keys())
			for value in values.keys():

				if value == value_key[0]:
					set_txt += 'SET {}=? '.format(value)
					data.append(values[value])

				else:
					set_txt += ', {}=? '.format(value)
					data.append(values[value])

			filter_key = list(filters.keys())
			for f in filter_key:

				if f == filter_key[0]:
					where_txt += 'WHERE {}=? '.format(f)
					data.append(filters[f])

				else:
					where_txt += 'AND {}=? '.format(f)
					data.append(filters[f])

			command = '{}{}'.format(set_txt, where_txt)
			# print(command)
			# print(data)

			if self.connection:
				self.cursor.execute(command, data)
				self.connection.commit()

	def delete(self, filters={}, table=''):
		'''
		filters [dict]
			|_ key in values is a name field in table
		table [str]
			|_ table name
		'''
		if filters and table:
			where_txt = 'DELETE FROM {} '.format(table)
			data = []

			filter_key = list(filters.keys())
			for f in filter_key:

				if f == filter_key[0]:
					where_txt += 'WHERE {}=? '.format(f)
					data.append(filters[f])

				else:
					where_txt += 'AND {}=? '.format(f)
					data.append(filters[f])

			if self.connection:
				self.cursor.execute(where_txt, data)
				self.connection.commit()

	


if __name__ == '__main__':
	path = "T:/rnd/zeafrost/work/shot/101/S01/0010/anm/.yggpipdata/files.db"
	db_local = SQLITE_BASE()
	# db_local.create(path=path, fields=['id', 'name'], table='users')
	db_local.connect(path=path)

	# db_local.insert(table='users', values={'id': 2, 'name': 'thaksaporn'})
	print(db_local.search(table='users', filters={}))
	# db_local.update(table='users', filters={'name': 'thaksaporn'}, values={'name': 'phone'})
	# db_local.delete(table='users', filters={'name': 'phone'})



	db_local.close_connection()
