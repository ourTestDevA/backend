import requests
import unittest
import time
import hashlib

class HotelbedsIntegrationTests(unittest.TestCase):
    BASE_URL = "http://localhost:5000/hotelbeds-hotels-booking-hotel-availability"
    API_KEY = "HOTELBEDS_HOTEL_API_KEY"
    SECRET = "HOTELBEDS_HOTEL_SECRET"

    def generate_signature(self):
        to_sign = self.API_KEY + self.SECRET + str(int(time.time()))
        hash_object = hashlib.sha256(to_sign.encode())
        return hash_object.hexdigest()

    def test_check_hotel_availability_success(self):
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
            "Api-key": self.API_KEY,
            "X-Signature": self.generate_signature()
        }
        request_body = '{"stay": {"checkIn": "2023-12-20", "checkOut": "2023-12-25"}, "occupancies": [{"rooms": 1, "adults": 2, "children": 0}]}'
        
        response = requests.post(self.BASE_URL, headers=headers, data=request_body)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("hotels", response.json())

    def test_check_hotel_availability_invalid_api_key(self):
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
            "Api-key": "INVALID_API_KEY",
            "X-Signature": self.generate_signature()
        }
        request_body = '{"stay": {"checkIn": "2023-12-20", "checkOut": "2023-12-25"}, "occupancies": [{"rooms": 1, "adults": 2, "children": 0}]}'
        
        response = requests.post(self.BASE_URL, headers=headers, data=request_body)
        
        self.assertEqual(response.status_code, 401)

    def test_check_hotel_availability_gateway_timeout(self):
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
            "Api-key": self.API_KEY,
            "X-Signature": self.generate_signature()
        }
        request_body = '{"stay": {"checkIn": "2023-12-20", "checkOut": "2023-12-25"}, "occupancies": [{"rooms": 1, "adults": 2, "children": 0}]}'
        
        # Simulate a network issue by using an invalid URL
        original_base_url = self.BASE_URL
        self.BASE_URL = "http://localhost:5000/invalid-url"
        
        response = requests.post(self.BASE_URL, headers=headers, data=request_body)
        
        self.assertEqual(response.status_code, 504)
        
        # Restore the original URL
        self.BASE_URL = original_base_url

if __name__ == '__main__':
    unittest.main()