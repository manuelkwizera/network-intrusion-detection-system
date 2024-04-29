from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QDialog, QSpacerItem
from database_connector import DatabaseConnector
import datetime


class Report(QDialog):
    def __init__(self, widget):
        super(Report, self).__init__()
        loadUi("view/report.ui", self)
        self.widget = widget
        self.database_connector = DatabaseConnector()

        from dashboard import Dashboard
        self.dashboard = Dashboard()
        
        #set column width
        self.tableWidget.setColumnWidth(0, 190)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 100)
        
        #laod report data into the table
        self.load_data_button.clicked.connect(self.show_report_data)
        
        #holds the report data from the database
        self.data = [] 
        
        # redirect to dashboad when go to dashboard button is clicked
        self.go_to_dashboard_button.clicked.connect(self.show_dashbaord)

    def show_report_data(self):
        database_connector = DatabaseConnector()
        self.data = database_connector.fetch_report_data()
        print(self.data)
        
        for value in self.data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(value[1]))  
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(value[2]))  
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem(value[3]))  
            self.tableWidget.setItem(row_position, 3, QTableWidgetItem("2024-04-22 "))  
            self.tableWidget.setItem(row_position, 4, QTableWidgetItem(value[5]))  
            self.tableWidget.setItem(row_position, 5, QTableWidgetItem(value[6]))  
            self.tableWidget.setItem(row_position, 6, QTableWidgetItem("active"))
            
            # Create layout for buttons
            button_layout = QHBoxLayout()
            delete_button = QPushButton("Delete", self)
            button_layout.addWidget(delete_button)
            
            delete_button.setFixedSize(70, 20)

            # Create a widget to hold the layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            # Set the widget as the cell widget for the desired column
            self.tableWidget.setCellWidget(row_position, 7, button_widget)

    # load dashboard widget
    def show_dashbaord(self):
        self.widget.addWidget(self.dashboard)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

           