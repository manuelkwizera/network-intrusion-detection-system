from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from dashboard import Dashboard
from database_connector import DatabaseConnector


class Login(QDialog):
    def __init__(self, widget):
        super(Login, self).__init__()
        loadUi("view/login.ui", self)
        self.widget = widget
        self.loginbutton.clicked.connect(self.handle_authentication)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.database_connector = DatabaseConnector()
      
    def handle_authentication(self):
        username = self.username.text()
        password = self.password.text()
    
        # Authenticate user
        if self.database_connector.authenticate(username, password):
            self.show_dashboard()
        else:
            self.show_alert()
            
    #show alter when login fails
    def show_alert(self):
        QMessageBox.information(self, 'Alert', 'Invalid username or password!', QMessageBox.Ok)

    def show_dashboard(self):
        dashboard = Dashboard()
        self.widget.addWidget(dashboard)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        

    