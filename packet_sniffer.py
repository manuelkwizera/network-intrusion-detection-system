import scapy.all as scp
import threading
from datetime import datetime



"""
we have a class called PacketSniffer which encapsulates the functionality related to packet capturing.
The __init__ method initializes the object with the necessary parameters.
The pkt_process method is responsible for processing each packet captured.
The start_capture method starts the packet capture in a separate thread.
The stop_capture method stops the packet capture if it's still running.
The get_packet_count method returns the count of captured packets.
At the end, an instance of PacketSniffer is created and used to start and stop the packet capture, and to get the count of captured packets.
"""

class PacketSniffer:
    def __init__(self, iface, filter="", timeout=30):
        self.iface = iface
        self.filter = filter
        self.timeout = timeout
        self.pkt_list = []
        self.sniff_thread = None

    def pkt_process(self, pkt):
        self.pkt_list.append(pkt)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f"[{timestamp}] {pkt.summary()}")

    def start_capture(self):
        self.sniff_thread = threading.Thread(target=scp.sniff, kwargs={"prn": self.pkt_process, "filter": self.filter, "iface": self.iface}, daemon=True)
        self.sniff_thread.start()
        self.sniff_thread.join(timeout=self.timeout)

    def stop_capture(self):
        if self.sniff_thread and self.sniff_thread.is_alive():
            self.sniff_thread.join()

    def get_packet_count(self):
        return len(self.pkt_list)
    
    
ifaces = [iface for iface in scp.conf.ifaces]
sniffer = PacketSniffer(ifaces[0:7])
sniffer.start_capture()
sniffer.stop_capture()
print("Captured packets:", sniffer.get_packet_count())
