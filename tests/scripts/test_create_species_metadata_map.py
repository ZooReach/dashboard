import unittest
from scripts.create_species_metadata_map import MetaData
from mock import patch, Mock
import requests

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