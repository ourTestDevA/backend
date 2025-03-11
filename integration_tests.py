import requests
import os
import unittest
from unittest.mock import patch

class TestDuffelFlightsAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    ENDPOINT = "/duffel-flights-list-offers"

    @patch.dict(os.environ, {"DUFFEL_API_KEY": "test_api_key"})
    def test_post_duffel_flights_list_offers_success(self):
        payload = {
            "slices": [
                {
                    "origin": "LHR",
                    "destination": "JFK",
                    "departure_date": "2023-12-01"
                }
            ],
            "passengers": [
                {
                    "type": "adult"
                }
            ]
        }
        response = requests.post(f"{self.BASE_URL}{self.ENDPOINT}", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", response.json())

    @patch.dict(os.environ, {"DUFFEL_API_KEY": "test_api_key"})
    def test_post_duffel_flights_list_offers_invalid_request(self):
        payload = {
            "slices": [
                {
                    "origin": "LHR",
                    "destination": "JFK"
                    # Missing departure_date
                }
            ],
            "passengers": [
                {
                    "type": "adult"
                }
            ]
        }
        response = requests.post(f"{self.BASE_URL}{self.ENDPOINT}", json=payload)
        self.assertEqual(response.status_code, 400)

    @patch.dict(os.environ, {"DUFFEL_API_KEY": ""})
    def test_post_duffel_flights_list_offers_unauthorized(self):
        payload = {
            "slices": [
                {
                    "origin": "LHR",
                    "destination": "JFK",
                    "departure_date": "2023-12-01"
                }
            ],
            "passengers": [
                {
                    "type": "adult"
                }
            ]
        }
        response = requests.post(f"{self.BASE_URL}{self.ENDPOINT}", json=payload)
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()