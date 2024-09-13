
# -*- coding: utf-8 -*-

import os
import sys
import ctypes
import platform
from pprint import pprint


from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

MODULE_PATH = os.path.dirname(__file__).replace('\\','/')

import libs.src.saveAndOpen_func as func
reload(func)


class ItemTreeProject(QDialog):
	def __init__(self, parent = None, text=''):
		super(self.__class__, self).__init__(parent)

		self.project = text

		self.main_layout = QHBoxLayout()
		self.main_layout.setContentsMargins(5,0,0,0)
		self.main_layout.setSpacing(0)
		self.setLayout(self.main_layout)

		icon = QIcon('{}/icons/folder.png'.format(MODULE_PATH))

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

class DccItemWidget(QListWidgetItem):
	def __init__(self, *args, **kwargs):
		super(DccItemWidget, self).__init__(*args, **kwargs)

		self.set_thumbnail()

	def set_thumbnail(self, dcc=''):

		path_thumb = '{MODULE_PATH}/icons/dcc'.format(MODULE_PATH=MODULE_PATH)

		if dcc == 'maya':
			pixmap = QPixmap('{path_thumb}/maya_default_a.png'.format(path_thumb=path_thumb))
			pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio)

		elif dcc == 'houdini':
			pixmap = QPixmap('{path_thumb}/houdini_default_a.png'.format(path_thumb=path_thumb))
			pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio)

		elif dcc == 'blender':
			pixmap = QPixmap('{path_thumb}/blender.png'.format(path_thumb=path_thumb))
			pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio)

		else:
			pixmap = QPixmap('{path_thumb}/tool.png'.format(path_thumb=path_thumb))
			pixmap = pixmap.scaled(40, 40)

		self.setIcon(QIcon(pixmap))
		self.setSizeHint(QSize(65, 60))

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


class ProjectAddDialog(QDialog):
	def __init__(self, parent = None):
		super(self.__class__, self).__init__(parent)

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.setFixedSize(300,160)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setSpacing(10)
		self.mainLayout.setContentsMargins(20,10,20,10)
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

		self.setWindowTitle('Add Project')
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

		title_label = QLabel('Add Project')
		title_label.setStyleSheet('color: rgb(190, 190, 190); font-size: 14px;')
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

		name_layout = QHBoxLayout()
		self.mainLayout.addLayout(name_layout)

		name_label = QLabel('name: ')
		name_label.setFixedWidth(35)
		name_layout.addWidget(name_label)

		self.name_edit = QLineEdit()
		name_layout.addWidget(self.name_edit)

		path_layout = QHBoxLayout()
		self.mainLayout.addLayout(path_layout)

		path_label = QLabel('path: ')
		path_label.setFixedWidth(35)
		path_layout.addWidget(path_label)

		self.path_edit = QLineEdit()
		path_layout.addWidget(self.path_edit)


		btn_layout = QHBoxLayout()
		btn_layout.setContentsMargins(15,0,15,0)
		btn_widget = QDialog()
		btn_widget.setStyleSheet('border: 0px;')
		btn_widget.setFixedHeight(50)
		btn_widget.setLayout(btn_layout)
		self.mainLayout.addWidget(btn_widget)

		self.add_btn = QPushButton('Add')
		btn_layout.addWidget(self.add_btn)

		self.cancel_btn = QPushButton('Cancel')
		self.cancel_btn.clicked.connect(self.close)
		btn_layout.addWidget(self.cancel_btn)






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
		