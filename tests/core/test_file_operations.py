import unittest
from app.core import file_operations as file


class FileOperationTestCase(unittest.TestCase):

    def test_get_json_file(self):
        self.assertEqual(file.get_json_file('path'), 'data/path.json')
        self.assertEqual(file.get_json_file('append'), 'data/append.json')

    def test_append_files(self):
        self.assertEqual(file.append_files([], "filename", "files"), ['filename/files'])
        self.assertEqual(file.append_files(["file1"], "file2", "file"), ['file1', 'file2/file'])


    def test_client(self):
        self.assertEqual(file.get_json_file_path_from_data('path'), 'data/path.json')
