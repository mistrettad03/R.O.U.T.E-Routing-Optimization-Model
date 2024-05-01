from PyQt6.QtWidgets import (QToolBar, QStatusBar)
from PyQt6.QtGui import (QAction, QIcon)
from PyQt6.QtCore import Qt
import os

class MenuToolbar():
    def __init__(self, window):
        
        self.toolbar = QToolBar('MainToolBar')
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        
        self.folder = os.path.dirname(os.path.realpath(__file__)) + '/icons/'
        
        # menu, toolbar, statusbar
        self.menu = window.menuBar()
        window.addToolBar(self.toolbar)
        window.setStatusBar(QStatusBar(window))
        
        # file menu and toolbar buttons
        self.file_menu = self.menu.addMenu('&File')
        
        self.add_button('&Open', 'Open file', 'icon.open.png',
                        self.file_menu, window, window.dashboard.open_database)       
        self.add_button('&Exit', 'Exit file', 'icon.exit.png',
                        self.file_menu, window, window.dashboard.exit_app)
        
        self.toolbar.addSeparator()
        
        
        # data menu and toolbar buttons
        self.data_menu = self.menu.addMenu('&Data')

        self.toolbar.addSeparator()
        self.analyze_menu = self.menu.addMenu('&Analyze')

        
        self.add_button('&Analyze' , 'Show Analyze' , 'icon.analyze.png',
                        self.data_menu, window, window.dashboard.analyze_data)
        self.add_button('&Visualize' , 'Show Visualize' , 'icon.visualize.png',
                        self.data_menu, window, window.dashboard.visualize)

        self.add_button('D&ash', 'Show Dashboard', 'icon.dash.png', 
                        self.data_menu, window, window.dashboard.show_dashboard)     
        self.add_button('&Data', 'Show data', 'icon.data.png', 
                        self.data_menu, window, window.dashboard.show_data_window)  
        
        
        self.toolbar.addSeparator()

        self.help_menu = self.menu.addMenu('&Help')

        self.add_button('&Tutorial' , 'Show Tutorial' , 'icon.tutorial.png', 
                         self.data_menu, window, window.dashboard.tutorial)
        self.add_button('A&bout', 'About', 'icon.about.png', 
                       self.data_menu, window, window.dashboard.about)  
        
        
    
    # adds a button to the toolbar and menu
    def add_button(self, text, tip, file, menu, win, func):
        btn = QAction(QIcon(self.folder + file), text, win)
        btn.setStatusTip(tip)
        self.toolbar.addAction(btn)
        menu.addAction(btn)  
        if func:
            btn.triggered.connect(func)     
        

