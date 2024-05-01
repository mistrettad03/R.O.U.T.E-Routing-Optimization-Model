import sys
import sqlite3
import os
from PyQt6.QtGui import QPixmap
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import misc

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setWindowTitle("Login")
        
        # line edits for username and password
        self.userEditLine = QLineEdit(self)
        self.passwordEditLine = QLineEdit(self)
        self.passwordEditLine.setEchoMode(QLineEdit.EchoMode.Password)
        
        # push buttons for login and cancel
        self.loginButton = QPushButton("Login")
        self.cancelButton = QPushButton("Cancel")
        
        # label for image
        self.imageLabel = QLabel(self)
        
        # load and display login image
        filepath = os.path.join(os.path.dirname(__file__), 'icons/icon.login.png')
        pixmap = QPixmap(filepath)
        self.imageLabel.setPixmap(pixmap.scaled(150,150))

         # prevent advancing to the application while login window is running
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint)
        
        # login layout
        loginLayout = QVBoxLayout()
        loginLayout.addWidget(self.imageLabel)
        loginLayout.addWidget(QLabel("Username:"))
        loginLayout.addWidget(self.userEditLine)
        loginLayout.addWidget(QLabel("Password:"))
        loginLayout.addWidget(self.passwordEditLine)
        loginLayout.addWidget(self.loginButton)
        self.loginButton.clicked.connect(self.login_click)
        loginLayout.addWidget(self.cancelButton)
        self.cancelButton.clicked.connect(self.exit_app)
        self.setLayout(loginLayout)
        
        


    # checking login information and connecting to maintable
    def check_username_password(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UsersTable.db')        

        con = sqlite3.connect(filename)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM UsersTable")
        data = res.fetchall()
        found = False
        

        
        for item in data:
            user = self.userEditLine.text()
            password = self.passwordEditLine.text()
            if item[0] == user and item[1] == int(password):
                found = True
                break
        
        return found
    
    # login option and error checking if wrong username or password   
    def login_click(self):
        if self.check_username_password():
            self.close()
        else:
            self.passwordEditLine.setText(None)
            misc.show_message("Username or password not found.", "Login Error")
    
    # allows user to exit the app
    def exit_app(self):
        response = misc.exit_message("Are you sure you want to exit the application?", "Exit App")
        if response:
            sys.exit()
