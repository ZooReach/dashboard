from ..utils.rest_client import get
from ..utils.constants import api, meta_data_resource_id, visual_resource_id, experts_resource_id


def get_data_from_ckan(queryparams):
    return get(url=api['datastore_search_sql'],
               queryparams={"sql": queryparams})


def get_result_record(map):
    return map['result']['records']


def form_sql_query(resource_id, select_parameters, condition=None):
    main_statement = 'select ' + ','.join(str(name) for name in select_parameters) + ' from ' + '"{}"'.format(
        resource_id)
    if condition:
        return main_statement + ' where ' + ' and '.join('='.join(
            [key, (str(value) if isinstance(value, int) else "'{}'".format(value))]) for key, value in
                                                         condition.items())
    return main_statement


def form_sql_query_with_meta_data_table(select_parameters, condition=None):
    return form_sql_query(resource_id=meta_data_resource_id,
                          select_parameters=select_parameters,
                          condition=condition)


def form_sql_query_with_visual_table(select_parameters, condition=None):
    return form_sql_query(resource_id=visual_resource_id,
                          select_parameters=select_parameters,
                          condition=condition)


def get_resource_id_by_name(name):
    return validateAndExtractResult(get_data_from_ckan(
        form_sql_query_with_meta_data_table(select_parameters=['resource_id'],
                                            condition={'name': name})))


def validateAndExtractResult(response):
    if len(get_result_record(response)) > 0:
        return get_result_record(response)[0]['resource_id']
    return None


def get_parent_details(parent_name):
    response = get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'name': parent_name}))
    if len(get_result_record(response)) > 0:
        return get_result_record(response)[0]
    return None


def get_visual_data(id):
    return list(map(lambda x: x['visual'], get_result_record(get_data_from_ckan(
        form_sql_query_with_visual_table(select_parameters=['visual'],
                                         condition={'metadata_id': str(id)})))))


def get_home_page_data():
    return get_result_record(get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'parent_id': 0})))


def get_category_data(parent_id):
    return get_result_record(get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'parent_id': str(parent_id)})))


def get_species_data(immediate_parent_data, grand_parent):
    return get_result_record(get_data_from_ckan(
        form_sql_query(resource_id=get_resource_id_ckan(grand_parent),
                       select_parameters=['species', 'kingdom', 'genus'],
                       condition={'category_level2': immediate_parent_data['name']})))


def get_resource_id_ckan(name):
    return validateAndExtractResult(get_data_from_ckan(
        form_sql_query_with_meta_data_table(select_parameters=['resource_id'],
                                            condition={'name': name})))


def form_species_query(query, species_name):
    return (query + ' WHERE species LIKE ' + "'" + species_name + "%'")


def getSpeciesDetail(parent, species_name):
    return get_result_record(get_data_from_ckan(
        form_species_query(form_sql_query(resource_id=get_resource_id_by_name(parent),
                                          select_parameters=['*']),
                           species_name)))[0]


def get_all_species_details():
    return get_result_record(
        get_data_from_ckan(form_sql_query(resource_id=meta_data_resource_id, select_parameters=['*'])))


def get_species_experts_data(parent_id):
    return get_result_record(get_data_from_ckan(form_sql_query(resource_id=experts_resource_id, select_parameters=[
        'first_name', 'last_name', 'email', 'affiliation', 'tags'
    ], condition={'metadata_id': parent_id})))
