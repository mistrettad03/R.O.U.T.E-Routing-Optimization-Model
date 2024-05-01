import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication,
    QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
    QComboBox, QListWidget, QTreeWidget, QTreeWidgetItem,
    QPushButton, QProgressBar, QColorDialog, QFileDialog, 
    QMdiArea, QMdiSubWindow
)

from PyQt6.QtWidgets import QMessageBox  

import misc as Misc
from network import Node, Edge, Network

from itertools import groupby
import numpy as np

import modelview as mv
import pandas as pd
import routing
from routing import Optimization, Routing


import menutoolbar as mt
import os 
from PyQt6.QtCore import Qt
from database import Database as db

from tutorial import TutorialWindow
from about import AboutWindow
from visualize import GraphWindow

from PIL import Image




class DashboardWindow(QWidget):

    def __init__(self, window):
        super(QWidget, self).__init__()
        self.mdi_parent = window

        # show data button 
        self.showDataButton = QPushButton("Show Data")
        self.showDataButton.setFixedWidth(100)
        self.showDataButton.clicked.connect(self.show_data_window)
        
        # origin layout
        originLayout = QVBoxLayout()
        originLayout.addWidget(QLabel("Origin"))
        self.originComboBox = QComboBox()
        #self.originComboBox.currentIndexChanged.connect(self.origincombobox_currentindexchanged)
        originLayout.addWidget(self.originComboBox)

        # location layout
        locationLayout = QVBoxLayout()
        locationLayout.addWidget(QLabel("Location"))
        self.locationListWidget = QListWidget()        
        locationLayout.addWidget(self.locationListWidget)
        self.addLocationButton = QPushButton("Add Stop")
        self.addLocationButton.clicked.connect(self.add_stop_window)
        locationLayout.addWidget(self.addLocationButton)
        
        # stops layout
        stopsLayout = QVBoxLayout()
        stopsLayout.addWidget(QLabel("Stops"))
        self.stopsListWidget = QListWidget()        
        stopsLayout.addWidget(self.stopsListWidget)
        self.removeLocationButton = QPushButton("Remove Stop")
        self.removeLocationButton.clicked.connect(self.remove_stop_window)
        stopsLayout.addWidget(self.removeLocationButton)


        # tree Display layout
        treeLayout = QVBoxLayout()
        self.route_label = QLabel("Route")
        treeLayout.addWidget(self.route_label)
        self.routeTreeWidget = QTreeWidget()
        self.routeTreeWidget.setHeaderHidden(True)
        treeLayout.addWidget(self.routeTreeWidget)
        self.route_length_label = QLabel("Route Length: ")
        treeLayout.addWidget(self.route_length_label)
        self.analyzeButton = QPushButton("Analyze Data")
        self.analyzeButton.clicked.connect(self.analyze_data)
        treeLayout.addWidget(self.analyzeButton)

        # method layout
        methodLayout = QVBoxLayout()
        methodLayout.addWidget(QLabel("Select method"))
        self.methodComboBox = QComboBox()
        #self.methodComboBox.currentIndexChanged.connect(self.methodCombobox_currentindexchanged)
        methodLayout.addWidget(self.methodComboBox)

        # buttons layout
        '''
        buttonsLayout = QHBoxLayout()
        self.addLocationButton = QPushButton("Add location")
        self.addLocationButton.clicked.connect(self.add_location_window)
        self.removeLocationButton = QPushButton("Remove location")
        self.removeLocationButton.clicked.connect(self.remove_location_window)
        self.analyzeButton = QPushButton("Analyze data")
        self.analyzeButton.clicked.connect(self.analyze_data)
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.addLocationButton)
        buttonsLayout.addWidget(self.removeLocationButton)
        buttonsLayout.addWidget(self.analyzeButton)
        ''' 

        # left layout
        leftLayout = QVBoxLayout()
        leftLayout.addLayout(originLayout)
        leftLayout.addLayout(locationLayout)
        leftLayout.addLayout(stopsLayout)
        leftLayout.setContentsMargins(0,0,0,10)
        
        # top layout
        topLayout = QHBoxLayout()
        topLayout.addLayout(leftLayout)
        topLayout.addLayout(treeLayout)
        topLayout.setContentsMargins(0,0,0,10)

        #main layout
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(methodLayout)
        mainLayout.setContentsMargins(20,20,20,20)        
        self.setLayout(mainLayout)
        
        
    # function to open database
    def open_database(self):
        fname = None
        folder = os.path.dirname(os.path.realpath(__file__))
        fname, ok = QFileDialog.getOpenFileName(self, 'Open file',
                                folder, 'Sqlite3 database files (*.db)')
        
        if fname:
            self.mdi_parent.enable_access(True)
            self.database = db(fname)
            self.data, self.fields = self.database.get_data()
            self.dataset = pd.DataFrame(self.data, columns=self.fields)
            self.network = Network(self.database)
            self.initialize_dashboard()

    # show connection data in a window
    def show_data_window(self):
        data, fields = self.database.get_data()
        data = pd.DataFrame(data, columns = fields)
        win = mv.TableViewWindow(data, 'Connections')
        self.mdi_parent.add_subwindow(win,'data')

    # exit application
    def exit_app(self):
        response = Misc.exit_message('Are you sure you want to exit?', 'Exit App')
        if response:
            sys.exit()

    # show dashboard
    def show_dashboard(self):
        self.mdi_parent.dashboard.showMaximized()

    
    # initializing dashboard
    def initialize_dashboard(self):
        self.data, self.fields = self.database.get_data()
        self.network = Network(self.database)
        self.optimizaiton_model = Optimization(self.network)
        self.optimizaiton_model.set_matrices()

        self.originComboBox.clear()
        self.originComboBox.addItems(self.network.get_node_names())
        self.originComboBox.setCurrentIndex(0)
        
        self.locationListWidget.clear()
        self.locationListWidget.addItems(self.network.get_node_names())
        self.locationListWidget.setCurrentRow(0)
        
        self.methodComboBox.clear()
        self.methodComboBox.addItems(['greedy', 'optimal'])
        self.methodComboBox.setCurrentIndex(0)

    # checks if location is in location list widget
    def is_stop(self, location):
        for n in range(self.stopsListWidget.count()):
            item = self.stopsListWidget.item(n)
            if item.text() == location:
                return True
        return False

    # add location to stops list widget
    def add_stop_window(self):
        try:
            item = self.locationListWidget.currentItem()
            if item is None: 
                raise Exception('Select a locations first')
            stop = item.text()
            if self.is_stop(stop):
                raise Exception(stop + ' is already in the location list')
            
            self.stopsListWidget.addItem(stop)
        except Exception as e:
            Misc.show_message(e.args[0], 'Error', QMessageBox.Icon.Critical)
    
    # remove location from stops list widget
    def remove_stop_window(self):
        try:
            if self.stopsListWidget.count() == 0:
                raise ValueError('There is no stop to remove')
            item = self.stopsListWidget.currentItem()
            if item is None:
                raise ValueError('A stop must be selected')
            
            row = self.stopsListWidget.currentRow()
            self.stopsListWidget.takeItem(row)
        except Exception as e:
            Misc.show_message(e.args[0], 'Error', QMessageBox.Icon.Critical)

    # function to analyze routes and lengths
    def analyze_data(self):
        self.show_dashboard()
        origin = self.originComboBox.currentText() 
        stops = []
        for item in range(self.stopsListWidget.count()):
            item = self.stopsListWidget.item(item)
            stops.append(item.text())
        
        route = None
        lengths = None
        routing_model = Routing(self.optimizaiton_model, origin, stops)
        
        if self.methodComboBox.currentText() == 'greedy':
            route, lengths = routing_model.get_greedy_route()
        else:
            route, lengths = routing_model.get_optimal_route()

        route_length = sum(lengths)
        self.route_length_label.setText("Route Length: {0:.4f}".format(route_length))
        
        self.routeTreeWidget.clear()
        self.route = route
        count = 0

        for path in route:
            origin = path[0].tail.name
            destination = path[-1].head.name
            current_length = lengths[count]
            count += 1
            path_item = QTreeWidgetItem()
            path_item.setText(0,origin + destination + ' : ' + '{0:.4f}'.format(current_length))
            self.routeTreeWidget.addTopLevelItem(path_item)
            
            for arc in path:
                arc_item = QTreeWidgetItem()
                arc_item.setText(0,arc.name + '-' + '{0:.4f}'.format(arc.weight))
                path_item.addChild(arc_item)
    
    def tutorial(self):
        window = TutorialWindow()
        self.mdi_parent.add_subwindow(window, 'tutorial')

    def visualize(self):
        origin = self.originComboBox.currentText()
        stops = [self.stopsListWidget.item(i).text() for i in range(self.stopsListWidget.count())]
        
        image = 'virginia_map.png'
        
        node_ids = [data[0] for data in self.data]
        node_colors = ['gray' for x in range(len(node_ids))]
        i = node_ids.index(origin)
        node_colors[i] = 'red'
        for stop in stops:
            j = node_ids.index(stop)
            node_colors[j] = 'green'

        positions = []

        width, height = Image.open(image).size
        for item in self.data:
            xcoord = item[1]/ width
            ycoord = item[2]/ height
            positions.append((xcoord, ycoord))

        node_size = 0.02
        sizes = [node_size for node in range(len(self.data))]
        
        arc_list = self.network.get_arcs()
        edges = [(arc.tail.name, arc.head.name) for arc in arc_list]

        edge_name = [arc.edgeName for arc in arc_list]
        edge_colors = ['black' for x in range(len(arc_list))]
        weights = [1 for x in range(len(arc_list))]
        
        edge_list = []
        for p in self.route:
            edge_list.extend(p)

        for edge in edge_list:
            i = edge_name.index(edge.edgeName)
            edge_colors[i] = 'blue'
            weights[i] = 5
               
        edge_values = ["{0:.0f}".format(arc.weight) for arc in arc_list]
        window = GraphWindow(node_ids, node_colors, positions, sizes, edges, edge_colors, weights, edge_values, image)
        self.mdi_parent.add_subwindow(window, 'visualize')

    def about(self):
        window = AboutWindow()
        self.mdi_parent.add_subwindow(window, 'about')
        
