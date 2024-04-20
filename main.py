import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from login import Login
"""
sudo .venv/bin/python main.py
"""

def main():
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    mainwindow = Login(widget)  # Pass widget to the Login class constructor
    widget.addWidget(mainwindow)
    widget.setFixedWidth(1000)
    widget.setFixedHeight(600)
    widget.show()
    app.exec_()

if __name__ == '__main__':
    main()
