from scapy.all import Ether, ARP, srp, sniff, conf
import threading
from time import sleep
import os


class ArpSpoofDetector:
    def __init__(self):
        self.terminate_sniffing = False #for tracking thread status
        self.sniff_thread = threading.Thread(target=self.start_sniffing)

         

    """
    This function will make an ARP request
    and retrieves the real MAC address the that IP address
    """

    def get_mac(self, ip):
        """
        Returns the MAC address of `ip`, if it is unable to find it
        for some reason, throws `IndexError`
        """
        p = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)
        result = srp(p, timeout=3, verbose=False)[0]
        return result[0][1].hwsrc


    """
    this function checks for ARP packets. More precisely,
    ARP replies, and then compares between the real MAC address and the
    response MAC address (that's sent in the packet itself).
    """

    def process(self, packet):
        if self.terminate_sniffing:
            return  # If termination flag is set, stop processing packets
        
        # if the packet is an ARP packet
        if packet.haslayer(ARP):
            # if it is an ARP response (ARP reply)
            if packet[ARP].op == 2:
                try:
                    # get the real MAC address of the sender
                    real_mac = self.get_mac(packet[ARP].psrc)
                    # get the MAC address from the packet sent to us
                    response_mac = packet[ARP].hwsrc
                    
                    # if they're different, definitely there is an attack
                    if real_mac != response_mac:
                        print(f"[!] You are under attack, REAL-MAC: {real_mac.upper()}, FAKE-MAC: {response_mac.upper()}")
                        #attacker_ip_address = self.get_ip_from_mac(response_mac)
                        #print("Attacker IP address:", attacker_ip_address)
                        self.log_arp_spoofing_attempt(response_mac)
                        
                except IndexError:
                    # unable to find the real mac
                    # may be a fake IP or firewall is blocking packets
                    pass


    """
    The sniff function from Scapy is used for packet sniffing, 
    allowing you to capture and process network packets in real-time
    """
    def start_sniffing(self):
        #prn: This argument specifies a callback function to be called for each packet sniffed. 
        #prn: This function is called with the packet as its argument.
        #store: This argument specifies whether to store the packets in memory or not
        sniff(timeout=60, store=False, prn=self.process)

    #running sniffing thread at the background
    def start(self):
        self.sniff_thread.start()

    def stop(self):
        self.terminate_sniffing = True
        self.sniff_thread.join()
    
    
    def get_ip_from_mac(self, mac_address):
        # Execute the "arp -a" command to get the ARP table
        arp_table = os.popen('arp -a').read()
        
        for line in arp_table.split('\n'):
            if mac_address in line:
                # Extract the IP address from the line
                ip_address = line.split()[1]
                return ip_address
        
        # If the MAC address is not found in the ARP table
        return None

    def log_arp_spoofing_attempt(self, mac_addres):
        print(mac_addres)
         

arp_spoof_detector = ArpSpoofDetector()
arp_spoof_detector.start()

try:
    while True:
        #print("Executing other tasks...")
        sleep(2)
except KeyboardInterrupt:
    print("Terminating sniffing thread...")
    arp_spoof_detector.stop()
    print("Sniffing thread terminated.")

            