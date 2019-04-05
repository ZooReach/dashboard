from unittest import TestCase
from mock import patch, Mock
from app.core import file_operations as file
import mock



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
                         ["js/visualization/dir1.js", "js/visualization/dir2.js", "js/visualization/dir3.js"])


    @patch("app.core.file_operations.get_all_visual_data_files")
    def test_get_all_visual_chart_files(self, get_all_visual_data_files):
        get_all_visual_data_files.return_value = ['test', 'fishes', 'spiders', 'demo']
        self.assertEqual(file.get_all_visual_chart_files(), 
        ["js/visualization/test.js", "js/visualization/fishes.js", "js/visualization/spiders.js", "js/visualization/demo.js"])


    def test_get_visual_file(self):
        self.assertEqual(file.get_visual_file('fishes'), ["js/visualization/fishes.js"])


    @patch("json.load")
    @patch("app.core.file_operations.open", create=True)
    def test_get_json_file(self, mock_open, json_load):
        mock_open.side_effect = [
            mock.mock_open(read_data='{"fishes":0, "demo":1}').return_value
        ]
        json_load.return_value = {"fishes":0, "demo":1}
        self.assertEqual({"fishes":0, "demo":1}, file.get_json_file("fileA"))
        

    @patch("json.load")
    def test_update_json(self, json_load):
        json_load.return_value = {"type": {"key": "value"}}
        self.assertEqual(file.update_json({}, "somefile"), {"key": "value"})


    @patch("app.core.file_operations.update_json")
    @patch("app.core.file_operations.open", create=True)
    def test_update_json_from_file(self, mock_open, update_json):
        update_json.return_value = {"key":"value"}
        mock_open.side_effect = [
            mock.mock_open(read_data={"type":{"key":"value"}}).return_value
        ]
        self.assertEqual(file.update_json_from_file({}, 'test', "x.txt"), {"key":"value"})


    @patch("app.core.file_operations.get_visual_data")
    def test_get_visual_map_from_db(self, get_visual_data):
        visual_response = ['visual1', 'visual2']
        get_visual_data.return_value = visual_response
        self.assertEqual(file.get_visual_map_from_db(1), visual_response)
        get_visual_data.assert_called_with(1)
