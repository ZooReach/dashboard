from unittest import TestCase
from app.core import species_repository
from app.utils.constants import meta_data_resource_id
from mock import patch,Mock


class RepositoryTestCase(TestCase):


    @patch("app.core.species_repository.get",return_value={"result":{"records":[{"resource_id":"resource123"}]}})
    def test_get_resource_id_by_name(self,get):
        resource_id =species_repository.get_resource_id_by_name("fishes")
        self.assertEqual("resource123",resource_id)

    @patch("app.core.species_repository.get", return_value={"result": {"records": []}})
    def test_get_resource_id_by_name_should_return_none(self, get):
        resource_id = species_repository.get_resource_id_by_name("fishes")
        self.assertEqual(None, resource_id)

    def test_query_to_get_resourceid(self):
        query = 'select resource_id from "' + meta_data_resource_id + '" where name' + "='fish'"
        expected_query_param = {"sql": query}
        result = species_repository.query_to_get_resourceid('fish')
        self.assertEqual(expected_query_param,result)

    # def test_frame_select_query_to_list_category_without_filter_condition(self):
    #     expected = 'SELECT _id,name,kingdom,description,image,parent_id from "12345"'
    #     actual = species_repository.frame_select_query_to_list_category('12345','')
    #     self.assertEqual(expected,actual)

    # def test_frame_select_query_to_list_category_with_filter_condition(self):
    #     expected = 'SELECT _id,name,kingdom,description,image,parent_id from "12345" WHERE'+ " name='fish'"
    #     actual = species_repository.frame_select_query_to_list_category('12345', "name='fish'")
    #     self.assertEqual(expected, actual)

    @patch("app.core.species_repository.get", return_value={"result": {"records": [{"resource_id": "resource123"},{"resource_id": "resource1234"}]}})
    def test_get_parent_details(self,get):
        actual = species_repository.get_parent_details('Fish')
        self.assertEqual({"resource_id": "resource123"},actual)

    @patch("app.core.species_repository.get", return_value={"result": {"records": []}})
    def test_get_parent_details(self,get):
        actual = species_repository.get_parent_details('Fish')
        self.assertEqual(None,actual)

    def test_filtercondition_home_page(self):
        self.assertEqual("parent_id = 0",species_repository.filtercondition_home_page())

    @patch("app.core.species_repository.get",
           return_value={"result": {"records": [{"resource_id": "resource123"}, {"resource_id": "resource1234"}]}})
    def test_get_home_page_data(self,get):
        expected = [{"resource_id": "resource123"}, {"resource_id": "resource1234"}]
        self.assertEqual(expected,species_repository.get_home_page_data())

    def test_parent_id_query(self):
        self.assertEqual("parent_id =1",species_repository.parent_id_query(1))

    def test_query_for_resource_id_from(self):
        query = 'select resource_id from "' + meta_data_resource_id + '" where _id=123'
        query_param = {"sql": query}
        self.assertEqual(query_param,species_repository.query_for_resource_id_from('123'))

    def test_get_category_list_sql_condition_ckan(self):
        name= 'Freshwater Eels'
        self.assertEqual('category_level2'+"='" + name + "'",species_repository.get_category_list_sql_condition_ckan({"name":name}))

    def test_frame_select_query_to_list_species(self):
        query = 'SELECT species,kingdom,genus from "123" WHERE name="fish"'
        self.assertEqual(query,species_repository.frame_select_query_to_list_species('123','name="fish"'))

    @patch("app.core.species_repository.get",
           return_value={"result": {"records": [{"resource_id": "resource123"}, {"resource_id": "resource1234"}]}})
    def test_getSpeciesDetail(self,get):
        self.assertEqual({"resource_id": "resource123"},species_repository.getSpeciesDetail('',''))

    def test_form_query_params(self):
        query = 'SELECT * from "resource_id_one" WHERE species LIKE '
        query += "'species_one%'"
        expected = {"sql": query}
        self.assertEqual(expected,species_repository.form_species_query("resource_id_one", "species_one"))
