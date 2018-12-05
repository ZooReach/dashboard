import unittest

from app.core.file_operations import get_json_file


class AppTestCase(unittest.TestCase):

    def test_client(self):
        self.assertEqual(get_json_file('path'), 'data/path.json')
