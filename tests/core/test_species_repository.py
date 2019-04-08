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


    @patch("app.core.species_repository.form_sql_query",
           return_value="select id, name, resource_id from resourceId123")
    def test_form_sql_query_with_visual_table(self, form_sql_query):
        result = species_repository.form_sql_query_with_visual_table(['id', 'name', 'resource_id'])
        self.assertEqual("select id, name, resource_id from resourceId123", result)


    @patch("app.core.species_repository.form_sql_query_with_visual_table")
    @patch("app.core.species_repository.get_data_from_ckan")
    @patch("app.core.species_repository.get_result_record")
    def test_get_visual_data(self, get_result_record, get_data_from_ckan, form_sql_query_with_visual_table):
        form_sql_query_with_visual_table.return_value = "select * from visual_table"
        get_data_from_ckan.return_value = {"result":{"record":[{"id":1, "meta_data_id":2, "visual":"fishes"}]}}
        get_result_record.return_value = [{"id":1, "meta_data_id":2, "visual":"fishes"}]
        result = species_repository.get_visual_data(1)
        self.assertEqual(result, ["fishes"])


    @patch("app.core.species_repository.form_sql_query_with_visual_table")
    @patch("app.core.species_repository.get_data_from_ckan")
    @patch("app.core.species_repository.get_result_record")
    def test_get_all_visual_data_files(self, get_result_record, get_data_from_ckan, form_sql_query_with_visual_table):
        form_sql_query_with_visual_table.return_value = "select * from visual_table"
        get_data_from_ckan.return_value = {"result":{"record":[{"id":1, "meta_data_id":2, "visual":"fishes"}]}}
        get_result_record.return_value = [{"id":1, "meta_data_id":2, "visual":"fishes"}]
        result = species_repository.get_all_visual_data_files()
        self.assertEqual(result, ["fishes"])


    @patch("app.core.species_repository.form_sql_query_with_visual_table")
    @patch("app.core.species_repository.get_data_from_ckan")
    @patch("app.core.species_repository.get_result_record")
    def test_get_category_data(self, get_result_record, get_data_from_ckan, form_sql_query_with_visual_table):
        form_sql_query_with_visual_table.return_value = "select * from metadata_table"
        get_data_from_ckan.return_value = {"result":{"record":[{"id":1, "resource_id":2, "name":"fishes"}]}}
        get_result_record.return_value = [{"id":1, "resource_id":2, "name":"fishes"}]
        result = species_repository.get_category_data(0)
        self.assertEqual(result, [{"id":1, "resource_id":2, "name":"fishes"}])


    @patch("app.core.species_repository.get_resource_id_ckan")
    @patch("app.core.species_repository.form_sql_query")
    @patch("app.core.species_repository.get_data_from_ckan")
    @patch("app.core.species_repository.get_result_record")    
    def test_get_species_data(self, get_result_record, get_data_from_ckan, form_sql_query, get_resource_id_ckan):
        get_resource_id_ckan.return_value = 123
        form_sql_query.return_value = "select species, kingdom, genus from species_table"
        get_data_from_ckan.return_value = {"result":{"record":[{"species":"some", "kingdom":"any", "genus":"any"}]}}
        get_result_record.return_value = [{"species":"some", "kingdom":"any", "genus":"any"}]
        result = species_repository.get_species_data({"name":"fishes"}, 0)
        self.assertEqual(result, [{"species":"some", "kingdom":"any", "genus":"any"}])


    @patch("app.core.species_repository.validateAndExtractResult")
    @patch("app.core.species_repository.get_data_from_ckan")
    @patch("app.core.species_repository.form_sql_query_with_meta_data_table")
    def test_get_resource_id_ckan(self, form_sql_query_with_meta_data_table, get_data_from_ckan, validateAndExtractResult):
        form_sql_query_with_meta_data_table.return_value = "select * from metadata_table"
        get_data_from_ckan.return_value = {"result":{"record":[{"id":1, "resource_id":2, "name":"fishes"}]}}
        validateAndExtractResult.return_value = 2
        result = species_repository.get_resource_id_ckan("fishes")
        self.assertEqual(result, 2)