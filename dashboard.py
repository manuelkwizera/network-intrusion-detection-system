from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class Dashboard(QDialog):
    def __init__(self):
        super(Dashboard, self).__init__()
        loadUi("dashboard.ui", self)
        
