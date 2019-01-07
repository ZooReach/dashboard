from unittest import TestCase
from app.core import category
from mock import patch, Mock

class CategoryTestCase(TestCase):

    @patch("app.core.category.get_category_data",return_value=[{"Name":"FreshwaterFish"},{"Name":"SaltwaterFish"}])
    def test_get_category(self,getcategory_data):
        result = category.get_category('0',{})
        self.assertEqual([{"Name":"FreshwaterFish"},{"Name":"SaltwaterFish"}],result)

    @patch("app.core.category.get_category_data")
    @patch("app.core.category.get_species_data")
    def test_get_category(self,get_species_data, get_category_data):
        get_species_data.return_value = [{"species": "tigerFish","genus":"animalia","type": {},"kingdom":"Kingdom","image": "images/placeholder.svg"}]
        get_category_data.return_value = []
        result = category.get_category('0', {})
        self.assertEqual([{"name": "tigerFish","genus":"animalia","type": {},"kingdom":"Kingdom","image": "images/placeholder.svg"}], result)

