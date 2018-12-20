from unittest import TestCase
from app.core import category
from mock import patch, Mock

class CategoryTestCase(TestCase):
    def test_get_categories_json(self):
        path = ['bats', 'fruit']
        json_data = {'type': {'bats': {'type': {'fruit': {'name': 'hello'}}}}}
        actual = category.get_categories_json(path, json_data)
        self.assertEqual(actual, {'name': 'hello'})

    def test_get_species_from_path_with_type(self):
        category_type = {
            "type": {
                "category1": {
                    "type": {}}}}
        path = ['category1']
        self.assertEqual(category.get_species_from_path(category_type, path), '')

    def test_get_species_from_path_without_type(self):
        category_type = {
            "type": {
                "category1": {}}}
        path = ['category1', 'species']
        species = ['species']
        self.assertEqual(category.get_species_from_path(category_type, path), species)

    def test_get_category_list_sql_condition(self):
        path = ['bats','fruit_eating','large']
        expected = "category_level1='fruit_eating' AND category_level2='large'"
        self.assertEqual(category.get_category_list_sql_condition(path),expected)


    def test_frame_select_query_to_list_species_with_filter_query(self):
        filter_query = "category_level1='fruit_eating' AND category_level2='large'"
        expected = 'SELECT species,kingdom from "1234" WHERE '+filter_query
        self.assertEqual(category.frame_select_query_to_list_species('1234',filter_query),expected)

    def test_frame_select_query_to_list_species_without_filter_query(self):
        expected = 'SELECT species,kingdom from "1234"'
        self.assertEqual(category.frame_select_query_to_list_species('1234',''),expected)

    @patch("app.core.category.get_categories_json")
    def test_get_category(self,get_categories_json):
        json_data = {'Name':'Fish','type':{'Eels' : {'type':{ 'Eels1':{'Name':'Eels1'}}
            ,'Eels2':{'Name':'Eels2'}}}}
        get_categories_json.return_value = json_data
        path=['category','fish','Eels']
        self.assertEqual(category.get_category(path,json_data),json_data)

    @patch("app.core.category.get_species_list")
    @patch("app.core.category.get_categories_json")
    def test_get_category(self,get_categories_json,get_species_list):
        json_data = {'Name':'Eels', 'type':{ 'Eels1':{'Name':'Eels'}}}
        species = {"pop fish":{"Name":"pop fish"}}
        get_categories_json.return_value = json_data
        get_species_list.return_value = species
        path=['fishes','Eels']
        result = {'Name':'Eels', 'type':{ 'Eels1':{'Name':'Eels','type':species}}}
        result_actual = category.get_category(path,json_data)
        self.assertEqual(result_actual,result)