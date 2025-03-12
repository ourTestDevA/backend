import os
import requests
import unittest
from unittest.mock import patch

class TestDuffelFlightsAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = 'http://localhost:5000'
        cls.api_key = os.getenv('DUFFEL_API_KEY')
        if not cls.api_key:
            raise ValueError("DUFFEL_API_KEY environment variable is not set")

    @patch.dict(os.environ, {"DUFFEL_API_KEY": "test_api_key"})
    def test_list_orders_success(self):
        response = requests.get(f'{self.base_url}/duffel-flights-list-orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json())

    @patch.dict(os.environ, {"DUFFEL_API_KEY": "invalid_api_key"})
    def test_list_orders_unauthorized(self):
        response = requests.get(f'{self.base_url}/duffel-flights-list-orders')
        self.assertEqual(response.status_code, 401)

    def test_list_orders_server_error(self):
        with patch('requests.get') as mocked_get:
            mocked_get.side_effect = requests.exceptions.RequestException
            response = requests.get(f'{self.base_url}/duffel-flights-list-orders')
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()