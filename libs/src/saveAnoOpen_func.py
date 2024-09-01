import os
import sys
import platform

# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

import libs.database_manage.sqlite_project as db_project
reload(db_project)

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
    


        
    