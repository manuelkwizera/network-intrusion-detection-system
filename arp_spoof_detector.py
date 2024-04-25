from scapy.all import Ether, ARP, srp, sniff, conf
import threading
from time import sleep

class ArpSpoofDetector:
    def __init__(self):
        self.terminate_sniffing = False #for tracking thread status
         

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
                real_mac = get_mac(packet[ARP].psrc)
                # get the MAC address from the packet sent to us
                response_mac = packet[ARP].hwsrc
                
                # if they're different, definitely there is an attack
                if real_mac != response_mac:
                    print(f"[!] You are under attack, REAL-MAC: {real_mac.upper()}, FAKE-MAC: {response_mac.upper()}")
            
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
    sniff(timeout=60, store=False, prn=process)

#running sniffing thread at the background
def start(self):
    self.sniff_thread.start()

def stop():
    


# Start sniffing in a separate thread
sniff_thread = threading.Thread(target=start_sniffing)
sniff_thread.start()


try:
    while True:
        print("Executing other tasks...")
        sleep(2)
except KeyboardInterrupt:
    # If user interrupts the program (e.g., Ctrl+C)
    print("Terminating sniffing thread...")
    terminate_sniffing = True
    sniff_thread.join()  # Wait for the sniffing thread to terminate gracefully
    print("Sniffing thread terminated.")
            