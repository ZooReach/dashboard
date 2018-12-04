from app import app
import unittest


class AppTestCase(unittest.TestCase):

    def test_client(self):
        self.assertEqual(app.get_json_file('path'), 'data/path.json')
