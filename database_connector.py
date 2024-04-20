import mysql.connector
import hashlib


class DatabaseConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='password',
            database='nids'
        )
        
        self.cursor = self.connection.cursor()

    def authenticate(self, username, password):
        # Hash the provided password using MD5
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Execute the query with the hashed password
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, hashed_password))
        user = self.cursor.fetchone()
        return user is not None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()