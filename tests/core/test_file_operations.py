from unittest import TestCase
from mock import patch
from app.core import file_operations as file


class FileOperationTestCase(TestCase):

    @patch("app.core.file_operations.get_os_directory")
    def test_get_json_file_path_from_data(self, os_dir):
        os_dir.return_value = "dir"
        self.assertEqual(file.get_json_file_path_from_data('path'), 'dir/data/path.json')
        self.assertEqual(file.get_json_file_path_from_data('append'), 'dir/data/append.json')

    @patch("os.path.dirname")
    def test_get_os_directory(self, dirname):
        dirname.return_value = "dir"
        self.assertEqual(file.get_os_directory(), "dir")

    @patch("os.path.isdir")
    @patch("os.listdir")
    def test_list_dir(self, listdir, isdir):
        isdir.return_value = True
        listdir.return_value = ["directory"]
        self.assertEqual(file.list_dir("directory"), ["directory"])

        isdir.return_value = False
        self.assertEqual(file.list_dir("directory"), [])

    @patch("app.core.file_operations.get_os_directory")
    @patch("app.core.file_operations.get_visual_map_from_db")
    def test_get_visual_files(self, get_visual_map_from_db, os_dir):
        get_visual_map_from_db.return_value = ["dir1", "dir2", "dir3"]
        os_dir.return_value = "dir"
        self.assertEqual(file.get_visual_files("fishes"),
                         ["js/visualization/dir1", "js/visualization/dir2", "js/visualization/dir3"])

    @patch("json.load")
    def test_update_json(self, json_load):
        json_load.return_value = {"type": {"key": "value"}}
        self.assertEqual(file.update_json({}, "somefile"), {"key": "value"})
