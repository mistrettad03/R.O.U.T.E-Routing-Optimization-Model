from PyQt6.QtWidgets import QMessageBox

# show error message in a QMessageBox
def show_message(txt,title,icon = QMessageBox.Icon.NoIcon):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(txt)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    response = msg.exec()   
    
# show exit message in a QMessageBox
def exit_message(txt,title,icon = QMessageBox.Icon.Critical):
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(txt)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
    response = msg.exec()    
    if response == QMessageBox.StandardButton.Yes:
        return True
    else:
        return False
    