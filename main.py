import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication,
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
    QComboBox, QListWidget, QTreeWidget, QTreeWidgetItem,
    QPushButton, QProgressBar, QColorDialog, QFileDialog, 
    QMdiArea, QMdiSubWindow
)

from PyQt6.QtWidgets import QMessageBox  

from dashboard import DashboardWindow

import menutoolbar as mt

import os

from PyQt6.QtCore import Qt
from login import LoginWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Social Network")

        self.loginwin = LoginWindow()
        self.loginwin.show()

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        #subwindows dictionary
        self.subwindows = {'dashboard' : None, 'data': None, 'tutorial': None, 'visualize': None, 'about' : None}
        
        #dashboard window
        self.dashboard = DashboardWindow(self)
        self.add_subwindow(self.dashboard, 'dashboard')

        # menu and toolbar
        self.menutoolbar = mt.MenuToolbar(self)
        self.toolbar = self.menutoolbar.toolbar
        self.enable_access(True)

    # add subwindow and add it in subwindows dictionary
    def add_subwindow(self, window, name):
        if self.subwindows[name]:
            self.subwindows[name].close()
        sub = QMdiSubWindow()
        sub.setWidget(window)
        sub.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        sub.setWindowTitle(name)
        self.mdi.addSubWindow(sub)
        self.subwindows[name] = sub
        sub.showMaximized()

    # enable controls
    def enable_access(self, val):
        self.dashboard.setEnabled(val)
        self.menutoolbar.toolbar.setEnabled(val)
        self.menutoolbar.data_menu.setEnabled(val)
        self.menutoolbar.analyze_menu.setEnabled(val)



app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()

app.exec()    
