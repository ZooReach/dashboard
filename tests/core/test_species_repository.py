from unittest import TestCase
from app.core import species_repository
from app.utils.constants import meta_data_resource_id
from mock import patch, Mock


class RepositoryTestCase(TestCase):

    @patch("app.core.species_repository.get_data_from_ckan",
           return_value={"result": {"records": [{"resource_id": "resource123"}]}})
    def test_get_resource_id_by_name(self, get_data_from_ckan):
        resource_id = species_repository.get_resource_id_by_name("fishes")
        self.assertEqual("resource123", resource_id)

    @patch("app.core.species_repository.get_data_from_ckan", return_value={"result": {"records": []}})
    def test_get_resource_id_by_name_should_return_none(self, get_data_from_ckan):
        resource_id = species_repository.get_resource_id_by_name("fishes")
        self.assertEqual(None, resource_id)

    @patch("app.core.species_repository.get_data_from_ckan",
           return_value={"result": {"records": [{"resource_id": "resource123"}, {"resource_id": "resource1234"}]}})
    def test_get_parent_details(self, get):
        actual = species_repository.get_parent_details('Fish')
        self.assertEqual({"resource_id": "resource123"}, actual)

    @patch("app.core.species_repository.get_data_from_ckan", return_value={"result": {"records": []}})
    def test_get_parent_details(self, get):
        actual = species_repository.get_parent_details('Fish')
        self.assertEqual(None, actual)

    @patch("app.core.species_repository.get_data_from_ckan",
           return_value={"result": {"records": [{"resource_id": "resource123"}, {"resource_id": "resource1234"}]}})
    def test_get_home_page_data(self, get):
        expected = [{"resource_id": "resource123"}, {"resource_id": "resource1234"}]
        self.assertEqual(expected, species_repository.get_home_page_data())

    @patch("app.core.species_repository.get_data_from_ckan",
           return_value={"result": {"records": [{"resource_id": "resource123"}, {"resource_id": "resource1234"}]}})
    def test_getSpeciesDetail(self, get):
        self.assertEqual({"resource_id": "resource123"}, species_repository.getSpeciesDetail('', ''))

    def test_form_query_params(self):
        query = 'query WHERE species LIKE '
        query += "'species_one%'"
        self.assertEqual(query, species_repository.form_species_query("query", "species_one"))

    @patch("app.core.species_repository.get_data_from_ckan")
    def test_get_data_from_ckan(self, get_data_from_ckan):
        ckan_data = {"key": "success"}
        get_data_from_ckan.return_value = ckan_data
        call_parameter = "sql query"
        self.assertEqual(species_repository.get_data_from_ckan(call_parameter), ckan_data)
        get_data_from_ckan.assert_called_with(call_parameter)

    def test_form_sql_query_when_only_select_parameter_passed(self):
        resource_id = "resource_id"
        expected = 'select id,name,desc from \"' + resource_id + '\"'
        actual = species_repository.form_sql_query(resource_id=resource_id, select_parameters=['id', 'name', 'desc'])
        self.assertEqual(actual, expected)

    def test_form_sql_query_when_condition_is_passed(self):
        resource_id = "resource_id"
        expected = "select id,name,desc from \"" + resource_id + "\" where id=123 and name='aaa'"
        actual = species_repository.form_sql_query(resource_id=resource_id, select_parameters=['id', 'name', 'desc'],
                                                   condition={'id': 123, 'name': 'aaa'})
        self.assertEqual(actual, expected)

    @patch("app.core.species_repository.form_sql_query")
    def test_form_sql_query_with_meta_data_table(self, form_sql_query):
        success_return_value = "success"
        meta_resource_id = "meta_resource_id"
        species_repository.meta_data_resource_id = meta_resource_id
        form_sql_query.return_value = success_return_value
        selected_parameters = "selected_parameters"
        condition = "condition"
        self.assertEqual(species_repository.form_sql_query_with_meta_data_table(select_parameters=selected_parameters,
                                                                                condition=condition),
                         success_return_value)
        form_sql_query.assert_called_once_with(resource_id=meta_resource_id, select_parameters=selected_parameters,
                                               condition=condition)

    def test_get_result_record(self):
        data = {'result': {'records': 'success_value'}}
        self.assertEqual(species_repository.get_result_record(data), 'success_value')
