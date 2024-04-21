from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from packet_sniffer import PacketSniffer
import scapy.all as scp
from ip_geolocator import IPGeolocator
from network_scanner import NetworkScanner

class Dashboard(QDialog):
    def __init__(self, widget):
        super(Dashboard, self).__init__()
        loadUi("view/dashboard.ui", self)
        self.widget = widget
        self.startsniff.clicked.connect(self.start_sniff)
        self.stopsniff.clicked.connect(self.stop_sniff)
        self.clear_table_button.clicked.connect(self.clear_packet_table)
        self.sniffer = None  # Initialize sniffer as None
        self.get_ip_info_button.clicked.connect(self.get_ip_geolocator)
        self.network_scanner_button.clicked.connect(self.show_network_scanner)

    #start packet sniffing
    def start_sniff(self):
        ifaces = [iface for iface in scp.conf.ifaces]
        #self.sniffer = PacketSniffer(ifaces[0:7])
        self.sniffer = PacketSniffer(ifaces[0:7], self.tableWidget)  # Pass tableWidget reference
        self.sniffer.start_capture()
    
    #stop packet sniffing
    def stop_sniff(self):
        if self.sniffer:  # Check if sniffer instance exists
            self.sniffer.stop_capture()
        else:
            print("No capture running")
    
    #clear packet sniffing table
    def clear_packet_table(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

    def get_ip_geolocator(self):
        ip_geolocator = IPGeolocator(self.widget)
        ip_geolocator.get_ip_info()
        
    def show_network_scanner(self):
        target_ip = "192.168.150.1/24"
        network_scanner = NetworkScanner(target_ip)
        self.widget.addWidget(network_scanner)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        

        