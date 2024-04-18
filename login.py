from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from dashboard import Dashboard


class Login(QDialog):
    def __init__(self, widget):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.widget = widget
        self.loginbutton.clicked.connect(self.handle_authentication)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def handle_authentication(self):
        email = self.username.text()
        password = self.password.text()
    
        # Handle authentication
        if email == "admin" and password == "admin":
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
        

    