import unittest
from scripts.create_species_metadata_map import MetaData
from mock import patch, Mock, PropertyMock
import requests
import github

class TestSpeciesMetaData(unittest.TestCase):

    def SetUp(self):
        pass

    @patch("scripts.create_species_metadata_map.get",
           return_value={"result": {"records": [{"name": "spiders"}, {"name": "fishes"}]}})
    def test_get_parent_metadata(self,get):
        metadata = MetaData()
        self.assertEqual({"result": {"records": [{"name": "spiders"}, {"name": "fishes"}]}}, metadata.get_parent_metadata())


    def test_create_visual_metadata_map(self):
        metadata = MetaData()
        species_records =  [
                            {
                                "parent_id": "0",
                                "id": "1",
                                "name": "Spiders"
                            },
                            {
                                "parent_id": "0",
                                "id": "2",
                                "name": "Fishes"
                            }
                            ]
        meta_data = metadata.create_visual_metadata_map(species_records)
        self.assertEqual([{"id": 1, "visual": "Spiders"}, {"id": 2, "visual": "Fishes"}], meta_data)
        
    
    # def test_commit_species_visual_metadata(self):
    #     data = [{'id':1, 'visual':"reptiles"}, {'id':2, 'fishes':'fishes'}]
    #     with patch.object(github, 'Github') as github_mock:
    #         github_mock.get_user = users_mock = Mock()
    #         users_mock.get_repos = repo_mock = Mock(return_value=[{'name':'visual'}])
    #         repo_mock.get_file_contents = file_repo = Mock()
    #         file_repo.update_file = commit_response = Mock()
    #         commit_response.return_value = {"commit": "done", 'content':data}
    #         metadata = MetaData()
    #         response = metadata.commit_species_visual_metadata(data, 'sdfbhrrhewhegvd')
    #         self.assertEqual(response.commit, 'done')
    #         self.assertEqual(response.content, data)
            

