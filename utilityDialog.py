
# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import platform
import glob
from pprint import pprint

try:
	from PySide2.QtCore import *
	from PySide2.QtWidgets import *
	from PySide2.QtGui import *
except:
	from PySide.QtCore import *
	from PySide.QtGui import *

# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

MODULE_PATH = os.path.dirname(__file__).replace('\\','/')

EP_CODE = os.getenv("YGG_EPISODE") or ''
SEQ_CODE = os.getenv("YGG_SEQUENCE") or ''
SHOT_CODE = os.getenv("YGG_SHOT") or ''
STEP_CODE = os.getenv("YGG_STEP") or ''
PROJ_CODE = os.getenv("YGG_PROJECT") or ''
ASSET_CODE = os.getenv("YGG_ASSET") or ''
ASSETTYPE_CODE = os.getenv("YGG_ASSETTYPE") or ''
VARIATION_CODE = os.getenv("YGG_ASSETVARIATION") or ''
TASKS_DATA = os.getenv("YGG_TASKS_DATA") or {}

ENTITY_CODE = os.getenv("YGG_ENTITY")
if ENTITY_CODE:
	ENTITY = ENTITY_CODE

else:
	ENTITY = 'shot'
	# if EP_CODE:
	# 	ENTITY = 'shot'
	# else:
	# 	ENTITY = 'asset'

try: 
	from . import saveAndOpenTool_func as func
	reload(func)
except:
	import saveAndOpenTool_func as func
	reload(func)

#--------------------------------------------
# TEST DATA
# PROJ_CODE = 'TWH'	
# ENTITY = 'asset'

class ItemTreeSelect(QDialog):
	def __init__(self, parent = None, episode=False, sequence=False, text=''):
		super(self.__class__, self).__init__(parent)

		self.main_layout = QHBoxLayout()
		self.main_layout.setContentsMargins(5,0,0,0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		if episode:
			icon = QIcon('{}/icons/episode.png'.format(MODULE_PATH))
		elif text == 'cam':
			icon = QIcon('{}/icons/category/cam.png'.format(MODULE_PATH))
		elif text == 'char':
			icon = QIcon('{}/icons/category/char.png'.format(MODULE_PATH))
		elif text == 'prop':
			icon = QIcon('{}/icons/category/prop.png'.format(MODULE_PATH))
		elif text == 'set':
			icon = QIcon('{}/icons/category/set.png'.format(MODULE_PATH))
		elif text == 'cmb':
			icon = QIcon('{}/icons/category/cmb.png'.format(MODULE_PATH))
		elif text == 'dmp':
			icon = QIcon('{}/icons/category/dmp.png'.format(MODULE_PATH))
		elif text == 'env':
			icon = QIcon('{}/icons/category/env.png'.format(MODULE_PATH))
		elif text == 'fx':
			icon = QIcon('{}/icons/category/fx.png'.format(MODULE_PATH))
		elif text == 'master':
			icon = QIcon('{}/icons/category/all.png'.format(MODULE_PATH))
		elif text == 'scat':
			icon = QIcon('{}/icons/category/scat.png'.format(MODULE_PATH))
		elif text == 'trn':
			icon = QIcon('{}/icons/category/trn.png'.format(MODULE_PATH))
		elif text == 'vhcl':
			icon = QIcon('{}/icons/category/vhcl.png'.format(MODULE_PATH))
		elif text == 'elem':
			icon = QIcon('{}/icons/category/all.png'.format(MODULE_PATH))
		else:
			icon = QIcon('{}/icons/sequence.png'.format(MODULE_PATH))

		pixmap = icon.pixmap(23,23, QIcon.Active, QIcon.On)
		inst_icon = QLabel()
		inst_icon.setFixedWidth(30)
		inst_icon.setPixmap(pixmap)

		label = QLabel(text)
		label.setStyleSheet('color: rgb(190, 190, 190);')
		label.setFixedHeight(30)

		self.main_layout.addWidget(inst_icon)
		self.main_layout.addWidget(label)

		self.resize(190,30)
		self.setStyleSheet('background: rgba(0,0,0,0); border: none; border-radius: 0px; ')


class ItemTreeShotAssetSelect(QDialog):
	def __init__(self, parent = None, data={}, entity=''):
		super(self.__class__, self).__init__(parent)
		'''
		|_data
			|_name		ex. 'zeafrost_101_S01_0010'
			|_cutin		ex. 1001
			|_cutout	ex. 1010
			|_status	ex. wtg
		'''
		self.data = data
		self.entity = entity

		self.main_layout = QVBoxLayout()
		self.main_layout.setContentsMargins(5,0,0,0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)
		self.setFixedSize(280,70)
		self.setStyleSheet('''
			QDialog{background: rgba(0,0,0,0); border: none; border-radius: 0px; color: rgb(190, 190, 190)}
			QLabel{color: rgb(100,100,100)}
		''')

		splitter = QSplitter()
		splitter.setStyleSheet('''
		QSplitter:handle{background:rgb(70,70,70); border: none;
			margin-top:25px; margin-bottom:25px; width: 10px}''')
		self.main_layout.addWidget(splitter)
		
		if self.entity == 'shot':
			thumbnail_path = self.getThumbnailShot()

		elif self.entity == 'asset':
			thumbnail_path = self.getThumbnailAsset()

		if thumbnail_path:
			icon = QIcon(thumbnail_path)
			pixmap = icon.pixmap(95,60, QIcon.Active, QIcon.On)
		else:
			icon = QIcon('{}/icons/shot.png'.format(MODULE_PATH))
			pixmap = icon.pixmap(30,30, QIcon.Active, QIcon.On)

		inst_icon = QLabel()
		inst_icon.setAlignment(Qt.AlignCenter)
		inst_icon.setStyleSheet('border: none; border-radius: 6; background: rgb(5,5,5)')
		inst_icon.setFixedSize(90, 60)
		inst_icon.setPixmap(pixmap)
		splitter.addWidget(inst_icon)

		detail_layout = QVBoxLayout()
		detail_layout.setContentsMargins(10, 5, 10, 0)
		detail_layout.setAlignment(Qt.AlignTop)
		detail_widget = QDialog()
		detail_widget.setLayout(detail_layout)
		splitter.addWidget(detail_widget)

		name_label = QLabel(self.data['name'])
		name_label.setStyleSheet('font-size: 11px; color: rgb(190,190,190); font-weight: bold;')
		detail_layout.addWidget(name_label)

		frame_layout = QHBoxLayout()
		frame_layout.setAlignment(Qt.AlignLeft)
		frame_layout.setContentsMargins(0,0,0,0)
		detail_layout.addLayout(frame_layout)

		if self.entity == 'shot':
			cutin_head = QLabel('Cut In : ')
			cutin_head.setFixedWidth(40)
			frame_layout.addWidget(cutin_head)
			cutin_label = QLabel(str(self.data['cutin']))
			cutin_label.setFixedWidth(28)
			frame_layout.addWidget(cutin_label)

			cutout_head = QLabel('Cut Out : ')
			cutout_head.setFixedWidth(50)
			frame_layout.addWidget(cutout_head)
			cutout_label = QLabel(str(self.data['cutout']))
			# cutout_label.setFixedWidth(40)
			frame_layout.addWidget(cutout_label)

		status_layout = QHBoxLayout()
		status_layout.setAlignment(Qt.AlignLeft)
		status_layout.setContentsMargins(0,0,0,0)
		detail_layout.addLayout(status_layout)

		status_head = QLabel('Status : ')
		status_head.setFixedWidth(40)
		status_layout.addWidget(status_head)
		status_label = QLabel(str(self.data['status']))
		status_layout.addWidget(status_label)

	def getThumbnailShot(self):
		
		thumbnail_path = ''
		pattern_check = '{root}/review/shot/{episode}/{sequence}/{shot}'
		
		proj_data = func.getProjectData()
		if proj_data:
			root_path = proj_data[0]['project_path']

			path_check = pattern_check.format(
				root = root_path,
				episode = self.data['episode'],
				sequence = self.data['sequence'],
				shot = self.data['shot'])

			if os.path.exists(path_check):
				files = os.listdir(path_check)
				paths = [os.path.join(path_check, basename) for basename in files]
				lastest_step = max(paths, key=os.path.getmtime)

				image_path = '{}/image'.format(lastest_step.replace('\\', '/'))
				if os.path.exists(image_path):
					files = os.listdir(image_path)
					paths = [os.path.join(image_path, basename) for basename in files]
					lastest_media = max(paths, key=os.path.getmtime)

					thumbnail_folder = '{}/thumbnail'.format(lastest_media.replace('\\', '/'))
					if os.path.exists(thumbnail_folder):
						media_files = os.listdir(thumbnail_folder)

						if media_files:
							thumbnail_path = '{}/{}'.format(thumbnail_folder, media_files[0])

		# print(thumbnail_path)
		return thumbnail_path

	def getThumbnailAsset(self):
		
		thumbnail_path = ''
		pattern_check = '{root}/publish/asset/{asset_type}/{asset}/thumbnail'

		proj_data = func.getProjectData()
		if proj_data:
			root_path = proj_data[0]['project_config']['directory']['publish']['asset']
			pattern_check = proj_data[0]['project_config']['pattern']['step']['rig']['production_area']['publish']['media']['thumbnail']['directory']
			
			thumbnail_folder = pattern_check.format(root = root_path, asset_type = self.data['asset_type'], asset = self.data['asset'])
			if os.path.exists(thumbnail_folder):
				media_files = [os.path.join(thumbnail_folder, basename) for basename in os.listdir(thumbnail_folder)]

				if media_files:
					thumbnail_path = max(media_files, key=os.path.getmtime)

		return thumbnail_path


class ItemTreeFileSelect(QDialog):
	def __init__(self, parent = None, data={}, item='', files=False, folder=False, mainWidget=''):
		super(self.__class__, self).__init__(parent)
		'''
		|_data
			|_name			ex. 'zeafrost_101_S01_0010_lay_master_v001.ma'
			|_date			ex. '2023/10/14 10:25'
			|_size			ex. '10.10 MB''
			|_owner			ex. 'thaksaporn'
			|_permssion		ex. 'W/R'
			|_comment		ex. 'test publish'
			|_thumbnail		ex. '"T:/rnd/zeafrost/work/shot/101/S01/0020/lay/.yggpipdata/thumbnail/zeafrost_101_S01_0020_lay_master_v001/20231123_1133.1001.jpg"'
		'''

		self.pressPose = None

		self.data = data
		self.parent = parent
		self.item = item
		self.folder = folder
		self.mainWidget = mainWidget

		self.main_layout = QVBoxLayout()
		self.main_layout.setContentsMargins(5,0,0,0)
		self.main_layout.setSpacing(0)

		self.setLayout(self.main_layout)
		self.resize(500,80)
		self.setStyleSheet('''
			QDialog{background: rgba(0,0,0,0); border: none; border-radius: 0px; color: rgb(190, 190, 190)}
			QLabel{color: rgb(100,100,100)}''')

		splitter = QSplitter()
		splitter.setStyleSheet('''
		QSplitter:handle{background:rgb(70,70,70); border: none;
			margin-top:25px; margin-bottom:25px; width: 10px}''')
		self.main_layout.addWidget(splitter)

		if files:
			# pprint(self.data)
			if self.data.get('thumbnail'):
				if os.path.exists(self.data['thumbnail']):
					icon = QIcon(self.data['thumbnail'])
					pixmap = icon.pixmap(125,70, QIcon.Active, QIcon.On)
				else:
					if self.data['name'].endswith('.ma'):
						icon = QIcon('{}/icons/ma_file.png'.format(MODULE_PATH))
					elif self.data['name'].endswith('.mb'):
						icon = QIcon('{}/icons/mb_file.png'.format(MODULE_PATH))
					elif self.data['name'].endswith('.hip') or self.data['name'].endswith('.hiplc') or self.data['name'].endswith('.hipnc'):
						icon = QIcon('{}/icons/houdini.png'.format(MODULE_PATH))
					else:
						icon = QIcon('{}/icons/files.png'.format(MODULE_PATH))
					pixmap = icon.pixmap(35,35, QIcon.Active, QIcon.On)
			else:
				if self.data['name'].endswith('.ma'):
					icon = QIcon('{}/icons/ma_file.png'.format(MODULE_PATH))
				elif self.data['name'].endswith('.mb'):
					icon = QIcon('{}/icons/mb_file.png'.format(MODULE_PATH))
				elif self.data['name'].endswith('.hip') or self.data['name'].endswith('.hiplc') or self.data['name'].endswith('.hipnc'):
					icon = QIcon('{}/icons/houdini.png'.format(MODULE_PATH))
				else:
					icon = QIcon('{}/icons/files.png'.format(MODULE_PATH))
				pixmap = icon.pixmap(35,35, QIcon.Active, QIcon.On)
		else:
			icon = QIcon('{}/icons/folder.png'.format(MODULE_PATH))
			pixmap = icon.pixmap(40,40, QIcon.Active, QIcon.On)

		inst_icon = QLabel()
		inst_icon.setAlignment(Qt.AlignCenter)
		inst_icon.setStyleSheet('border: none; border-radius: 6; background: rgb(5,5,5)')
		inst_icon.setFixedSize(125, 70)

		if func.DCC == 'houdini':
			inst_icon.setStyleSheet('border: none; border-radius: 6; background: rgb(5,5,5); margin-top: 5px')
			inst_icon.setFixedSize(125, 75)
		
		inst_icon.setPixmap(pixmap)
		splitter.addWidget(inst_icon)

		detail_layout = QVBoxLayout()
		detail_layout.setContentsMargins(20, 2, 0, 2)
		detail_layout.setAlignment(Qt.AlignTop)
		detail_widget = QDialog()
		detail_widget.setLayout(detail_layout)
		splitter.addWidget(detail_widget)

		name_label = QLabel(self.data['name'])
		name_label.setStyleSheet('font-size: 11px; color: rgb(190,190,190); font-weight: bold;')
		detail_layout.addWidget(name_label)

		date_layout = QHBoxLayout()
		date_layout.setContentsMargins(0,0,0,0)
		detail_layout.addLayout(date_layout)

		date_head = QLabel('Date Modifild : ')
		date_head.setFixedWidth(70)
		date_layout.addWidget(date_head)
		date_label = QLabel(self.data['date'])
		date_label.setFixedWidth(100)
		date_layout.addWidget(date_label)

		size_head = QLabel('Size : ')
		size_head.setFixedWidth(25)
		date_layout.addWidget(size_head)
		size_label = QLabel(self.data['size'])
		date_layout.addWidget(size_label)

		owner_layout = QHBoxLayout()
		owner_layout.setContentsMargins(0,0,0,0)
		detail_layout.addLayout(owner_layout)

		owner_head = QLabel('Owner : ')
		owner_head.setFixedWidth(40)
		owner_layout.addWidget(owner_head)
		owner_label = QLabel(self.data['owner'])
		owner_label.setFixedWidth(70)
		owner_layout.addWidget(owner_label)

		permission_head = QLabel('Permission : ')
		permission_head.setFixedWidth(60)
		owner_layout.addWidget(permission_head)
		permission_label = QLabel(self.data['permission'])
		owner_layout.addWidget(permission_label)

		if files:
			comment_layout = QHBoxLayout()
			comment_layout.setContentsMargins(0,0,0,0)
			detail_layout.addLayout(comment_layout)

			comment_head = QLabel('Comment : ')
			comment_head.setFixedWidth(55)
			comment_layout.addWidget(comment_head)
			comment_label = QLabel(self.data['comment'])
			comment_layout.addWidget(comment_label)

		else:
			type_layout = QHBoxLayout()
			type_layout.setContentsMargins(0,0,0,0)
			detail_layout.addLayout(type_layout)
			
			type_head = QLabel('Type : ')
			type_head.setFixedWidth(35)
			type_layout.addWidget(type_head)
			type_label = QLabel('File folder')
			type_layout.addWidget(type_label)

	def mousePressEvent(self, event):

		self.parent.clearSelection()
		self.parent.setCurrentItem(self.item)

		if event.button() == Qt.RightButton:
			
			fileMenu = QMenu()
			fileMenu.setStyleSheet('''
					QMenu{background: rgb(40,40,40,190);}
					QMenuBar{background: rgb(70,70,70,190);}
					QMenuBar::hover, QMenuBar::item:selected, QMenu::item:selected{background: #3b87d3; color: rgb(235,235,235)}''')
			fileMenu.addAction('Open Location File', self.openLocationFile)

			pos = event.pos()
			fileMenu.exec_(self.mapToGlobal(pos))
		
		elif event.button() == Qt.LeftButton:
			self.pressPose = event.pos()

	def mouseReleaseEvent(self, event):

		if ( not self.pressPose == None and 
			event.button() == Qt.LeftButton):

			self.mainWidget.selectFileItem()

		self.pressPose = None


	def mouseDoubleClickEvent(self, event):

		if event.button() == Qt.LeftButton:
			self.mainWidget.callOpenConfirmDialog()


	def openLocationFile(self):

		if self.folder:
			open_path = self.data['full_path']
		else:
			open_path = os.path.dirname(self.data['full_path'])

		if os.path.exists(open_path):
			os.startfile(open_path)


class SearchBoxWidget(QDialog):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

		self.main_layout = QHBoxLayout()
		self.main_layout.setContentsMargins(0,0,0,0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		self.resize(200,25)

		self.line = QLineEdit()
		self.line.setStyleSheet('background: rgba(0,0,0,0); border: none; color: rgb(190, 190, 190)')
		self.line.setFixedHeight(25)
		self.main_layout.addWidget(self.line)

		self.search_btn = QPushButton()
		# self.search_btn.installEventFilter(self)
		# self.search_btn.setIcon(QIcon('{}/icons/search.png'.format(MODULE_PATH)))
		self.search_btn.setStyleSheet('''
		QPushButton{border: none; margin: 3px;
			image: url(''' + MODULE_PATH +'''/icons/search.png); background: rgba(0,0,0,0)}
		QPushButton:hover{image: url(''' + MODULE_PATH +'''/icons/search_hover.png)}
		''')
		self.search_btn.setFixedSize(20,20)
		self.main_layout.addWidget(self.search_btn)

		self.setStyleSheet('QDialog{background: rgb(40, 40, 40); border-bottom: 2px solid rgb(100, 100, 100)}')


class ConfirmDialog(QDialog):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.setFixedSize(300,160)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.setLayout(self.mainLayout)
		dialog.setStyleSheet('''
			QDialog{background-color: rgb(30, 30, 30); border: 2px solid rgb(10,10,10); border-radius: 5px;} 
			QLabel{color: rgb(190,190,190)}
			QPushButton{background: rgb(10, 10, 10); border: none;border-radius: 3px;color:rgb(190, 190, 190); height: 25px}
			QPushButton:hover{background: rgb(50, 50, 50);color: rgb(150, 150, 150)}''')

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)

		self.setWindowTitle('Open File')
		self.setLayout(panel)

		self.initTitleWidget()
		self.initBodyWidget()

	def mousePressEvent(self,event):
		self.moving = True
		self.offset = event.pos()

	def mouseMoveEvent(self,event):
		if self.moving:
			self.move(event.globalPos()-self.offset)

	def showEvent(self,event):
		self.repaint()

	def initTitleWidget(self):
		
		title_layout = QHBoxLayout()
		self.mainLayout.addLayout(title_layout)

		title_label = QLabel('Open File')
		title_label.setFixedWidth(250)
		title_label.setStyleSheet('color: rgb(190, 190, 190); font-size: 14px; margin-left: 10px')
		title_layout.addWidget(title_label)

		self.manage_closeBtn = QPushButton('X')
		self.manage_closeBtn.setFixedSize(25,25)
		self.manage_closeBtn.setStyleSheet('''
			QPushButton{font:bold Segoe UI; color:rgb(200,200,200); background:rgba(0,0,0,0); border:none; border-radius:4px;}
			QPushButton:hover:!pressed{background:rgba(20,20,20,100);color: red}
			QPushButotn:pressed{background:rgba(20,20,20,10)}''')
		title_layout.addWidget(self.manage_closeBtn)
		self.manage_closeBtn.clicked.connect(self.close)

	def initBodyWidget(self):

		body_layout = QHBoxLayout()
		body_layout.setSpacing(15)
		body_layout.setContentsMargins(15,0,10,10)
		self.mainLayout.addLayout(body_layout)

		warning_label = QLabel('Do you want to Open ?')

		icon = QIcon('{}/icons/information.png'.format(MODULE_PATH))
		pixmap = icon.pixmap(60,60, QIcon.Active, QIcon.On)
		inst_icon = QLabel()
		inst_icon.setFixedWidth(60)
		inst_icon.setPixmap(pixmap)

		body_layout.addWidget(inst_icon)
		body_layout.addWidget(warning_label)

		btn_layout = QHBoxLayout()
		btn_layout.setContentsMargins(15,0,15,0)
		self.mainLayout.addLayout(btn_layout)

		self.yes_btn = QPushButton('Yes')
		btn_layout.addWidget(self.yes_btn)

		self.no_btn = QPushButton('No')
		self.no_btn.clicked.connect(self.close)
		btn_layout.addWidget(self.no_btn)


class SortFileDialog(QDialog):
	def __init__(self, parent = None, position='', entity=''):
		super(self.__class__, self).__init__(parent)

		self.parent = parent
		self.entity = entity
		
		pPosX = position.x()
		pPosY = position.y()

		cPosX = pPosX - 458
		cPosY = pPosY + 27

		self.setGeometry(cPosX,cPosY,100,120)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.resize(100, 120)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setSpacing(0)
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.focusOutEvent = self.close_Window
		dialog.setLayout(self.mainLayout)
		dialog.setStyleSheet('''
			QDialog{background-color: rgb(33, 33, 33); border: 2px solid rgb(40,40,40); border-radius: 5px;} 
			QLabel{color: rgb(190,190,190)}
			QPushButton{background: rgb(10, 10, 10); border: none;border-radius: 3px;color:rgb(190, 190, 190); height: 25px}
			QPushButton:hover{background: rgb(50, 50, 50);color: rgb(150, 150, 150)}''')

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)
		self.setLayout(panel)

		manage_layout = QHBoxLayout()
		manage_layout.setContentsMargins(0,0,0,0)
		manage_layout.setAlignment(Qt.AlignRight)
		self.mainLayout.addLayout(manage_layout)

		title_label = QLabel('Sort by')
		title_label.setFixedWidth(80)
		manage_layout.addWidget(title_label)

		self.w_closeBtn = QPushButton('X')
		manage_layout.addWidget(self.w_closeBtn)
		self.w_closeBtn.setFixedSize(12,12)
		self.w_closeBtn.setFocusPolicy(Qt.NoFocus)
		self.w_closeBtn.setStyleSheet('''
			QPushButton{font:bold Segoe UI; color:rgb(200,200,200); font-size: 8px; background:rgba(0,0,0,0); border:none; border-radius:4px;}
			QPushButton:hover:!pressed{background:rgba(20,20,20,100);color: red}
			QPushButotn:pressed{background:rgba(20,20,20,10)}''')
		self.w_closeBtn.clicked.connect(self.close)

		self.sortTypeList = QListWidget()
		self.sortTypeList.setIconSize(QSize(13,13))
		self.sortTypeList.setStyleSheet("""
			QListView{outline:none; border:none; background:rgba(0,0,200,0); font:bold;}
			QListWidget{padding:5px 5px 5px 5px;}

			QListWidget:item{height:23px; color:rgb(150,150,150); background:rgba(0,0,0,0); padding-left:5px;}
			QListWidget:item:hover:!pressed{background:rgba(0,0,0,0); color: rgb(230,230,230)}
			QListWidget:item:selected{background:rgba(0,0,0,0);}
			QListView:icon{margin-right:3px;}

			QListView:indicator{height:13px; width:13px; border:none; margin-right:3px;}
			QListView:indicator:checked{image:url("""+MODULE_PATH+"""/icons/checkbox/check.png);}
			QListView:indicator:checked:!enabled{image:url("""+MODULE_PATH+"""/icons/checkbox/uncheck.png);}
			QListView:indicator:unchecked{image:url("""+MODULE_PATH+"""/icons/checkbox/uncheck.png);}
			QListView:indicator:unchecked:!enabled{image:url("""+MODULE_PATH+"""/icons/checkbox/uncheck.png);}""")

		self.sortTypeList.focusOutEvent = self.close_Window
		self.sortTypeList.addItems(['name', 'date modifild', 'owner'])
		self.sortTypeList.itemPressed.connect(self.doSortFileItem)
		self.mainLayout.addWidget(self.sortTypeList)

	def close_Window(self,event):

		self.close()

	def doSortFileItem(self):

		item = self.sortTypeList.currentItem()
		sorter = item.text()

		folders = []
		new_folders = []
		files = []
		new_files = []

		for item in self.parent.dataFile_item.keys():

			data = self.parent.dataFile_item[item]

			if os.path.isfile(data['name']):
				files.append(data)
			else:
				folders.append(data)


		if sorter == 'name':
			
			if files:
				new_files = sorted(files, key=lambda x: x['name'])

			if folders:
				new_folders = sorted(folders, key=lambda x: x['name'])
		
		elif sorter == 'date modifild':

			if files:
				new_files = sorted(files, key=lambda x: x['date'])
				new_files.reverse()

			if folders:
				new_folders = sorted(folders, key=lambda x: x['date'])
				new_folders.reverse()

		elif sorter == 'owner':

			if files:
				new_files = sorted(files, key=lambda x: x['owner'])

			if folders:
				new_folders = sorted(folders, key=lambda x: x['owner'])

		
		new_data = new_folders + new_files

		if self.parent.work_checkbox.isChecked():
			area = 'work'
		elif self.parent.publish_checkbox.isChecked():
			area = 'publish'
		else:
			area = 'work'

		self.parent.file_tree.clear()
		self.parent.dataFile_item = {}

		# pprint(new_data)

		QApplication.setOverrideCursor(Qt.WaitCursor)

		for data in new_data:
			f = data['name']
			ep = data.get('episode') or ''
			seq = data.get('sequence') or ''
			shot = data.get('shot') or ''
			asset = data.get('asset') or ''
			asset_type = data.get('asset_type') or ''
			step = data.get('step') or ''

			data, typ = func.getDataFile(
					path=f,
					ep=ep, 
					seq=seq, 
					shot=shot, 
					asset=asset, 
					asset_type=asset_type, 
					step=step)

			# pprint(data)

			item = QTreeWidgetItem(self.parent.file_tree)

			if self.parent.itemFile_view == 'grid':

				self.parent.file_tree.setHeaderHidden(True)
				self.parent.file_tree.setHeaderLabels([''])

				if typ == 'folder':
					widget = ItemTreeFileSelect(parent = self.parent.file_tree, data=data, folder=True)
				else:
					widget = ItemTreeFileSelect(parent = self.parent.file_tree, data=data, files=True)

				size = widget.size()
				item.setSizeHint(0, size)
				self.parent.file_tree.setItemWidget(item, 0, widget)
			else:
				item.setText(0, data['name'])
				item.setText(1, data['date'])
				item.setText(2, data['owner'])

				self.parent.file_tree.setColumnWidth(0, 330)
				self.parent.file_tree.setColumnWidth(1, 95)
				self.parent.file_tree.setColumnWidth(2, 70)

				if typ == 'folder':
					item.setIcon(0, QIcon('{}/icons/folder.png'.format(MODULE_PATH)))
				else:
					item.setIcon(0, QIcon('{}/icons/files.png'.format(MODULE_PATH)))


			if self.entity == 'shot':
				self.parent.dataFile_item[str(item)] = {
					'name': data['full_path'], 
					'type': 'file', 
					'item': item, 
					'episode': ep,
					'sequence': seq,
					'shot': shot,
					'step': step,
					'area': area,
					'date': data['date'],
					'owner': data['owner']}
			else:
				self.parent.dataFile_item[str(item)] = {
					'name': data['full_path'], 
					'type': 'file', 
					'item': item, 
					'asset': asset,
					'asset_type': asset_type,
					'step': step,
					'area': area,
					'date': data['date'],
					'owner': data['owner']}

		QApplication.restoreOverrideCursor()
		self.close()

		
class WarningReplaceDialog(QDialog):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.setFixedSize(300,160)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.setLayout(self.mainLayout)
		dialog.setStyleSheet('''
			QDialog{background-color: rgb(30, 30, 30); border: 2px solid rgb(10,10,10); border-radius: 5px;} 
			QLabel{color: rgb(190,190,190)}
			QPushButton{background: rgb(10, 10, 10); border: none;border-radius: 3px;color:rgb(190, 190, 190); height: 25px}
			QPushButton:hover{background: rgb(50, 50, 50);color: rgb(150, 150, 150)}''')

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)

		self.setWindowTitle('Save File')
		self.setLayout(panel)

		self.initTitleWidget()
		self.initBodyWidget()

	def mousePressEvent(self,event):
		self.moving = True
		self.offset = event.pos()

	def mouseMoveEvent(self,event):
		if self.moving:
			self.move(event.globalPos()-self.offset)

	def showEvent(self,event):
		self.repaint()

	def initTitleWidget(self):
		
		title_layout = QHBoxLayout()
		self.mainLayout.addLayout(title_layout)

		title_label = QLabel('Save File')
		title_label.setFixedWidth(250)
		title_label.setStyleSheet('color: rgb(190, 190, 190); font-size: 14px; margin-left: 10px')
		title_layout.addWidget(title_label)

		self.manage_closeBtn = QPushButton('X')
		self.manage_closeBtn.setFixedSize(25,25)
		self.manage_closeBtn.setStyleSheet('''
			QPushButton{font:bold Segoe UI; color:rgb(200,200,200); background:rgba(0,0,0,0); border:none; border-radius:4px;}
			QPushButton:hover:!pressed{background:rgba(20,20,20,100);color: red}
			QPushButotn:pressed{background:rgba(20,20,20,10)}''')
		title_layout.addWidget(self.manage_closeBtn)
		self.manage_closeBtn.clicked.connect(self.close)

	def initBodyWidget(self):

		body_layout = QHBoxLayout()
		body_layout.setSpacing(15)
		body_layout.setContentsMargins(15,0,10,10)
		self.mainLayout.addLayout(body_layout)

		warning_label = QLabel('Do you want to Replace file ?')

		icon = QIcon('{}/icons/information.png'.format(MODULE_PATH))
		pixmap = icon.pixmap(60,60, QIcon.Active, QIcon.On)
		inst_icon = QLabel()
		inst_icon.setFixedWidth(60)
		inst_icon.setPixmap(pixmap)

		body_layout.addWidget(inst_icon)
		body_layout.addWidget(warning_label)

		btn_layout = QHBoxLayout()
		btn_layout.setContentsMargins(15,0,15,0)
		self.mainLayout.addLayout(btn_layout)

		self.yes_btn = QPushButton('Yes')
		btn_layout.addWidget(self.yes_btn)

		self.no_btn = QPushButton('No')
		self.no_btn.clicked.connect(self.close)
		btn_layout.addWidget(self.no_btn)


class WarningInpuNameFileDialog(QDialog):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.setFixedSize(300,160)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.setLayout(self.mainLayout)
		dialog.setStyleSheet('''
			QDialog{background-color: rgb(30, 30, 30); border: 2px solid rgb(10,10,10); border-radius: 5px;} 
			QLabel{color: rgb(190,190,190)}
			QPushButton{background: rgb(10, 10, 10); border: none;border-radius: 3px;color:rgb(190, 190, 190); height: 25px}
			QPushButton:hover{background: rgb(50, 50, 50);color: rgb(150, 150, 150)}''')

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)

		self.setWindowTitle('Name File')
		self.setLayout(panel)

		self.initTitleWidget()
		self.initBodyWidget()

	def mousePressEvent(self,event):
		self.moving = True
		self.offset = event.pos()

	def mouseMoveEvent(self,event):
		if self.moving:
			self.move(event.globalPos()-self.offset)

	def showEvent(self,event):
		self.repaint()

	def initTitleWidget(self):
		
		title_layout = QHBoxLayout()
		self.mainLayout.addLayout(title_layout)

		title_label = QLabel('Name File')
		title_label.setFixedWidth(250)
		title_label.setStyleSheet('color: rgb(190, 190, 190); font-size: 14px; margin-left: 10px')
		title_layout.addWidget(title_label)

		self.manage_closeBtn = QPushButton('X')
		self.manage_closeBtn.setFixedSize(25,25)
		self.manage_closeBtn.setStyleSheet('''
			QPushButton{font:bold Segoe UI; color:rgb(200,200,200); background:rgba(0,0,0,0); border:none; border-radius:4px;}
			QPushButton:hover:!pressed{background:rgba(20,20,20,100);color: red}
			QPushButotn:pressed{background:rgba(20,20,20,10)}''')
		title_layout.addWidget(self.manage_closeBtn)
		self.manage_closeBtn.clicked.connect(self.close)

	def initBodyWidget(self):

		body_layout = QHBoxLayout()
		body_layout.setSpacing(15)
		body_layout.setContentsMargins(15,0,10,10)
		self.mainLayout.addLayout(body_layout)

		warning_label = QLabel('Please input name file in box or \nselect task before save file')

		icon = QIcon('{}/icons/information.png'.format(MODULE_PATH))
		pixmap = icon.pixmap(60,60, QIcon.Active, QIcon.On)
		inst_icon = QLabel()
		inst_icon.setFixedWidth(60)
		inst_icon.setPixmap(pixmap)

		body_layout.addWidget(inst_icon)
		body_layout.addWidget(warning_label)

		btn_layout = QHBoxLayout()
		btn_layout.setContentsMargins(15,0,15,0)
		self.mainLayout.addLayout(btn_layout)

		self.no_btn = QPushButton('Close')
		self.no_btn.clicked.connect(self.close)
		btn_layout.addWidget(self.no_btn)


class WarningJonInDialog(QDialog):
	def __init__(self, parent = None, data='', entity=''):
		super(self.__class__, self).__init__(parent)

		self.data = data
		self.entity = entity

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.setFixedSize(350,200)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.setLayout(self.mainLayout)
		dialog.setStyleSheet('''
			QDialog{background-color: rgb(30, 30, 30); border: 2px solid rgb(10,10,10); border-radius: 5px;} 
			QLabel{color: rgb(190,190,190)}
			QPushButton{background: rgb(10, 10, 10); border: none;border-radius: 3px;color:rgb(190, 190, 190); height: 25px}
			QPushButton:hover{background: rgb(50, 50, 50);color: rgb(150, 150, 150)}''')

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)

		self.setWindowTitle('Job in')
		self.setLayout(panel)

		self.initTitleWidget()
		self.initBodyWidget()

	def mousePressEvent(self,event):
		self.moving = True
		self.offset = event.pos()

	def mouseMoveEvent(self,event):
		if self.moving:
			self.move(event.globalPos()-self.offset)

	def showEvent(self,event):
		self.repaint()

	def initTitleWidget(self):
		
		title_layout = QHBoxLayout()
		self.mainLayout.addLayout(title_layout)

		title_label = QLabel('Jon In')
		title_label.setFixedWidth(250)
		title_label.setStyleSheet('color: rgb(190, 190, 190); font-size: 14px; margin-left: 10px')
		title_layout.addWidget(title_label)

		self.manage_closeBtn = QPushButton('X')
		self.manage_closeBtn.setFixedSize(25,25)
		self.manage_closeBtn.setStyleSheet('''
			QPushButton{font:bold Segoe UI; color:rgb(200,200,200); background:rgba(0,0,0,0); border:none; border-radius:4px;}
			QPushButton:hover:!pressed{background:rgba(20,20,20,100);color: red}
			QPushButotn:pressed{background:rgba(20,20,20,10)}''')
		title_layout.addWidget(self.manage_closeBtn)
		self.manage_closeBtn.clicked.connect(self.close)

	def initBodyWidget(self):

		body_layout = QHBoxLayout()
		body_layout.setSpacing(15)
		body_layout.setContentsMargins(15,0,10,10)
		self.mainLayout.addLayout(body_layout)

		warning_label = QLabel("Can not Job in from path. \nPlease select Job in.")

		icon = QIcon('{}/icons/information.png'.format(MODULE_PATH))
		pixmap = icon.pixmap(60,60, QIcon.Active, QIcon.On)
		inst_icon = QLabel()
		inst_icon.setFixedWidth(60)
		inst_icon.setPixmap(pixmap)

		body_layout.addWidget(inst_icon)
		body_layout.addWidget(warning_label)

		jobIn_head_layout = QHBoxLayout()
		jobIn_head_layout.setContentsMargins(15,0,10,0)
		self.mainLayout.addLayout(jobIn_head_layout)

		jobIn_combobox_layout = QHBoxLayout()
		jobIn_combobox_layout.setContentsMargins(15,0,10,10)
		self.mainLayout.addLayout(jobIn_combobox_layout)

		if self.entity == 'shot':
			ep_label = QLabel('episode : ')
			ep_label.setFixedWidth(105)
			seq_label = QLabel('sequence : ')
			seq_label.setFixedWidth(100)
			shot_label = QLabel('shot : ')

			jobIn_head_layout.addWidget(ep_label)
			jobIn_head_layout.addWidget(seq_label)
			jobIn_head_layout.addWidget(shot_label)

			self.ep_combobox = QComboBox()
			self.ep_combobox.setFixedHeight(25)
			self.ep_combobox.setEditable(True)
			self.seq_combobox = QComboBox()
			self.seq_combobox.setFixedHeight(25)
			self.seq_combobox.setEditable(True)
			self.shot_combobox = QComboBox()
			self.shot_combobox.setFixedHeight(25)
			self.shot_combobox.setEditable(True)


			self.ep_combobox.currentIndexChanged.connect(self.showSequence)
			self.seq_combobox.currentIndexChanged.connect(self.showShot)

			jobIn_combobox_layout.addWidget(self.ep_combobox)
			jobIn_combobox_layout.addWidget(self.seq_combobox)
			jobIn_combobox_layout.addWidget(self.shot_combobox)

			ep_list = list(self.data.keys())
			ep_list.sort()
			self.ep_combobox.addItems(ep_list)

		else:
			type_label = QLabel('type : ')
			type_label.setFixedWidth(105)
			asset_label = QLabel('asset : ')

			jobIn_head_layout.addWidget(type_label)
			jobIn_head_layout.addWidget(asset_label)

			self.type_combobox = QComboBox()

			self.type_combobox.setFixedSize(100, 25)
			self.type_combobox.setEditable(True)
			self.asset_combobox = QComboBox()
			self.asset_combobox.setFixedHeight(25)
			self.asset_combobox.setEditable(True)

			self.type_combobox.currentIndexChanged.connect(self.showAsset)

			jobIn_combobox_layout.addWidget(self.type_combobox)
			jobIn_combobox_layout.addWidget(self.asset_combobox)

			type_list = list(self.data.keys())
			type_list.sort()
			self.type_combobox.addItems(type_list)

		btn_layout = QHBoxLayout()
		btn_layout.setContentsMargins(15,0,15,0)
		self.mainLayout.addLayout(btn_layout)

		self.yes_btn = QPushButton('Job In')
		btn_layout.addWidget(self.yes_btn)

		# self.no_btn = QPushButton('Close')
		# self.no_btn.clicked.connect(self.close)
		# btn_layout.addWidget(self.no_btn)

	def showSequence(self):

		self.seq_combobox.clear()

		ep = self.ep_combobox.currentText()
		if ep:
			seq_list = list(self.data[ep].keys())
			seq_list.sort()	

			self.seq_combobox.addItems(seq_list)	
		
	def showShot(self):
		
		self.shot_combobox.clear()

		ep = self.ep_combobox.currentText()
		seq = self.seq_combobox.currentText()

		shot_list = []

		if ep and seq:
			for shot in self.data[ep][seq].keys():
				name = self.data[ep][seq][shot]['short_name']
				if name:
					shot_list.append(name)

			shot_list.sort()
			self.shot_combobox.addItems(shot_list)

	def showAsset(self):
		
		self.asset_combobox.clear()

		asset_type = self.type_combobox.currentText()
		asset_list = []

		if asset_type:
			asset_list  = self.data[asset_type].keys()
			asset_list.sort()

			self.asset_combobox.addItems(asset_list)


class WarningNotExistsPathDialog(QDialog):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.setFixedSize(300,160)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.setLayout(self.mainLayout)
		dialog.setStyleSheet('''
			QDialog{background-color: rgb(30, 30, 30); border: 2px solid rgb(10,10,10); border-radius: 5px;} 
			QLabel{color: rgb(190,190,190)}
			QPushButton{background: rgb(10, 10, 10); border: none;border-radius: 3px;color:rgb(190, 190, 190); height: 25px}
			QPushButton:hover{background: rgb(50, 50, 50);color: rgb(150, 150, 150)}''')

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)

		self.setWindowTitle('Path Input')
		self.setLayout(panel)

		self.initTitleWidget()
		self.initBodyWidget()

	def mousePressEvent(self,event):
		self.moving = True
		self.offset = event.pos()

	def mouseMoveEvent(self,event):
		if self.moving:
			self.move(event.globalPos()-self.offset)

	def showEvent(self,event):
		self.repaint()

	def initTitleWidget(self):
		
		title_layout = QHBoxLayout()
		self.mainLayout.addLayout(title_layout)

		title_label = QLabel('Path Input')
		title_label.setFixedWidth(250)
		title_label.setStyleSheet('color: rgb(190, 190, 190); font-size: 14px; margin-left: 10px')
		title_layout.addWidget(title_label)

		self.manage_closeBtn = QPushButton('X')
		self.manage_closeBtn.setFixedSize(25,25)
		self.manage_closeBtn.setStyleSheet('''
			QPushButton{font:bold Segoe UI; color:rgb(200,200,200); background:rgba(0,0,0,0); border:none; border-radius:4px;}
			QPushButton:hover:!pressed{background:rgba(20,20,20,100);color: red}
			QPushButotn:pressed{background:rgba(20,20,20,10)}''')
		title_layout.addWidget(self.manage_closeBtn)
		self.manage_closeBtn.clicked.connect(self.close)

	def initBodyWidget(self):

		body_layout = QHBoxLayout()
		body_layout.setSpacing(15)
		body_layout.setContentsMargins(15,0,10,10)
		self.mainLayout.addLayout(body_layout)

		warning_label = QLabel('Path not exists. \nPlease check path again.')

		icon = QIcon('{}/icons/information.png'.format(MODULE_PATH))
		pixmap = icon.pixmap(60,60, QIcon.Active, QIcon.On)
		inst_icon = QLabel()
		inst_icon.setFixedWidth(60)
		inst_icon.setPixmap(pixmap)

		body_layout.addWidget(inst_icon)
		body_layout.addWidget(warning_label)

		btn_layout = QHBoxLayout()
		btn_layout.setContentsMargins(15,0,15,0)
		self.mainLayout.addLayout(btn_layout)

		# self.yes_btn = QPushButton('Yes')
		# btn_layout.addWidget(self.yes_btn)

		self.no_btn = QPushButton('Close')
		self.no_btn.clicked.connect(self.close)
		btn_layout.addWidget(self.no_btn)


class WarningCheckSaveCurrentFileDialog(QDialog):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.setFixedSize(300,160)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(Qt.AlignTop)

		dialog = QDialog()
		dialog.setLayout(self.mainLayout)
		dialog.setStyleSheet('''
			QDialog{background-color: rgb(30, 30, 30); border: 2px solid rgb(10,10,10); border-radius: 5px;} 
			QLabel{color: rgb(190,190,190)}
			QPushButton{background: rgb(10, 10, 10); border: none;border-radius: 3px;color:rgb(190, 190, 190); height: 25px}
			QPushButton:hover{background: rgb(50, 50, 50);color: rgb(150, 150, 150)}''')

		panel = QVBoxLayout()
		panel.setContentsMargins(0,0,0,0)
		panel.addWidget(dialog)

		self.setWindowTitle('Path Input')
		self.setLayout(panel)

		self.initTitleWidget()
		self.initBodyWidget()

	def mousePressEvent(self,event):
		self.moving = True
		self.offset = event.pos()

	def mouseMoveEvent(self,event):
		if self.moving:
			self.move(event.globalPos()-self.offset)

	def showEvent(self,event):
		self.repaint()

	def initTitleWidget(self):
		
		title_layout = QHBoxLayout()
		self.mainLayout.addLayout(title_layout)

		title_label = QLabel('Save File')
		title_label.setFixedWidth(250)
		title_label.setStyleSheet('color: rgb(190, 190, 190); font-size: 14px; margin-left: 10px')
		title_layout.addWidget(title_label)

		self.manage_closeBtn = QPushButton('X')
		self.manage_closeBtn.setFixedSize(25,25)
		self.manage_closeBtn.setStyleSheet('''
			QPushButton{font:bold Segoe UI; color:rgb(200,200,200); background:rgba(0,0,0,0); border:none; border-radius:4px;}
			QPushButton:hover:!pressed{background:rgba(20,20,20,100);color: red}
			QPushButotn:pressed{background:rgba(20,20,20,10)}''')
		title_layout.addWidget(self.manage_closeBtn)
		self.manage_closeBtn.clicked.connect(self.close)

	def initBodyWidget(self):

		body_layout = QHBoxLayout()
		body_layout.setSpacing(15)
		body_layout.setContentsMargins(15,0,10,10)
		self.mainLayout.addLayout(body_layout)

		warning_label = QLabel('Are you save current file.')

		icon = QIcon('{}/icons/information.png'.format(MODULE_PATH))
		pixmap = icon.pixmap(60,60, QIcon.Active, QIcon.On)
		inst_icon = QLabel()
		inst_icon.setFixedWidth(60)
		inst_icon.setPixmap(pixmap)

		body_layout.addWidget(inst_icon)
		body_layout.addWidget(warning_label)

		btn_layout = QHBoxLayout()
		btn_layout.setContentsMargins(15,0,15,0)
		self.mainLayout.addLayout(btn_layout)

		self.yes_btn = QPushButton('Yes')
		btn_layout.addWidget(self.yes_btn)

		self.no_btn = QPushButton('No')
		btn_layout.addWidget(self.no_btn)









def main():
	# Create App Single
	#------------------
	app = QApplication(sys.argv)

	# // edit icon taskbar // #
	AppUserModelID = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
	ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(AppUserModelID)

	# Create Window
	#--------------
	# window = ItemTreeFileSelect(
	# 		data={
	# 		'name':'zeafrost_101_S01_0010_lay_master_v001.ma',
	# 		'date':'2023/10/14 10:25',
	# 		'size':'10.10 MB',
	# 		'owner':'thaksaporn',
	# 		'permission':'W/R',
	# 		'comment':'test publish'},
	# 	folder=True)

	window = ItemTreeShotAssetSelect(
			data={
			'name': 'PipelineAreaA',
			'asset_type': 'set',
			'asset': 'PipelineAreaA',
			'status': 'wip'})

	# window = SortFileDialog()
	
	window.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
		