## run this file with command 'python -m tests.scripts.test_visual_metadata_db_dump' ##

from unittest import TestCase, main
from scripts.visual_metadata_db_dump import VisualMetaData, read_visual_metadata_map
from mock import patch, Mock
import requests

class TestVisualMetadataTest(TestCase):
    
    def setUp(self):
        self.species_list = [
                        {
                            "id":1,
                            "visual":"spiders"
                        },
                        {
                            "id":2,
                            "visual":"fishes"
                        },
                        {
                            "id":258,
                            "visual":"primates"
                        }]
        self.visual_metadata = VisualMetaData(self.species_list)


    def test_read_visual_metadat_map(self):
        with patch.object(requests, 'get') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = self.species_list
            response = read_visual_metadata_map(get_mock)
            self.assertEqual(response.text, self.species_list)
            self.assertEqual(response.status_code, 200)


    def test_delete_visual_metadata(self):
        with patch.object(requests, 'post') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.success = True
            response = self.visual_metadata.delete_visual_metadata()
            self.assertTrue(response.success)
            self.assertEqual(response.status_code, 200)    


    def test_insert_visual_metadata(self):
        with patch.object(requests, 'post') as get_mock:
            get_mock.return_value = mock_response = Mock()
            mock_response.status_code = 200
            mock_response.success = True
            response = self.visual_metadata.insert_visual_metadata()
            self.assertTrue(response.success)
            self.assertEqual(response.status_code, 200) 


    def test_get_species_data(self):
        records = [
                    {
                    "id":1,
                    "metadata_id":1,
                    "visual":"spiders"
                    },
                    {
                        "id":2,
                        "metadata_id":2,
                        "visual":"fishes"
                    },
                    {
                        "id":3,
                        "metadata_id":258,
                        "visual":"primates"
                    }]
        results =  self.visual_metadata.get_species_data()
        self.assertEqual(results, records)           
        

if __name__ == '__main__':
    main()
