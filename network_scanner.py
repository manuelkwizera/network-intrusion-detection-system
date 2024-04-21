from scapy.all import ARP, Ether, srp
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class NetworkScanner(QDialog):
    def __init__(self, target_ip):
        super(NetworkScanner, self).__init__()
        loadUi("view/connections.ui", self)
        self.target_ip = target_ip
        self.clients = []
        self.result = []
    
    def scan_network(self):
        # IP Address for the destination
        # create ARP packet
        arp = ARP(pdst = self.target_ip) 
        # create the Ether broadcast packet
        # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        # stack them
        packet = ether/arp

        result = srp(packet, timeout=3, verbose=0)[0]
                