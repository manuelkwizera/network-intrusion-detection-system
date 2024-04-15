import scapy.all as scp
import threading
from datetime import datetime


#sudo .venv/bin/python network_scanner.py 

pkt_list = []  # this holds actual packet object

# get interface names
ifaces = [iface for iface in scp.conf.ifaces]

# define what to do with each captured packet
def pkt_process(pkt):
    global pkt_list

    pkt_list.append(pkt)  # add actual packet object to pkt_list
    #print(pkt.summary())  # print packet summary to console
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] # Get current timestamp
    print(f"[{timestamp}] {pkt.summary()}")


# start packet capture
sniffthread = threading.Thread(target=scp.sniff, kwargs={"prn": pkt_process, "filter": "", "iface": ifaces[0:7]}, daemon=True)
sniffthread.start()

# let the capture run for some time
sniffthread.join(timeout=30)  # Capture packets for 30 seconds

# stop the capture (if still running)
sniffthread.join()

# Print captured packet count
print("Captured packets:", len(pkt_list))
