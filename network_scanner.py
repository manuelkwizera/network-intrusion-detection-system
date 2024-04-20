from scapy.all import ARP, Ether, srp

class NetworkScanner():
    def __init__(self, target_ip, connections_table):
        #target_ip = "192.168.150.1/24"
        self.target_ip = target_ip
        self.connections_table = connections_table
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
                