import unittest
from app.app import app


class TestIntegrations(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_home_page_renders(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
