from unittest import TestCase
from app.core import services
import json
from mock import patch, Mock


class ServicesTestCase(TestCase):

    @patch("app.core.services.get")
    @patch("app.core.services.render_template")
    def test_render_species_details(self, render_template, get):
        render_template.return_value = 'success'
        get.return_value = {'result': {'records': [
            {'phylum': 'phylumdata', 'class': 'classdata', 'family': 'familydata',
             'redlist_category': 'redlist_category'}]}}
        path = ['fishes', 'anamalia']
        self.assertEqual(services.render_species_details(path), 'success')

    @patch("app.core.services.render_template")
    def test_render_home(self, render_template):
        render_template.return_value = 'success'
        self.assertEqual(services.render_home(), 'success')

    def test_form_query_params(self):
        self.assertEqual(services.form_query_params("resource_id_one", "species_one"),
                         {'resource_id': "resource_id_one", 'filters': json.dumps({'species': 'species_one%'}), 'limit': 10})
        self.assertEqual(services.form_query_params("resource_id_one", "species_one", 1),
                         {'resource_id': "resource_id_one", 'filters': json.dumps({'species': "species_one%"}), 'limit': 1})

    def test_get_species_name(self):
        self.assertEqual(services.get_species_name(['array1', 'array2', 'array3']), 'array3')
        self.assertEqual(services.get_species_name(['array1']), 'array1')

    def test_get_array_from_string_path(self):
        self.assertEqual(services.get_array_from_string_path('aaa/bbb/ccc'), ['aaa', 'bbb', 'ccc'])
        self.assertEqual(services.get_array_from_string_path('aaa'), ['aaa'])


    @patch("app.core.services.import_module")
    @patch("app.core.services.get_array_from_string_path")
    def test_get_json(self,get_array_from_string_path,import_module):
        class SampleMockTest(object):
            def main(self):
                return 'hello'
        get_array_from_string_path.return_value = ['data','fishes.js']
        import_module.return_value = SampleMockTest()
        import_module.main.return_value = 'hello'
        self.assertEqual(services.get_json('fishes'),'hello')

