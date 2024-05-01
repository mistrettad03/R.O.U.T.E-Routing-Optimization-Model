import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPixmap

class TutorialWindow(QWidget):

    # tutorial button display
    def get_label(self, text, style):
        label = QLabel()
        label.setText(text)
        label.setStyleSheet(style)
        label.setWordWrap(True)
        return label

    # displays corresponding icon
    def get_image(self, filename):
        label = QLabel()
        filepath = os.path.dirname(os.path.realpath(__file__)) + '/icons/' + filename
        pixmap = QPixmap(filepath)
        label.setPixmap(pixmap.scaled(20, 20)) 
        return label

    # populates header section for image and label
    def insert_title(self, title, image, layout):
        style = "QLabel{color: red; border-width: 1px; font: bold 20px }"
        current_layout = QHBoxLayout()
        current_image = self.get_image(image)
        current_layout.addWidget(current_image)
        current_label = self.get_label(title, style)
        current_layout.addWidget(current_label)
        current_layout.addStretch()
        layout.addLayout(current_layout)

    # adds text to explain icon
    def insert_text(self, text, layout):
        style = "QLabel{color: green; font: 16px}" 
        label = self.get_label(text, style)
        layout.addWidget(label)

    # initializing tutorial window with buttons
    def __init__(self):
        super(TutorialWindow, self).__init__()
        self.setWindowTitle("Tutorial Window")
         
        mainLayout = QVBoxLayout()

        self.insert_title("Open Button", "icon.open.png", mainLayout)
        self.insert_text("This button allows the user to select a database file" + \
                    "from the user's computer", mainLayout)

        self.insert_title("Exit", "icon.exit.png", mainLayout)
        self.insert_text("This button allows the user to exit the entire window ", mainLayout)

        self.insert_title("Analyze", "icon.analyze.png", mainLayout)
        self.insert_text("This button performs an analysis of route data entered into the application." +\
                        "To perform an analysis, press the ‘Open’ icon in the top left corner and import" +\
                        "‘MainTable.db’ database. Then choose the origin and stops for the route you would" +\
                        " like to optimize. If you want to add or remove stops, simply select the city/town" +\
                        " you would like to add or remove and press the corresponding button. Lastly, you " +\
                        "can select if you would like to use a greedy or optimal method at the bottom of the " +\
                        "screen in a dropdown menu. Once you have all the information selected, you can select " +\
                        "the ‘Analyze’ button at the top of the toolbar or the ‘Analyze. You will be provided " +\
                        "with the individual route distances of the giving city and the receiving city for each " +\
                        "interaction until the end location is met. The total distance of all the routes taken is " +\
                        "displayed below the individual route box.", mainLayout)

        # dashboard button and explanation
        self.insert_title("Dash", "icon.dash.png", mainLayout)
        self.insert_text("The dash button serves as a navigational tool, allowing "
                        "users to return to the main dashboard interface from any "
                        "other screen within the application. The other screens they "
                        "could be on would be Visualize, Data, Tutorial or "
                        "About. Clicking the dash button would provide users with "
                        "quick access to the central hub of the application, where "
                        "they can select different origins, locations, add or remove "
                        "stops to create new paths, and analyze the data. This allows for "
                        "seamless navigation throughout the application.", mainLayout)


        self.insert_title("Data", "icon.data.png", mainLayout)
        self.insert_text("After the user has selected a file to import into the software,"+\
                        " the user can then select the data button which allows the user to" +\
                        " see the data imported.  The data is shown in a table with the city" +\
                        " names, left coordinate, and right coordinate for the assigned locations.", mainLayout)

        self.insert_title("Visualize", "icon.data.png", mainLayout)
        self.insert_text("After the user has added their stops and then selected to analyze data, the user can " +\
                        "select whether they would like the route to be greedy or optimal. Then once the Visualize" +\
                        " button is pressed, it opens up a map of Virginia with all of the cities labeled. It then" +\
                        " shows the selected route with a blue colored line to show the most optimal or greedy route" +\
                        "through all of the cities from the beginning destination to the end.", mainLayout)

        mainLayout.addStretch()
        self.setLayout(mainLayout)
