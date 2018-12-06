import unittest
from mock import patch
from app.core import file_operations as file


class FileOperationTestCase(unittest.TestCase):

    def test_get_json_file(self):
        self.assertEqual(file.get_json_file_path_from_data('path'), 'data/path.json')
        self.assertEqual(file.get_json_file_path_from_data('append'), 'data/append.json')

    def test_append_files(self):
        self.assertEqual(file.append_files([], "filename", "files"), ['filename/files'])
        self.assertEqual(file.append_files(["file1"], "file2", "file"), ['file1', 'file2/file'])

    @patch("os.path.isdir")
    @patch("os.listdir")
    def test_list_dir(self, listdir, isdir):
        isdir.return_value = True
        listdir.return_value = ["directory"]
        self.assertEqual(file.list_dir("directory"), ["directory"])

        isdir.return_value = False
        self.assertEqual(file.list_dir("directory"), [])

    @patch("app.core.file_operations.list_dir")
    def test_hello(self, list_dir):
        list_dir.return_value = ["dir1", "dir2", "dir3"]
        self.assertEqual(file.get_visual_files("filename"), ["filename/dir1", "filename/dir2", "filename/dir3"])

    @patch("json.load")
    def test_update_json(self, json_load):
        json_load.return_value = {"type": {"key": "value"}}
        self.assertEqual(file.update_json({}, "somefile"), {"key": "value"})

    def test_client(self):
        self.assertEqual(file.get_json_file_path_from_data('path'), 'data/path.json')
