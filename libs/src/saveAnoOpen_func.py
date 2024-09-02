import os
import sys
import platform
import subprocess
import re
from pprint import pprint

# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

import libs.database_manage.sqlite_project as db_project
reload(db_project)
import libs.database_manage.sqlite_program as db_program
reload(db_program)

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
    
    # Parse the output
    #-----------------
    for line in output.splitlines():

        display_name = ''

        if "DisplayName" in line:
            display_name = line.split("    ")[-1].strip()
        
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
            if f"{program_name}.exe" in files and ver in root:
                path = os.path.join(root, f"{program_name}.exe")
                path = path.replace('\\', '/')
                return path
    return None
    
def get_dcc():

    db = db_program.SQLITE_PROGRAM_DB()
    result = db.search_program_data()

    return result


