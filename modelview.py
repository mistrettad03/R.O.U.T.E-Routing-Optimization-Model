from PyQt6.QtCore import(Qt, QAbstractListModel, QAbstractTableModel)
from PyQt6.QtWidgets import(QVBoxLayout, QWidget, QTableView)
import pandas as pd

# list model for combo box
class ListModel(QAbstractListModel):
    def __init__(self, *args, data=None, **kwargs):
        super(ListModel, self).__init__()
        self.data = data or None
        
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            text = self.data[index.row()]
            return text
        
    def rowCount(self, index):
        return len(self.data)
    
    def add(self, newItem):
        self.data.append(newItem)
        self.layoutChanged.emit()
        
    def delete(self, index):
        del self.data[index]
        self.layoutChanged.emit()
        
# table model for 2D (tabular) data
class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        
    def rowCount(self, index):
        return len(self._data)
    
    def columnCount(self, index):
        return len(self._data[0])
    
# display data in QTableView in QWidget
class TableViewWindow(QWidget):
    def __init__(self, data, title):
        super(TableViewWindow, self).__init__()
        
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)
        self.setWindowTitle(title)
        
        self.table = QTableView() # visual control
        
        if isinstance(data, pd.DataFrame):
            self.model = DataFrameModel(data)
        else:
            self.model = TableModel(data)
        
        
        self.table.setModel(self.model)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
# table model for Pandas DataFrame
class DataFrameModel(QAbstractTableModel):
    def __init__(self, data):
        super(DataFrameModel, self).__init__()
        self._data = data
        
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row()][index.column()]
            return str(value)
        
    def rowCount(self, index):
        return self._data.shape[0]
    
    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, oritentation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if oritentation == Qt.Orientation.Horizontal:
                return str(self._data.columns[section])
            if oritentation == Qt.Orientation.Vertical:
                return str(self._data.index[section])