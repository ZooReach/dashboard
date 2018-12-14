from unittest import TestCase
from app.core import category


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