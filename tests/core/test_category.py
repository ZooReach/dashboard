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
