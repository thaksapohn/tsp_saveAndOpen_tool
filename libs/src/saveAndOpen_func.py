import os
import sys
import platform
import subprocess
import re
import datetime
import math
import getpass
from pprint import pprint
from datetime import datetime

# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

MODULE_PATH = os.path.dirname(__file__).replace('\\', '/')
PATHS = [ MODULE_PATH, os.path.dirname(os.path.dirname(MODULE_PATH)) ]
for path in PATHS:
	if not path in sys.path:
		sys.path.append(path)

import libs.database_manage.sqlite_project as db_project
reload(db_project)
import libs.database_manage.sqlite_program as db_program
reload(db_program)
import libs.database_manage.sqlite_file as db_file
reload(db_file)

import getOwnerFile
reload(getOwnerFile)

USER = getpass.getuser().lower()

def create_project(name='', path=''):

	db = db_project.SQLITE_PROJECT_DB()
	check_project_other()

	# check db in project
	#--------------------
	filters = {'name': name}
	search_result = db.search_project_data(filters=filters)

	if search_result:
		return False

	else:
		payload = {
			'name': name,
			'path': path }

		db.insert_project_data(values=payload)
		return True

def check_project_other():
	db = db_project.SQLITE_PROJECT_DB()

	# check db in project
	#--------------------
	filters = {'name': '_other'}
	search_result = db.search_project_data(filters=filters)

	if not search_result:
		payload = {
			'name': '_other',
			'path': '' }

		db.insert_project_data(values=payload)

def search_project(filters={}):

	db = db_project.SQLITE_PROJECT_DB()
	search_result = db.search_project_data(filters=filters)

	return search_result

def create_db_program(clear=False):
	
	db = db_program.SQLITE_PROGRAM_DB()

	if os.path.exists(db.db_path):

		if clear:
			db.delete_program_db()

			programs = check_list_project()

			for data in programs:
				
				# check exists program
				#---------------------
				result_check = db.search_program_data(filters={'name': data['name']})

				if not result_check:
					db.insert_program_data(values=data)

	else:

		programs = check_list_project()

		for data in programs:
			
			# check exists program
			#---------------------
			result_check = db.search_program_data(filters={'name': data['name']})

			if not result_check:
				db.insert_program_data(values=data)

def check_list_project():

	print(':: TOOL MASSAGE :: list program process...')

	maya_list = []
	houdini_list = []
	blender_list = []

	dataReturn = []

	# Command to list installed programs from the registry
	#-----------------------------------------------------
	cmd = r'reg query HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Uninstall /s'
	
	# Execute the command and decode the output
	#------------------------------------------
	output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
	path_install = ''
	
	# Parse the output
	#-----------------
	for line in output.splitlines():

		display_name = ''

		if "DisplayName" in line:
			display_name = line.split("    ")[-1].strip()

		if 'InstallLocation' in line:
			path_install = line.split("    ")[-1]

		
		if display_name:
			data = {}
			if 'autodesk maya' in display_name.lower():

				if not display_name in maya_list:

					maya_list.append(display_name)

					ver = display_name.split(' ')[-1]
					path = get_program_path('maya', ver)

					data = {'name': display_name, 'path': path, 'version': ver, 'shortname': 'maya'}
					dataReturn.append(data)

			elif 'houdini' in display_name.lower():

				if not display_name in houdini_list:

					houdini_list.append(display_name)
					
					ver = display_name.split(' ')[-1]
					path = get_program_path('houdini', ver)

					data = {'name': display_name, 'path': path, 'version': ver, 'shortname': 'houdini'}
					dataReturn.append(data)

			elif 'blender' in display_name.lower():

				if not display_name in blender_list:

					if 'blender' in path_install.lower():
						display_name = os.path.basename(os.path.dirname(path_install))

					blender_list.append(display_name)
					ver = ''
					
					if re.findall('([0-9])', display_name):
						ver = display_name.split(' ')[-1]

					path = get_program_path('blender', ver)

					if path:
						ver = path.split('/')[-2].split(' ')[-1]

					data = {'name': display_name, 'path': path, 'version': ver, 'shortname': 'blender'}
					dataReturn.append(data)

	return dataReturn

def get_program_path(program_name, ver):

	common_paths = [
		r"C:\Program Files",
		r"C:\Program Files (x86)"
	]
	
	for path in common_paths:
		for root, dirs, files in os.walk(path):
			if "{}.exe".format(program_name) in files and ver in root:
				path = os.path.join(root, "{}.exe".format(program_name))
				path = path.replace('\\', '/')
				return path
	return None
	
def get_dcc():

	db = db_program.SQLITE_PROGRAM_DB()
	result = db.search_program_data()

	return result

def open_dcc(path, project='', dcc=''):

	if os.path.exists(path):

		os.environ['SAO_PROJECT'] = project
		os.environ['SAO_DCC'] = dcc

		command = ''

		if dcc == 'maya':
			command = "import maya.standalone; maya.standalone.initialize(); cmds.file(new=True, force=True); os.environ['SAO_PROJECT'] = {}".format(project)
			subprocess.Popen([path, '-command', command])

		elif dcc == 'houdini':
			subprocess.Popen([path])

		elif dcc == 'blender':
			subprocess.Popen([path, '--factory-startup'])
			
def get_path_default(project):

	pathReturn = ''

	if not project == '_other':
		pathReturn = ''

	return pathReturn

def get_data_file(path=''):
	
	data = {
			'name': os.path.basename(path),
			'full_path': path,
			'comment':'',
			'date': '',
			'size': '',
			'owner': '',
			'permission':'',
			'thumbnail': ''}

	#---------------
	# DATE
	fileTime = datetime.fromtimestamp(os.path.getmtime(path))
	dateModified = str(fileTime.strftime('%Y/%m/%d %H:%M'))
	data['date'] = dateModified

	#---------------
	# SIZE
	size = '0 B'
	size_raw = os.path.getsize(path)

	if not size_raw == 0:
		size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
		i = int(math.floor(math.log(size_raw,1024)))
		p = math.pow(1024,i)
		s = round(size_raw/p,2)
		size = '%s %s' % (s, size_name[i])

	data['size'] = size

	#---------------
	# OWNER
	try:
		pSD = getOwnerFile.get_file_security(path)
		owner_name, owner_domain, owner_sid_type = pSD.get_owner()
	except: owner_name = ''

	data['owner'] = owner_name

	#---------------
	# PERMISSION
	permission = os.access(path, os.W_OK) 
	if permission == True:
		permission_text = 'W/R'
	else:
		permission_text = 'R'

	data['permission'] = permission_text

	#---------------
	# COMMENT AND THUMBNAIL
	sqFile = db_file.SQLITE_FILE_DB()
	result_file = sqFile.search_file_data(filters={'filepath': path})

	if result_file:
		comment = result_file[-1][2] # index [2] is description
		thumbnail = result_file[-1][-1] # index [7] is thumbnail path
		data['comment'] = comment
		data['thumbnail'] = thumbnail

	# pprint(data)
	return data
	
def save_scene(path, dcc, project, comment=''):
	db = db_file.SQLITE_FILE_DB()
	
	if dcc == 'maya':

		import maya.cmds as mc

		mc.file(rename=path)
		mc.file(save=True)

	elif dcc == 'houdini':

		import hou
		
		hou.hipFile.setName(path)
		hou.hipFile.save(save_to_recent_files=False)

	elif dcc == 'blender':

		import bpy
		bpy.ops.wm.save_as_mainfile(filepath=path)

	if project:
		os.environ['SAO_PROJECT'] = project

	result_search = db.search_file_data(filters={'filepath':path})
	if result_search:
		values = {'comment':comment}
		db.update_file_data(filters={'filepath':path}, values=values)
		db.insert_recent_data(
			filepath=path, 
			description=comment, 
			project=project, 
			dcc=dcc)
	else:
		db.insert_file_data(
			filepath=path,
			description=comment,
			dcc=dcc,
			project=project,
			user = USER)

def get_recent_file():
	
	result = []

	db = db_file.SQLITE_FILE_DB()
	data_files = db.search_recent_data()
	index = 0

	path_check = {}

	for data in data_files:

		# pprint(data)
		parse_data = {}

		parse_data['id'] = data[0]
		parse_data['name'] = data[1]
		parse_data['comment'] = data[2]
		parse_data['date'] = data[3]
		parse_data['project'] = data[4]
		parse_data['dcc'] = data[5]
		parse_data['path'] = data[6]

		for index, data_dict in enumerate(result):
			if data_dict.get('path') == data[6]:
				del result[index]
				break

		result.append(parse_data)


	return result

def get_cur_dcc():

	dcc = ''
	programs = ['houdini.exe']

	if sys.argv[0]:

		if sys.argv[0].endswith('maya.exe'):
			dcc = 'maya'

		elif sys.argv[0].endswith('blender.exe'):
			dcc = 'blender'

	else:

		for program in programs:
			cmd = 'tasklist /fi "imagename eq {}"'.format(program)
			output = subprocess.check_output(cmd, shell= True).decode()
			if program.lower() in output.lower():
				dcc = program.rpartition('.')[0]
				break

	return dcc

def open_scene(path, dcc, project, path_program = ''):

	check_open = False
	
	if dcc == 'maya':

		import maya.mel as mel

		typeFile = 'mayaAscii'

		if path.endswith('.mb'): 
			typeFile = 'mayaBinary'

		cmd = 'file -f -options "v=0;" -ignoreVersion -typ "{}" -pmt 0 -esn false -o "'.format(typeFile) + path + '" ;'
			
		try: 
			mel.eval(cmd)
			check_open = True
		except: pass

	elif dcc == 'houdini':

		import hou

		hou.hipFile.load(path, suppress_save_prompt=False)
		check_open = True

	elif dcc == 'blender':

		import bpy

		bpy.ops.wm.open_mainfile(filepath = path)

	else:
		if path_program:

			if path.endswith('.ma') or path.endswith('.ma'):
				subprocess.Popen([path_program, '-file', path])

			elif path.endswith('.hip') or path.endswith('.hiplc') or path.endswith('.hipnc'):
				subprocess.Popen([path_program, path])

			elif path.endswith('.blend'):
				subprocess.Popen([path_program, path])

		else:
			print(':: TOOL MASSAGE :: Please Select Program')

	# record recent file
	#-------------------
	db = db_file.SQLITE_FILE_DB()
	date = datetime.now()

	db.insert_recent_data(
		filepath=path, 
		description='open file', 
		project=project , 
		dcc=dcc, 
		date=date )

	return check_open


if __name__ == '__main__':
	
	data = get_recent_file()
	pprint(data)

