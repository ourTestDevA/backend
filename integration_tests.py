import requests
import unittest
import os

class TestDuffelFlightsCreateOrders(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    ENDPOINT = "/duffel-flights-create-orders"
    HEADERS = {
        'Accept-Encoding': 'gzip',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Duffel-Version': 'v1',
        'Authorization': f"Bearer {os.getenv('YOUR_ACCESS_TOKEN', '<YOUR_ACCESS_TOKEN>')}"
    }

    def test_create_order_success(self):
        payload = {
            # Example payload, replace with actual test data
            "data": {
                "type": "order",
                "slices": [
                    {
                        "origin": "JFK",
                        "destination": "LAX",
                        "departure_date": "2023-12-01"
                    }
                ],
                "passengers": [
                    {
                        "type": "adult"
                    }
                ]
            }
        }
        response = requests.post(f"{self.BASE_URL}{self.ENDPOINT}", json=payload, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

    def test_create_order_invalid_data(self):
        payload = {
            # Example of invalid payload
            "data": {
                "type": "order",
                "slices": [],
                "passengers": []
            }
        }
        response = requests.post(f"{self.BASE_URL}{self.ENDPOINT}", json=payload, headers=self.HEADERS)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("error", response.json())

if __name__ == "__main__":
    unittest.main()