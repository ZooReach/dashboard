from unittest import TestCase
from app.core import services
import json
from mock import patch, Mock


class ServicesTestCase(TestCase):

    @patch("app.core.services.render_template")
    def test_render_home(self, render_template):
        render_template.return_value = 'success'
        self.assertEqual(services.render_home(), 'success')


    @patch("app.core.services.getSpeciesDetail")
    @patch("app.core.services.render_template")
    def test_render_species_details(self, render_template, getSpeciesDetail):
        render_template.return_value = 'success'
        getSpeciesDetail.return_value = {'phylum': 'phylumdata', 'class': 'classdata', 'family': 'familydata',
             'redlist_category': 'redlist_category'}
        path = ['fishes', 'anamalia']
        self.assertEqual(services.render_species_details(path), 'success')



    def test_get_species_name(self):
        self.assertEqual(services.get_species_name(['array1', 'array2', 'array3']), 'array3')
        self.assertEqual(services.get_species_name(['array1']), 'array1')

    def test_get_category_name(self):
        self.assertEqual(services.get_category_name(['category','fish','Eels','freshwaterEels']),'Eels')


    @patch("app.core.services.import_module")
    @patch("app.core.services.split_path")
    def test_get_json(self,split_path,import_module):
        class SampleMockTest(object):
            def main(self):
                return 'hello'
        split_path.return_value = ['data','fishes.js']
        import_module.return_value = SampleMockTest()
        import_module.main.return_value = 'hello'
        self.assertEqual(services.get_json('fishes'),'hello')

