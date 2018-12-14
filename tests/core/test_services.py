from unittest import TestCase
from app.core import services
from mock import patch


class ServicesTestCase(TestCase):

    @patch("app.core.services.get")
    @patch("app.core.services.render_template")
    def test_render_species_details(self, render_template, get):
        render_template.return_value = 'success'
        get.return_value = {'result':{'records':[{'phylum':'phylumdata','class':'classdata','family':'familydata','redlist_category':'redlist_category'}]}}
        path = ['bats', 'anamalia']
        self.assertEqual(services.render_species_details(path), 'success')

    @patch("app.core.services.render_template")
    @patch("app.core.services.get_species_from_path")
    @patch("app.core.services.get_json_file")
    @patch("app.core.services.get_base_url_till_given_string")
    def test_render_category(self, base_url_till_given_string, get_json_file, get_species_from_path, render_template):
        base_url_till_given_string.return_value = 'http://localhost:5000/category/'
        get_json_file.return_value = {
            "type": {
                "category1": {
                    "type": {}}}}
        filename = 'category1'
        get_species_from_path.return_value = ''
        render_template.return_value = 'success'
        self.assertEqual(services.render_category(filename), 'success')

    @patch("app.core.services.render_template")
    def test_render_home(self, render_template):
        render_template.return_value = 'success'
        self.assertEqual(services.render_home(), 'success')
