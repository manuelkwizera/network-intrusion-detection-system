import scapy.all as scp
import threading
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi

class Dashboard(QDialog):
    def __init__(self):
        super(Dashboard, self).__init__()
        loadUi("dashboard.ui", self)
        
        # Start packet capture
        self.pkt_list = []  # List to hold captured packets
        self.sniffthread = threading.Thread(target=self.start_sniffing, daemon=True)
        self.sniffthread.start()

    def start_sniffing(self):
        # Define what to do with each captured packet
        def pkt_process(pkt):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] # Get current timestamp
            self.add_packet_to_table(timestamp, pkt.summary())

        # Start packet capture
        scp.sniff(prn=pkt_process, filter="", iface=scp.conf.ifaces[:7], store=False)

    def add_packet_to_table(self, timestamp, pkt_summary):
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        self.tableWidget.setItem(row_position, 0, QTableWidgetItem(timestamp))
        self.tableWidget.setItem(row_position, 1, QTableWidgetItem(pkt_summary))
        # Add more columns and parse packet summary to populate them accordingly

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())
