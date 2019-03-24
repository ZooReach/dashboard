from unittest import TestCase
from app.core import services
from mock import patch, Mock


class ServicesTestCase(TestCase):

    @patch("app.core.services.get_visual_files")
    @patch("app.core.services.get_home_page")
    @patch("app.core.services.render_template")
    def test_render_home(self, render_template, get_home_page, get_visual_files):
        render_template.return_value = 'success'
        data = 'returned_value'
        get_home_page.return_value = data
        visual_file = 'visual_file'
        get_visual_files.return_value = visual_file
        envvar = 'ckan'
        services.environment_details['ckan'] = envvar
        self.assertEqual(services.render_home(), 'success')
        get_home_page.assert_called_once()
        render_template.assert_called_once_with('home/home.html', ckan_url=envvar, js_files=visual_file,
                                                json_data=data)

    @patch("app.core.services.split_path")
    @patch("app.core.services.get_parent_details")
    @patch("app.core.services.render_species_details")
    def test_render_category_if_not_parent(self, render_species_details, get_parent_details, split_path):
        get_parent_details.return_value = None
        split_return = 'not_parent_split'
        split_path.return_value = split_return
        render_template_message = 'rendered species details'
        render_species_details.return_value = render_template_message
        path = 'not_parent'
        self.assertEqual(services.render_category(path), render_template_message)
        get_parent_details.assert_called_with(path)
        split_path.assert_called_with(path)
        render_species_details.assert_called_with(['not_parent'])

    @patch("app.core.services.environment_details")
    @patch("app.core.services.get_base_url_till_given_string")
    @patch("app.core.services.get_visual_files")
    @patch("app.core.services.get_category")
    @patch("app.core.services.split_path")
    @patch("app.core.services.get_parent_details")
    @patch("app.core.services.render_template")
    def test_render_category_if_parent(self, render_template, get_parent_details, split_path, get_category,
          get_visual_files, get_base_url_till_given_string, environment_details):
        environment_details.return_value = {'ckan': 'ckanvar'}
        visual_file_return_value = 'visual_file'
        get_visual_files.return_value = visual_file_return_value
        get_base_url_return_value = 'base_url'
        get_base_url_till_given_string.return_value = get_base_url_return_value
        parent_data = {'_id': 1, 'name': 'parent_name', 'id': '2'}
        get_parent_details.return_value = parent_data
        split_path_return_value = 'parent_split'
        split_path.return_value = split_path_return_value
        category_return_value = 'category_data'
        get_category.return_value = category_return_value
        render_template_message = 'parent_rendered'
        render_template.return_value = render_template_message
        path = 'parent'
        self.assertEqual(services.render_category(path), render_template_message)
        get_parent_details.assert_called_with(path)
        split_path.assert_called_with(path)
        get_category.assert_called_with(1, parent_data, 'parent')
        render_template.assert_called_with('category/category.html', ckan_url=environment_details['ckan'],
                                           json_data=category_return_value,
                                           parent_data=parent_data,
                                           parent_name='parent_name',
                                           fullpath=split_path_return_value,
                                           js_files=visual_file_return_value,
                                           base_url=get_base_url_return_value)

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
        self.assertEqual(services.get_category_name(['category', 'fish', 'Eels', 'freshwaterEels']), 'Eels')

    @patch("app.core.services.import_module")
    @patch("app.core.services.split_path")
    def test_get_json(self, split_path, import_module):
        class SampleMockTest(object):
            def main(self):
                return 'hello'

        split_path.return_value = ['data', 'fishes.js']
        import_module.return_value = SampleMockTest()
        import_module.main.return_value = 'hello'
        self.assertEqual(services.get_json('fishes'), 'hello')
