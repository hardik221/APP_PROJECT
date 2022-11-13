import unittest
from unittest.mock import Mock
import requests
from MainGateway import TDG
from connection import Connector
from controller import Main

class TestUtils(unittest.TestCase):
    def test_dbConnection(self):
        self.assertEqual(self.getDbObject(), Connector.create_connection(self))

    def test_api(self):
        url = f'https://www.googleapis.com/books/v1/volumes?q=love:keyes&key=AIzaSyCB4mblXymeFZnTJKzp409fWKh8QC8Ty5Y&maxResults=10'
        api_result = requests.get(url)
        self.assertEqual(api_result.status_code, 200)

    def test_read_api_and_insert_data(self):
        self.assertFalse(Main.readApiAndInsertData(self, TDG))

    def test_checkTableExists(self):
        db_connector = Mock()
        TDG.checkTableExists(db_connector)

    def test_singleton(self):
        self.assertEqual(Connector.create_connection(self), self.getDbObject())

    def test_write_data(self):
        db_connector = Mock()
        Main.write_data(db_connector, "File Write")

    def test_validation_string(self):
        self.assertEqual(TDG.validate_string(self, val=''), '')
        self.assertEqual(TDG.validate_string(self, val='Testing'), 'Testing')
        self.assertEqual(TDG.validate_string(self, val= 123), b'123')

    def getDbObject(self):
        return Connector.create_connection(self)

if __name__ == '__main__':
    unittest.main()
