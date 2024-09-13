
# -*- coding: utf-8 -*-

import os
import sys
import time
import platform
# import logging
import copy
from datetime import datetime
from pprint import pprint

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

MODULE_PATH = os.path.dirname(__file__).replace('\\', '/')
PATHS = [ MODULE_PATH , os.path.dirname(MODULE_PATH)]
for path in PATHS:
	if not path in sys.path:
		sys.path.append(path)

import libs.src.saveAndOpen_func as func
reload(func)
import sao_utilityDialog as util
reload(util)

DCC = func.get_cur_dcc()

PROJECT = os.getenv("SAO_PROJECT") or ''
CSS_PATH =  '{}/saveAndOpenTool_style.css'.format(MODULE_PATH)
EXT_FILE = []

class SceneManagerUI(QDialog):
	def __init__(self, parent = None, ext=[], project='_other'):
		super(self.__class__, self).__init__(parent)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setSpacing(0)
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.setLayout(self.mainLayout)

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)

		self.setWindowTitle('Save And Open Tool')
		self.setLayout(panel)
		self.resize(1225,800)
		self.setMinimumSize(1300,700)
		self.setContentsMargins(0,0,0,0)

		self.dcc = func.create_db_program()
		self.cur_dcc = DCC
		self.ext = ext
		self.dcc_dataItem = {}
		self.project_dataItem = {}
		self.project = project
		self.path_lookIn = func.get_path_default(project)
		self.css_main = ''

		with open(CSS_PATH, 'r') as css:
			self.css_main = css.read()
		
		self.setStyleSheet(self.css_main)

		self.initTitleWidget()
		self.initBodyWidget()

		if not DCC:
			self.initBottomWidget()
			self.showListDcc()

		self.showListProject()

		self.showLookInPath()
		self.showFileItems()
		self.showRecentFile()
		

	def mousePressEvent(self,event):
		self.moving = True
		self.offset = event.pos()

		self.old_Pos = event.globalPos()
		self.old_width = self.width()
		self.old_height = self.height()

		self.mouse_pos = self.mapToGlobal(self.offset)

	def mouseMoveEvent(self,event):
		if self.old_Pos:
			delta = QPoint(event.globalPos() - self.old_Pos)
			if (self.old_Pos.x() > self.x() + self.old_width - 15) or (self.old_Pos.y() > self.y() + self.old_height - 15):
				self.resize(self.old_width + delta.x(), self.old_height + delta.y())
				# self.setFixedSize(self.old_width + delta.x(), self.old_height + delta.y())
			else:
				self.move(self.x() + delta.x(), self.y() + delta.y())
				self.old_Pos = event.globalPos()

	def mouseReleaseEvent(self, event):
		self.old_Pos = None

	def showEvent(self,event):
		self.repaint()

	def initTitleWidget(self):

		titleLayout = QHBoxLayout()
		titleWidget = QDialog()
		titleWidget.setLayout(titleLayout)
		self.mainLayout.addWidget(titleWidget)

		titleLabel = QLabel('Save And Open Tool')
		titleLayout.addWidget(titleLabel)
		titleLabel.setStyleSheet('font-size: 18px; margin-left: 10px')

		self.miniBtn = QPushButton('_')
		self.miniBtn.setFixedSize(30, 30)
		self.miniBtn.clicked.connect(self.showMinimized)
		titleLayout.addWidget(self.miniBtn)

		self.miniBtn.setStyleSheet('''
		QPushButton{
			background: rgba(0, 0, 0,0);
			border: none;
			border-radius: 3px;
			color: #3b87d3;
			font-size: 14px
		}
		QPushButton:hover{
			background: #3b87d3;
			color: rgb(0, 0, 0)
		}
		''')

		self.closeBtn = QPushButton('X')
		self.closeBtn.setFixedSize(30, 30)
		self.closeBtn.clicked.connect(self.close)
		titleLayout.addWidget(self.closeBtn)

		self.closeBtn.setStyleSheet('''
		QPushButton{
			background: rgba(0, 0, 0,0);
			border: none;
			border-radius: 3px;
			color: red;
			font-size: 14px
		}
		QPushButton:hover{
			background: red;
			color: rgb(0, 0, 0)
		}
		''')

	def initBodyWidget(self):

		self.bodyLayout = QSplitter()
		self.bodyLayout.setHandleWidth(2)
		self.bodyLayout.setOrientation(Qt.Horizontal)
		self.bodyLayout.setStyleSheet(self.css_main)
		if DCC:
			self.bodyLayout.setFixedHeight(730)
		else:
			self.bodyLayout.setFixedHeight(600)
		self.mainLayout.addWidget(self.bodyLayout)

		self.initProjectWidget()
		self.initRecentWidget()
		self.initFileWidget()
		
	def initProjectWidget(self):	

		# Project Layout
		#-----------------
		projectLayout = QVBoxLayout()
		projectLayout.setAlignment(Qt.AlignTop)
		projectLayout.setContentsMargins(30, 0, 10, 10)
		projectWidget = QDialog()
		projectWidget.setFixedWidth(200)
		projectWidget.setLayout(projectLayout)
		self.bodyLayout.addWidget(projectWidget)

		projectTitleLayout = QHBoxLayout()
		projectTitleLayout.setContentsMargins(0,0,0,0)
		projectTitleWidget = QDialog()
		projectTitleWidget.setLayout(projectTitleLayout)
		projectLayout.addWidget(projectTitleWidget)

		projectLabel = QLabel('Project')
		projectTitleLayout.addWidget(projectLabel)

		self.createProjectBtn = QPushButton('+')
		self.createProjectBtn.setFixedSize(25,25)
		self.createProjectBtn.clicked.connect(self.showAddProject)
		projectTitleLayout.addWidget(self.createProjectBtn)
		self.createProjectBtn.setStyleSheet('''
		QPushButton{
			background: rgba(0, 0, 0,0);
			border: none;
			border-radius: 3px;
			color: rgb(190,190,190);
			font-size: 14px
		}
		QPushButton:hover{
			background: rgba(0, 0, 0,0);
			color: #3b87d3;
		}
		''')

		self.projectTree = QTreeWidget()
		projectLayout.addWidget(self.projectTree)

		projectScrollbar = QScrollBar()
		self.projectTree.setVerticalScrollBar(projectScrollbar)
		self.projectTree.setRootIsDecorated(False)
		self.projectTree.setHeaderHidden(True)
		self.projectTree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.projectTree.setAutoScroll(True)
		self.projectTree.setStyleSheet(self.css_main)
		self.projectTree.itemClicked.connect(self.doClickProject)
		
	def initRecentWidget(self):

		# Recent Layout
		#-----------------
		recentLayout = QVBoxLayout()
		recentLayout.setAlignment(Qt.AlignTop)
		recentLayout.setContentsMargins(20, 0, 10, 10)
		recentWidget = QDialog()
		recentWidget.setMinimumWidth(350)
		recentWidget.setLayout(recentLayout)
		self.bodyLayout.addWidget(recentWidget)

		recentTitleLayout = QHBoxLayout()
		recentTitleLayout.setContentsMargins(0,0,0,0)
		recentTitleWidget = QDialog()
		recentTitleWidget.setLayout(recentTitleLayout)
		recentLayout.addWidget(recentTitleWidget)

		recentLabel = QLabel('Recent')
		recentTitleLayout.addWidget(recentLabel)

		self.recentSearch = util.SearchBoxWidget()
		self.recentSearch.line.textChanged.connect(self.doSearchRecent)
		self.recentSearch.search_btn.clicked.connect(self.doSearchRecent)
		self.recentSearch.setStyleSheet('''
			border-radius: 0px;  border-bottom: 2px solid rgba(70, 70, 70, 100); background: rgba(40,40,40,100)''')
		self.recentSearch.setFixedSize(180, 22)
		recentTitleLayout.addWidget(self.recentSearch)

		self.recentTree = QTreeWidget()
		self.recentTree.itemDoubleClicked.connect(self.doDoubleClickRecent)
		self.recentTree.itemClicked.connect(self.doClickRecent)
		self.recentTree.setStyleSheet('padding-left: 5px; border: 0px;')
		recentLayout.addWidget(self.recentTree)
		self.recentTree.setStyleSheet(self.css_main)
		self.recentTree.setRootIsDecorated(False)
		self.recentTree.setHeaderHidden(False)
		self.recentTree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.recentTree.setAutoScroll(False)
		self.recentTree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.recentTree.setHeaderLabels(['name', 'date', 'comment', 'location'])
		self.recentTree.setColumnWidth(0, 225)
		self.recentTree.setColumnWidth(1, 95)
		self.recentTree.setColumnWidth(2, 70)


		# command for sort tree item
		#---------------------------
		self.recentTree.sortByColumn(4,Qt.AscendingOrder)
		self.recentTree.setSortingEnabled(True)
		self.recentTree.header().setSortIndicatorShown(False)

	def initFileWidget(self):

		# Location Layout
		#-----------------
		locationLayout = QVBoxLayout()
		locationLayout.setAlignment(Qt.AlignTop)
		locationLayout.setContentsMargins(20, 0, 10, 10)
		locationWidget = QDialog()
		locationWidget.setLayout(locationLayout)
		self.bodyLayout.addWidget(locationWidget)

		locationTitleLayout = QHBoxLayout()
		locationTitleLayout.setContentsMargins(0,0,0,0)
		locationTitleWidget = QDialog()
		locationTitleWidget.setLayout(locationTitleLayout)
		locationLayout.addWidget(locationTitleWidget)

		locationLabel = QLabel('Location File')
		locationTitleLayout.addWidget(locationLabel)

		self.fileSearch = util.SearchBoxWidget()
		self.fileSearch.line.textChanged.connect(self.doSearchFile)
		self.fileSearch.search_btn.clicked.connect(self.doSearchFile)
		self.fileSearch.setStyleSheet('''
			border-radius: 0px;  border-bottom: 2px solid rgba(70, 70, 70, 100); background: rgba(40,40,40,100)''')
		self.fileSearch.setFixedSize(180, 22)
		locationTitleLayout.addWidget(self.fileSearch)

		self.backBtn = QPushButton()
		self.backBtn.clicked.connect(self.doBackFile)
		self.backBtn.setFixedSize(36,24)
		self.backBtn.setStyleSheet('''
			QPushButton{border:none; image:url('''+MODULE_PATH+'''/icons/arrow_up.png);border:2px solid rgb(66,66,66); border-radius:4px;}
			QPushButton:hover:!pressed{background:rgb(44,44,44); border-color:rgb(85,85,85); color:rgb(200,200,200);}''')

		browseLayout = QHBoxLayout()
		browseLayout.setContentsMargins(0,0,0,0)
		locationLayout.addLayout(browseLayout)

		lookInLabel = QLabel('Look in : ')
		browseLayout.addWidget(lookInLabel)

		self.pathBox = QLineEdit()
		self.pathBox.setText(self.path_lookIn)
		self.pathBox.setFixedHeight(25)
		self.pathBox.setStyleSheet(self.css_main)
		browseLayout.addWidget(self.pathBox)

		browseLayout.addWidget(self.backBtn)

		self.fileTree = QTreeWidget()
		locationLayout.addWidget(self.fileTree)
		self.fileTree.itemDoubleClicked.connect(self.doDoubleClickFile)
		self.fileTree.itemClicked.connect(self.doClickFile)
		self.fileTree.setStyleSheet('padding-left: 5px; border: 0px;')
		self.fileTree.setStyleSheet(self.css_main)
		self.fileTree.setRootIsDecorated(False)
		self.fileTree.setHeaderHidden(False)
		self.fileTree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.fileTree.setAutoScroll(False)
		self.fileTree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.fileTree.setHeaderLabels(['  name', 'date','owner', 'comment'])
		self.fileTree.setColumnWidth(0, 350)
		self.fileTree.setColumnWidth(1, 95)
		self.fileTree.setColumnWidth(2, 70)

		# command for sort tree item
		#---------------------------
		self.fileTree.sortByColumn(4,Qt.AscendingOrder)
		self.fileTree.setSortingEnabled(True)
		self.fileTree.header().setSortIndicatorShown(False)

		fileScrollbar = QScrollBar()
		self.fileTree.setVerticalScrollBar(fileScrollbar)

		manage_file_layout = QHBoxLayout()
		manage_file_layout.setContentsMargins(0,0,0,0)
		manage_file_widget = QDialog()
		manage_file_widget.setLayout(manage_file_layout)
		manage_file_widget.setFixedHeight(120)
		locationLayout.addWidget(manage_file_widget)

		detail_layout = QVBoxLayout()
		manage_file_layout.addLayout(detail_layout)

		name_label = QLabel('Name :')
		detail_layout.addWidget(name_label)

		self.name_edit = QLineEdit()
		self.name_edit.setFixedHeight(25)
		self.name_edit.setStyleSheet(self.css_main)
		detail_layout.addWidget(self.name_edit)

		comment_label = QLabel('comment :')
		detail_layout.addWidget(comment_label)

		self.comment_edit = QTextEdit()
		self.comment_edit.setFixedHeight(40)
		self.comment_edit.setStyleSheet(self.css_main)
		detail_layout.addWidget(self.comment_edit)

		action_file_layout = QVBoxLayout()
		action_file_layout.setAlignment(Qt.AlignCenter)
		action_file_layout.setContentsMargins(20,40,10,10)
		action_file_widget = QDialog()
		action_file_widget.setLayout(action_file_layout)
		manage_file_layout.addWidget(action_file_widget)
		
		self.saveBtn = QPushButton('Save')
		self.saveBtn.clicked.connect(self.doSaveScene)
		self.saveBtn.setFixedSize(150, 30)

		if DCC:
			action_file_layout.addWidget(self.saveBtn)

		self.openBtn = QPushButton('Open')
		self.openBtn.clicked.connect(self.doClickOpenScene)
		self.openBtn.setFixedSize(150, 30)
		action_file_layout.addWidget(self.openBtn)

	def initBottomWidget(self):

		self.bottomLayout = QVBoxLayout()
		bottomWidget = QDialog()
		# bottomWidget.setFixedHeight(150)
		bottomWidget.setLayout(self.bottomLayout)
		self.mainLayout.addWidget(bottomWidget)

		bottomTitleLayout = QHBoxLayout()
		bottomTitleLayout.setAlignment(Qt.AlignLeft)
		bottomTitleLayout.setContentsMargins(0,0,0,0)
		bottomTitleWidget = QDialog()
		bottomTitleWidget.setLayout(bottomTitleLayout)
		self.bottomLayout.addWidget(bottomTitleWidget)

		bottomLabel = QLabel('Dcc')
		bottomLabel.setFixedWidth(25)
		bottomTitleLayout.addWidget(bottomLabel)

		self.dccRefreshBtn = QPushButton()
		self.dccRefreshBtn.clicked.connect(self.doRefreshDcc)
		self.dccRefreshBtn.setFixedSize(15,15)
		self.dccRefreshBtn.setStyleSheet('''
			QPushButton{border:none; image:url('''+MODULE_PATH+'''/icons/refresh.png);border:none; border-radius:4px;background: rgba(0,0,0,0)}
			QPushButton:hover:!pressed{background:rgb(44,44,44); border-color:rgb(85,85,85); color:rgb(200,200,200);}''')
		bottomTitleLayout.addWidget(self.dccRefreshBtn)

		self.dccList = QListWidget()
		self.dccList.setViewMode(QListView.IconMode)
		self.dccList.setResizeMode(QListWidget.Adjust)
		self.dccList.setSizeAdjustPolicy(QListWidget.AdjustToContents)
		self.dccList.setWrapping(True)
		self.dccList.setMovement(QListWidget.Static)
		self.dccList.setIconSize(QSize(142.4, 80))
		self.dccList.setSpacing(15)
		self.dccList.itemDoubleClicked.connect(self.doOpenDcc)
		self.dccList.itemClicked.connect(self.doClickDCC)
		self.bottomLayout.addWidget(self.dccList)

	def showAddProject(self):
		
		self.addProjectDialog = util.ProjectAddDialog()
		self.addProjectDialog.add_btn.clicked.connect(self.addProject)
		self.addProjectDialog.exec_()

	def addProject(self):
		
		name = self.addProjectDialog.name_edit.text()
		path = self.addProjectDialog.path_edit.text().replace('\\', '/')
		self.addProjectDialog.close()

		# add project to db
		#------------------
		check_crate = func.create_project(name=name, path=path)

		# if check_crate:
		self.showListProject()

		# select project item
		#--------------------
		items = self.projectTree.findItems(name, Qt.MatchExactly)
		item_select = ''

		for item in items:
			name_item = item.text(0)
			if name_item == name:
				item_select = item

		if item_select:
			item_select.setSelected(True)
			self.projectTree.scrollToItem(item_select)

	def showListProject(self):

		self.projectTree.clear()
		self.project_dataItem = {}

		project_result = func.search_project(filters={})
		self.project_data = {}
		projects = []
		check_other = False
		
		# add item to widget
		#-------------------
		for data in project_result:
			name = data['name']
			if name == '_other':
				check_other = True
			else:
				projects.append(name)

			self.project_data[name] = copy.deepcopy(data)

		projects.sort()
		if check_other:
			projects.insert(0, '_other')

		itemSelect = ''

		for name in projects:
			project_item = QTreeWidgetItem(self.projectTree)
			project_widget = util.ItemTreeProject(text=name)
			self.projectTree.addTopLevelItem(project_item)

			# project_item.setText(0, name)

			project_size = project_widget.size()
			project_item.setSizeHint(0, project_size)
			
			self.projectTree.setItemWidget(project_item, 0, project_widget)
			self.project_dataItem[str(project_item)] = {'name': name, path : self.project_data[name]['path']}

			if name == self.project:
				itemSelect = project_item

		if itemSelect:
			itemSelect.setSelected(True)
			self.projectTree.setCurrentItem(itemSelect)
			self.projectTree.scrollTo(self.projectTree.indexFromItem(itemSelect))

	def showListDcc(self):

		self.dccList.clear()
		self.dcc_dataItem = {}

		dcc = func.get_dcc()
		sorted_dcc = sorted(dcc, key= lambda x: x['name'])

		for data in sorted_dcc:
			item = util.DccItemWidget(self.dccList)
			name = '{} {}'.format(data['shortname'], data['version'])
			item.setText(name)
			item.set_thumbnail(data['shortname'])
			item.setToolTip(data['name'])

			self.dccList.addItem(item)
			self.dcc_dataItem[str(item)] = copy.deepcopy(data)

	def doRefreshDcc(self):

		QApplication.setOverrideCursor(Qt.WaitCursor)

		self.dcc = func.create_db_program(clear=True)
		self.showListDcc()

		QApplication.restoreOverrideCursor()

	def doOpenDcc(self):

		QApplication.setOverrideCursor(Qt.WaitCursor)

		current_item = self.dccList.currentItem()

		if str(current_item) in self.dcc_dataItem.keys():

			path = self.dcc_dataItem[str(current_item)]['path']
			func.open_dcc(path=path, project=self.project, dcc=self.dcc_dataItem[str(current_item)]['shortname'])

		QApplication.restoreOverrideCursor()

	def doClickProject(self):

		project_item = self.projectTree.currentItem()
		if project_item and str(project_item) in self.project_dataItem.keys():
				self.project = self.project_dataItem[str(project_item)]['name']
				self.showLookInPath()
				self.showFileItems()

	def showFileItems(self):

		path = self.pathBox.text()
		self.fileTree.clear()

		folders_path = []
		files_path = []

		if path:
			if os.path.exists(path):
				for item in os.listdir(path):
					fullpath = '{}/{}'.format(path, item)
					if not item == '__pycache__':
						if '.' in item:
							ext = item.rpartition('.')[-1]
							if ext in self.ext:
								files_path.append(fullpath)
						else:
							folders_path.append(fullpath)

		else:
			folders_path = ["{}:/".format(d) for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists("{}:\\".format(d))]

		folders_path.sort()
		files_path.sort()

		paths = folders_path + files_path

		for path in paths:

			item = QTreeWidgetItem(self.fileTree)
			self.fileTree.addTopLevelItem(item)

			data_file = func.get_data_file(path)

			if os.path.isdir(path):

				item.setIcon(0, QIcon('{}/icons/folder.png'.format(MODULE_PATH)))

			else:

				if path.endswith('.ma'):
					item.setIcon(0, QIcon('{}/icons/ma_file.png'.format(MODULE_PATH)))

				elif path.endswith('.mb'):
					item.setIcon(0, QIcon('{}/icons/mb_file.png'.format(MODULE_PATH)))
					
				elif path.endswith('.hip') or path.endswith('.hiplc') or path.endswith('.hipnc'):
					item.setIcon(0, QIcon('{}/icons/houdini.png'.format(MODULE_PATH)))

				elif path.endswith('.hip') or path.endswith('.blend'):
					item.setIcon(0, QIcon('{}/icons/blender.png'.format(MODULE_PATH)))

				else:
					item.setIcon(0, QIcon('{}/icons/files.png'.format(MODULE_PATH)))

				item.setText(1,data_file['date'])
				item.setText(2,data_file['owner'])
				item.setText(3,data_file['comment'])

			if path.endswith('/'):
				item.setText(0, path)

			else:
				item.setText(0, os.path.basename(path))

	def doDoubleClickFile(self):
		
		dir_path = self.pathBox.text()

		item= self.fileTree.currentItem()
		item_txt = item.text(0)

		if dir_path:
			if dir_path.endswith('/'):
				fullpath = '{}{}'.format(dir_path, item_txt)
			else:
				fullpath = '{}/{}'.format(dir_path, item_txt)
		else:
			fullpath = item_txt

		if os.path.isdir(fullpath):
			self.pathBox.setText(fullpath)
			self.showFileItems()
		else:
			self.doClickOpenScene()

	def doBackFile(self):

		path = self.pathBox.text()
		dirpath = ''

		if not path.endswith('/'):
			dirpath = os.path.dirname(path)

		self.pathBox.setText(dirpath)
		self.showFileItems()

	def showLookInPath(self):

		item = self.projectTree.currentItem()
		project = ''

		if item:
			project = item.text(0)

		if not project:
			project = self.project

		if project in self.project_data.keys():
			path = self.project_data[project]['path']
			self.pathBox.setText(path)

	def doSaveScene(self):

		dirpath = self.pathBox.text()
		name = self.name_edit.text()
		comment = self.comment_edit.toPlainText()

		if dirpath and name:
			if '.' in name:
				fullpath = '{}/{}'.format(dirpath, name)
				func.save_scene(
					path=fullpath,
					dcc=self.cur_dcc,
					project=self.project,
					comment=comment)

		self.close()

	def doClickFile(self):

		item = self.fileTree.currentItem()
		name = item.text(0)
		comment = item.text(3)

		if '.' in name:
			self.name_edit.setText(name)
			self.comment_edit.setText(comment)

	def showRecentFile(self):
		
		recent_files = func.get_recent_file()
		recent_files.reverse()

		for data in recent_files[:10]:

			ext = data['name'].rpartition('.')[-1]

			if ext in self.ext:

				item = QTreeWidgetItem(self.recentTree)
				self.recentTree.addTopLevelItem(item)
				

				if data['name'].endswith('.ma'):
					item.setIcon(0, QIcon('{}/icons/ma_file.png'.format(MODULE_PATH)))

				elif data['name'].endswith('.mb'):
					item.setIcon(0, QIcon('{}/icons/mb_file.png'.format(MODULE_PATH)))
					
				elif data['name'].endswith('.hip') or data['name'].endswith('.hiplc') or data['name'].endswith('.hipnc'):
					item.setIcon(0, QIcon('{}/icons/houdini.png'.format(MODULE_PATH)))

				elif data['name'].endswith('.hip') or data['name'].endswith('.blend'):
					item.setIcon(0, QIcon('{}/icons/blender.png'.format(MODULE_PATH)))

				else:
					item.setIcon(0, QIcon('{}/icons/files.png'.format(MODULE_PATH)))

				date = data['date'].rpartition('.')[0]
				date = date.replace('-', '/')
				date = date.rpartition(':')[0]

				item.setText(0, data['name'])
				item.setText(1, date)
				item.setText(2, data['comment'])
				item.setText(3, data['path'])
			
	def doClickOpenScene(self):

		QApplication.setOverrideCursor(Qt.WaitCursor)

		dir_path = self.pathBox.text()
		item = self.fileTree.currentItem()
		name = item.text(0)
		path_program = ''
		check_open = False

		if name:

			if dir_path.endswith('/'):
				fullPath = '{}{}'.format(dir_path, name)
			else:
				fullPath = '{}/{}'.format(dir_path, name)

			if os.path.exists(fullPath):

				if self.dcc_dataItem:
					item_dcc = self.dccList.currentItem()
					if item_dcc:
						data = self.dcc_dataItem[str(item_dcc)]
						path_program = data.get('path')

				check_open = func.open_scene(path=fullPath, dcc=self.cur_dcc, project=self.project, path_program=path_program)
				
			time.sleep(1)
			QApplication.restoreOverrideCursor()

			if check_open:
				self.close()

	def doDoubleClickRecent(self):

		QApplication.setOverrideCursor(Qt.WaitCursor)

		item = self.recentTree.currentItem()
		fullpath = item.text(3)
		path_program = ''
		check_open = False

		if os.path.exists(fullpath):

			if self.dcc_dataItem:
				item_dcc = self.dccList.currentItem()
				if item_dcc:
					data = self.dcc_dataItem[str(item_dcc)]
					path_program = data.get('path')

			check_open = func.open_scene(path=fullpath, dcc=self.cur_dcc, project=self.project, path_program=path_program)

		time.sleep(1)
		QApplication.restoreOverrideCursor()
		
		if check_open:
			self.close()

	def doClickRecent(self):

		item = self.recentTree.currentItem()
		path = item.text(3)
		dirpath = os.path.dirname(path)

		if os.path.exists(dirpath):
			self.pathBox.setText(dirpath)
			self.showFileItems()

	def doSearchRecent(self):

		search_txt = self.recentSearch.line.text().lower()

		for i in range(self.recentTree.topLevelItemCount()):
			item = self.recentTree.topLevelItem(i)
			name = item.text(0).lower()

			if search_txt in name:
				item.setHidden(False)

			else:
				item.setHidden(True)

	def doSearchFile(self):

		search_txt = self.fileSearch.line.text().lower()

		for i in range(self.fileTree.topLevelItemCount()):
			item = self.fileTree.topLevelItem(i)
			name = item.text(0).lower()

			if search_txt in name:
				item.setHidden(False)

			else:
				item.setHidden(True)

	def doClickDCC(self):

		current_item = self.dccList.currentItem()

		if str(current_item) in self.dcc_dataItem.keys():

			dcc = self.dcc_dataItem[str(current_item)]['shortname']
			ext = []

			if dcc == 'maya':
				ext = ['ma', 'mb']

			elif dcc == 'houdini':
				ext = ['hiplc', 'hip', 'hipnc']

			elif dcc == 'blender':
				ext = ['blend']

			if ext:

				for i in range(self.fileTree.topLevelItemCount()):
					item = self.fileTree.topLevelItem(i)
					name = item.text(0).lower()

					if '.' in name:
						search_txt = name.rpartition('.')[-1]

						if search_txt in ext:
							item.setHidden(False)
						else:
							item.setHidden(True)

				for i in range(self.recentTree.topLevelItemCount()):
					item = self.recentTree.topLevelItem(i)
					name = item.text(0).lower()

					if '.' in name:
						search_txt = name.rpartition('.')[-1]

						if search_txt in ext:
							item.setHidden(False)
						else:
							item.setHidden(True)












# ------------------------------------------- #
#               RUN TOOL FUNC                 #
# ------------------------------------------- #
def main():

	startTime = time.time()
	print(':: TOOL MASSAGE :: DCC --> {}'.format(DCC))

	if DCC == 'maya':

		from shiboken2 import wrapInstance
		import maya.OpenMayaUI as omui
		global maya_ui

		if PY_VERSION == 3:
			prt = wrapInstance(int(omui.MQtUtil.mainWindow()), QWidget)

		else:
			prt = wrapInstance(long(omui.MQtUtil.mainWindow()), QWidget)

		try:
			maya_ui.close()
		except:
			pass
		maya_ui = SceneManagerUI(parent=prt, ext=['ma', 'mb'], project=PROJECT)
		maya_ui.show()
		
	elif DCC == 'houdini':

		import hou

		temp = hou.ui.mainQtWindow()
		if temp:
			temp.setStyleSheet('background:none;')
		
		houdini_ui = SceneManagerUI(parent=temp, ext=['hiplc', 'hip', 'hipnc'], project=PROJECT)
		houdini_ui.show()
	
	elif DCC == 'blender':

		app = QApplication.instance()

		if app == None:
			app = QApplication(sys.argv)

		ui = SceneManagerUI(ext=['blend'], project=PROJECT)
		ui.exec_()


	else:
		app = QApplication(sys.argv)
		ui = SceneManagerUI(ext=['ma', 'mb', 'hiplc', 'hip', 'hipnc', 'blend'])
		ui.show()
		sys.exit(app.exec_())

	endTime = time.time()
	timeLap = endTime - startTime
	print(':: TOOL MASSAGE :: Time Open | {}'.format(timeLap))
	# logger.log(logging.INFO, '[{}] DCC : {} | {} | Time Open : {}'.format(PROJ_CODE, DCC, state, timeLap))


if __name__ == '__main__':
	main()
	# pprint(func.check_list_project())
