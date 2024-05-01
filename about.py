import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap

class AboutWindow(QWidget):

    # displays user name
    def get_label(self, text, style):
        label = QLabel()
        label.setText(text)
        label.setStyleSheet(style)
        label.setWordWrap(True)
        return label

    # displays user image 
    def get_image(self, filename):
        label = QLabel()
        filepath = os.path.dirname(os.path.realpath(__file__)) + '/icons/' + filename
        pixmap = QPixmap(filepath)
        label.setPixmap(pixmap.scaled(150, 150)) 
        return label

    # member title display layout
    def insert_title(self, title, image, layout):
        style = "QLabel{color: red; border-width: 1px; font: bold 20px }"
        current_layout = QHBoxLayout()
        current_image = self.get_image(image)
        current_layout.addWidget(current_image)
        current_label = self.get_label(title, style)
        current_layout.addWidget(current_label)
        current_layout.addStretch()
        layout.addLayout(current_layout)

    def insert_text(self, text, layout):
        style = "QLabel{color: green; font: 16px}" 
        label = self.get_label(text, style)
        layout.addWidget(label)

    # initializing window to display usernames and passwords
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setWindowTitle("About Window")

        # vertical layouts
        laceylayout = QVBoxLayout()
        dereklayout = QVBoxLayout()
        dominiclayout = QVBoxLayout()
        laurenlayout = QVBoxLayout()
        matthewlayout = QVBoxLayout()

        # left layout
        leftLayout = QVBoxLayout()
        leftLayout.addLayout(laceylayout)
        leftLayout.addLayout(laurenlayout)

        #Right layout
        rightLayout = QVBoxLayout()
        rightLayout.addLayout(dereklayout)
        rightLayout.addLayout(dominiclayout)
        rightLayout.addLayout(matthewlayout)

        # main layout
        mainlayout = QHBoxLayout()
        mainlayout.addLayout(leftLayout)
        mainlayout.addLayout(rightLayout)

        self.insert_title("Lacey Armstrong", "icon.lacey.png", laceylayout)
        self.insert_text("Dashboard Design(laceyarmstrong1@vt.edu)", laceylayout)

        self.insert_title("Derek Furr", "icon.derek.png", dereklayout)
        self.insert_text("Tutorial Design(dfurr35@vt.edu)", dereklayout)

        self.insert_title("Dominic Mistretta", "icon.dominic.png", dominiclayout)
        self.insert_text("Database Design(mistrettad03@vt.edu)", dominiclayout)

        self.insert_title("Lauren Lenhard", "icon.lauren.png", laurenlayout)
        self.insert_text("Log-In Design(lenhardlaurene@vt.edu)", laurenlayout)

        self.insert_title("Matthew McCullough", "icon.Matthew.png", matthewlayout)
        self.insert_text("Map Design(matthew25@vt.edu)", matthewlayout)

        mainlayout.addStretch()
        self.setLayout(mainlayout)
