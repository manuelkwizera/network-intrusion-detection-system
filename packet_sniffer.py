import scapy.all as scp
import threading
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem
from scapy.layers.inet import IP, TCP, UDP


class PacketSniffer:
 
    def __init__(self, iface, tableWidget, filter="", timeout=30):
        self.iface = iface
        self.filter = filter
        self.timeout = timeout
        self.pkt_list = []
        self.sniff_thread = None
        self.capture_running = False  # Flag to indicate if capture is running
        self.tableWidget = tableWidget  # Reference to the tableWidget

    def pkt_process(self, pkt):
        if self.capture_running:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            summary = pkt.summary()
            self.pkt_list.append((timestamp, summary))
            print(f"[{timestamp}] {pkt.summary()}")

            # Add packet information to the table widget
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            self.tableWidget.setItem(row_position, 0, QTableWidgetItem(timestamp))
        
            if IP in pkt:  # Check if the packet is an IP packet
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem("IP"))
                self.tableWidget.setItem(row_position, 2, QTableWidgetItem(pkt[IP].src))
                self.tableWidget.setItem(row_position, 3, QTableWidgetItem(pkt[IP].dst))
                self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(len(pkt))))
                # No flags for IP packets, set an empty string for the flags column
                self.tableWidget.setItem(row_position, 5, QTableWidgetItem(""))
            else:
                # If the packet is not an IP packet, handle it accordingly
                protocol = "TCP" if TCP in pkt else ("UDP" if UDP in pkt else "Other")
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(protocol))
                self.tableWidget.setItem(row_position, 2, QTableWidgetItem(pkt.src))
                self.tableWidget.setItem(row_position, 3, QTableWidgetItem(pkt.dst))
                self.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(len(pkt))))
                #self.tableWidget.setItem(row_position, 5, QTableWidgetItem(pkt.flags) if TCP in pkt else QTableWidgetItem(""))
                self.tableWidget.setItem(row_position, 5, QTableWidgetItem(""))


    def get_port_number(self, src_ip, dst_ip, pkt):
        src_port = None
        dst_port = None

        if IP in pkt and pkt[IP].src == src_ip and pkt[IP].dst == dst_ip:
            if TCP in pkt:
                src_port = pkt[TCP].sport
                dst_port = pkt[TCP].dport
            elif UDP in pkt:
                src_port = pkt[UDP].sport
                dst_port = pkt[UDP].dport

        # Return the extracted port numbers
        return src_port, dst_port


    def start_capture(self):
        self.capture_running = True  # Set flag to indicate capture is running
        self.sniff_thread = threading.Thread(target=self._capture_thread, daemon=True)
        self.sniff_thread.start()

    def _capture_thread(self):
        try:
            scp.sniff(prn=self.pkt_process, filter=self.filter, iface=self.iface, timeout=self.timeout)
        except Exception as e:
            print("An error occurred during packet capture:", e)
        finally:
            self.capture_running = False  # Reset flag when capture stops

    def stop_capture(self):
        if self.sniff_thread and self.capture_running:
            self.capture_running = False  # Set flag to stop packet capture
            self.sniff_thread.join()  # Wait for thread to stop
            print("Capture stopped successfully")
        else:
            print("No capture running")

    def get_packet_count(self):
        return len(self.pkt_list)

