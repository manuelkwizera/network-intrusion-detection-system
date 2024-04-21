from scapy.all import ARP, Ether, srp
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QDialog, QSpacerItem
from port_scanner import PortScanner

class NetworkScanner(QDialog):
    def __init__(self, target_ip, widget, dashboard):
        super(NetworkScanner, self).__init__()
        loadUi("view/connections.ui", self)
        self.dashboard = dashboard
        self.widget = widget
        self.target_ip = target_ip
        self.clients = [] # a list of clients, we will fill this in the upcoming loop
        self.result = []
        
        #set column width
        self.tableWidget.setColumnWidth(0, 160)
        self.tableWidget.setColumnWidth(1, 160)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 210)
        
        #detect when network scan button is clicked
        self.start_net_scan_button.clicked.connect(self.scan_network)
        
        #go back to dashbaord page
        self.got_to_dashboard_button.clicked.connect(self.show_dashbaord)
        
        #clear table widget
        self.clear_san_table_button.clicked.connect(self.clear_table)
        
        #detect when scan button is cliecked
        self.port_scan_button.clicked.connect(self.scan_ports)
    
    """
    scan for available devices in the network
    """   
    def scan_network(self):
        arp = ARP(pdst=self.target_ip)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether/arp
        result = srp(packet, timeout=3, verbose=0)[0]
        
        # Clear existing rows in the tableWidget
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        for sent, received in result:
            # Append IP and MAC address to `clients` list
            self.clients.append({'ip': received.psrc, 'mac': received.hwsrc})

        # Populate tableWidget with client data
        print("Available devices in the network:")
        print("IP" + " "*18+"MAC")
        
        for client in self.clients:
            print("{:16} {}".format(client['ip'], client['mac']))
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(client['ip']))
            self.tableWidget.setItem(row_position, 1, QTableWidgetItem(client['mac']))
            self.tableWidget.setItem(row_position, 2, QTableWidgetItem("active"))
            
            # Create layout for buttons
            button_layout = QHBoxLayout()
            enable_button = QPushButton("Enable", self)
            disable_button = QPushButton("Disable", self)
            button_layout.addWidget(enable_button)
            button_layout.addWidget(disable_button)
            
            enable_button.setFixedSize(70, 20) 
            disable_button.setFixedSize(70, 20)


            # Create a widget to hold the layout
            button_widget = QWidget()
            button_widget.setLayout(button_layout)

            # Set the widget as the cell widget for the desired column
            self.tableWidget.setCellWidget(row_position, 3, button_widget)

    def show_dashbaord(self):
        self.widget.addWidget(self.dashboard)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def clear_table(self):
        self.clients.clear()
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
    
    def scan_ports(self):
        port_scanner = PortScanner(self)
        port_scanner.run_port_scan()