import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app"))
)

from app import get_response


class TestApplication(unittest.TestCase):

    def test_homepage(self):
        status, message = get_response("/")
        self.assertEqual(status, 200)
        self.assertEqual(message, "AI-Assisted DevOps Demo Application")

    def test_health(self):
        status, message = get_response("/health")
        self.assertEqual(status, 200)
        self.assertEqual(message, "OK")

    def test_unknown_route(self):
        status, message = get_response("/unknown")
        self.assertEqual(status, 404)
        self.assertEqual(message, "Not Found")


if __name__ == "__main__":
    unittest.main()
