from app import app
import unittest


class AppTestCase(unittest.TestCase):

    def test_client(self):
        self.assertEqual(app.getJsonFile('path'), 'data/path.json')
