import requests
import json
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt


"""
Geolocate an IP address using an IP address database
Geolocation DB is free-to-use and doesn't require an API key. 
It stores an impressive database of IP addresses obtained from Internet service providers.
"""

class IPGeolocator(QDialog):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.get_ip_info_button = widget.get_ip_info_button  # Assuming this is how you access the button
        self.ip_address = widget.ip_address_input  # Assuming this is how you access the IP address input field
        
    def get_ip_info(self):
        ip_address = self.ip_address.text()
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)

        # Format geolocation data into a string
        formatted_info = ""
        for key, value in result.items():
            formatted_info += f"<b>{key}</b>: {value}<br>"

        # Display formatted geolocation data in QMessageBox
        message_box = QMessageBox()
        message_box.setWindowTitle('IP Information')
        message_box.setTextFormat(Qt.RichText)  # Set text format to support HTML
        message_box.setText(formatted_info)
        message_box.exec_()

