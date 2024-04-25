import requests
import json
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt


"""
Geolocate an IP address using an IP address database
Geolocation DB is free-to-use and doesn't require an API key. 
It stores an impressive database of IP addresses obtained from Internet service providers.
"""

class IPGeolocator(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.get_ip_info_button = parent.get_ip_info_button  
        self.ip_address = parent.ip_address_input
        
        #table static rows header
        self.COUNTRY_CODE_COLUMN = 0
        self.COUNTRY_NAME_COLUMN = 1
        self.CITY_COLUMN = 2
        self.POSTAL_COLUMN = 3
        self.LATITUDE_COLUMN = 4
        self.LONGITUDE_COLUMN = 5
        self.IPV4_COLUMN = 6
        self.STATE_COLUMN = 7
 
        
    def get_ip_info(self):
        ip_address = self.ip_address.text()
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)
        
        #display geolocation data inside the table
        row_index = 0 
        self.parent.ip_geolocation_table.setItem(row_index, self.COUNTRY_CODE_COLUMN, QTableWidgetItem(result['country_code']))
        self.parent.ip_geolocation_table.setItem(row_index, self.COUNTRY_NAME_COLUMN, QTableWidgetItem(result['country_name']))
        self.parent.ip_geolocation_table.setItem(row_index, self.CITY_COLUMN, QTableWidgetItem(result['city']))
        self.parent.ip_geolocation_table.setItem(row_index, self.POSTAL_COLUMN, QTableWidgetItem(result['postal']))
        self.parent.ip_geolocation_table.setItem(row_index, self.LATITUDE_COLUMN, QTableWidgetItem(str(result['latitude'])))
        self.parent.ip_geolocation_table.setItem(row_index, self.LONGITUDE_COLUMN, QTableWidgetItem(str(result['longitude'])))
        self.parent.ip_geolocation_table.setItem(row_index, self.IPV4_COLUMN, QTableWidgetItem(result['IPv4']))
        self.parent.ip_geolocation_table.setItem(row_index, self.STATE_COLUMN, QTableWidgetItem(result['state']))       

        # Format geolocation data into a string
        formatted_info = ""
        for key, value in result.items():
            formatted_info += f"<b>{key}</b>: {value}<br>"
            
            
        # Display formatted geolocation data in QMessageBox
        #message_box = QMessageBox()
        #message_box.setWindowTitle('IP Information')
        #message_box.setTextFormat(Qt.RichText)  # Set text format to support HTML
        #message_box.setText(formatted_info)
        #message_box.exec_()

