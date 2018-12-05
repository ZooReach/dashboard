from app.core import file_operations as file
import unittest


class AppTestCase(unittest.TestCase):

    def test_client(self):
        self.assertEqual(file.get_json_file('path'), 'data/path.json')
