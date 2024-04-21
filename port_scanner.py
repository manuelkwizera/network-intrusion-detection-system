import socket
from colorama import init, Fore
from PyQt5.QtWidgets import QTableWidgetItem


class PortScanner():
    def __init__(self, parent):
        self.parent = parent
        # Initialize colorama
        init()
        # Assigning instance variables for colors
        self.GREEN = Fore.GREEN
        self.RESET = Fore.RESET
        self.GRAY = Fore.LIGHTBLACK_EX
        
        self.host = None
        
    def is_port_open(self, host, port):
        """
        determine whether `host` has the `port` open
        """
        # creates a new socket
        s = socket.socket()
        try:
            # tries to connect to host using that port
            s.connect((host, port))
            # make timeout if you want it a little faster ( less accuracy )
            s.settimeout(0.2)
        except:
            # cannot connect, port is closed
            # return false
            return False
        else:
            # the connection was established, port is open!
            return True
    
    def run_port_scan(self):
        # Clear existing rows in the tableWidget
        self.parent.port_scan_table.clearContents()
        self.parent.port_scan_table.setRowCount(0)
        
        # get the host from the user
        host = self.parent.ip_address_input.text()

        # iterate over ports, from 1 to 1024
        for port in range(1, 1025):
            # Check if the port is open
            if self.is_port_open(host, port):
                print(f"{self.GREEN}[+] {host}:{port} is open {self.RESET}")
                status = "open"
            else:
                print(f"{self.GRAY}[!] {host}:{port} is closed {self.RESET}", end="\r")
                status = "closed"
            
            # Insert row into the table
            row_position = self.parent.port_scan_table.rowCount()
            self.parent.port_scan_table.insertRow(row_position)
            self.parent.port_scan_table.setItem(row_position, 0, QTableWidgetItem(host))
            self.parent.port_scan_table.setItem(row_position, 1, QTableWidgetItem(str(port)))
            self.parent.port_scan_table.setItem(row_position, 2, QTableWidgetItem(status))
