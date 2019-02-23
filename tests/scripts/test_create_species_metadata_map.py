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