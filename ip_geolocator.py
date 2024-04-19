import requests
import json
from PyQt5.QtWidgets import QDialog, QMessageBox


class IPGeolocator(QDialog):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.get_ip_info_button = widget.get_ip_info_button  # Assuming this is how you access the button
        self.ip_address = widget.ip_address  # Assuming this is how you access the IP address input field
        self.get_ip_info_button.clicked.connect(self.get_ip_info)

    def get_ip_info(self):
        ip_address = self.ip_address.text()
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)
        QMessageBox.information(self.widget, 'IP Information', json.dumps(result), QMessageBox.Ok)
        print(result)
