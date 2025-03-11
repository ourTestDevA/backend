import requests
import unittest

class TestDuffelFlightsAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"

    def test_create_pending_cancellation(self):
        endpoint = f"{self.BASE_URL}/duffel-flights-create-pending-cancellation"
        response = requests.post(endpoint, json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'pending cancellation created'})

if __name__ == "__main__":
    unittest.main()