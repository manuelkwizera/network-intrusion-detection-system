from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from packet_sniffer import PacketSniffer
import scapy.all as scp

class Dashboard(QDialog):
    def __init__(self):
        super(Dashboard, self).__init__()
        loadUi("dashboard.ui", self)
        self.startsniff.clicked.connect(self.start_sniff)
        self.stopsniff.clicked.connect(self.stop_sniff)
        self.clear_table_button.clicked.connect(self.clear_packet_table)
        self.sniffer = None  # Initialize sniffer as None

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
