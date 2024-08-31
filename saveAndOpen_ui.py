
# -*- coding: utf-8 -*-

import os
import sys
import time
import platform
import logging

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

# Setup Python Version
#---------------------
PY_VERSION = int(platform.python_version().split('.')[0])
if PY_VERSION == 3:
	from importlib import reload

MODULE_PATH = os.path.dirname(__file__).replace('\\', '/')
print(MODULE_PATH)
PATHS = [ MODULE_PATH ]
for path in PATHS:
	if not path in sys.path:
		sys.path.append(path)

import libs.src.saveAnoOpen_func as func
reload(func)
import utilityDialog as util
reload(util)

DCC = ''
CSS_PATH =  '{}/saveAndOpenTool_style.css'.format(MODULE_PATH)

class SceneManagerUI(QDialog):
	def __init__(self, parent = None):
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

		self.css_main = ''

		with open(CSS_PATH, 'r') as css:
			self.css_main = css.read()
		
		self.setStyleSheet(self.css_main)

		self.initTitleWidget()
		self.initBodyWidget()
		self.initBottomWidget()

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
		
		# self.bodyLayout = QHBoxLayout()
		# bodyWidget = QDialog()
		# bodyWidget.setLayout(self.bodyLayout)
		# self.mainLayout.addWidget(bodyWidget)

		self.bodyLayout = QSplitter()
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
		
	def initRecentWidget(self):

		# Recent Layout
		#-----------------
		recentLayout = QVBoxLayout()
		recentLayout.setAlignment(Qt.AlignTop)
		recentLayout.setContentsMargins(20, 0, 10, 10)
		recentWidget = QDialog()
		recentWidget.setFixedWidth(350)
		recentWidget.setLayout(recentLayout)
		self.bodyLayout.addWidget(recentWidget)

		recentTitleLayout = QHBoxLayout()
		recentTitleLayout.setContentsMargins(0,0,0,0)
		recentTitleWidget = QDialog()
		recentTitleWidget.setLayout(recentTitleLayout)
		recentLayout.addWidget(recentTitleWidget)

		recentLabel = QLabel('Recent')
		recentTitleLayout.addWidget(recentLabel)

		self.recentTree = QTreeWidget()
		self.recentTree.setStyleSheet('padding-left: 5px; border: 0px;')
		recentLayout.addWidget(self.recentTree)
		self.recentTree.setStyleSheet(self.css_main)
		self.recentTree.setRootIsDecorated(False)
		self.recentTree.setHeaderHidden(False)
		self.recentTree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.recentTree.setAutoScroll(False)
		self.recentTree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.recentTree.setHeaderLabels(['name', 'date', 'location'])
		self.recentTree.setColumnWidth(0, 225)
		self.recentTree.setColumnWidth(1, 95)

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

		locationLabel = QLabel('Location')
		locationTitleLayout.addWidget(locationLabel)

		self.fileSearch = util.SearchBoxWidget()
		# self.fileSearch.line.textChanged.connect(self.inputFileSearch)
		# self.fileSearch.searchBtn.clicked.connect(self.inputFileSearch)
		self.fileSearch.setStyleSheet('''
			border-radius: 0px;  border-bottom: 2px solid rgba(70, 70, 70, 100); background: rgba(40,40,40,100)''')
		self.fileSearch.setFixedSize(180, 22)
		locationTitleLayout.addWidget(self.fileSearch)

		self.backBtn = QPushButton()
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
		self.pathBox.setFixedHeight(25)
		self.pathBox.setStyleSheet('QLineEdit{background: rgb(30, 30, 30); border: 2px; border-bottom: 2px solid rgb(60, 60, 60)}')
		browseLayout.addWidget(self.pathBox)

		browseLayout.addWidget(self.backBtn)

		self.fileTree = QTreeWidget()
		locationLayout.addWidget(self.fileTree)
		self.fileTree.setStyleSheet('padding-left: 5px; border: 0px;')
		self.fileTree.setStyleSheet(self.css_main)
		self.fileTree.setRootIsDecorated(False)
		self.fileTree.setHeaderHidden(False)
		self.fileTree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
		self.fileTree.setAutoScroll(False)
		self.fileTree.setContextMenuPolicy(Qt.CustomContextMenu)
		self.fileTree.setHeaderLabels(['  name', 'date','owner', 'comment'])
		self.fileTree.setColumnWidth(0, 280)
		self.fileTree.setColumnWidth(1, 95)
		self.fileTree.setColumnWidth(2, 70)

		# command for sort tree item
		#---------------------------
		self.fileTree.sortByColumn(0,Qt.AscendingOrder)
		self.fileTree.setSortingEnabled(True)
		self.fileTree.header().setSortIndicatorShown(False)

		fileScrollbar = QScrollBar()
		self.fileTree.setVerticalScrollBar(fileScrollbar)

	def initBottomWidget(self):

		self.bottomLayout = QHBoxLayout()
		bottomWidget = QDialog()
		bottomWidget.setLayout(self.bottomLayout)
		self.mainLayout.addWidget(bottomWidget)

		bottomLabel = QLabel('Dcc')
		self.bottomLayout.addWidget(bottomLabel)


# ------------------------------------------- #
#               RUN TOOL FUNC                 #
# ------------------------------------------- #
def main(state='open'):

	global ENTITY 

	startTime = time.time()

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
		maya_ui = SceneManagerUI(parent=prt, state=state)
		maya_ui.show()


	elif DCC == 'houdini':

		import hou

		temp = hou.ui.mainQtWindow()
		temp.setStyleSheet('background:none;')
		
		houdini_ui = SceneManagerUI(parent=temp, state=state)
		houdini_ui.show()

	else:
		app = QApplication(sys.argv)
		ui = SceneManagerUI()
		ui.show()
		sys.exit(app.exec_())

	endTime = time.time()
	timeLap = endTime - startTime
	print(':: TOOL MASSAGE :: Time Open | {}'.format(timeLap))
	# logger.log(logging.INFO, '[{}] DCC : {} | {} | Time Open : {}'.format(PROJ_CODE, DCC, state, timeLap))


if __name__ == '__main__':
	main()
