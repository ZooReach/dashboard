from ..utils.rest_client import get
from ..utils.constants import api, meta_data_resource_id, visual_resource_id


def get_data_from_ckan(queryparams):
    return get(url=api['datastore_search_sql'], queryparams={"sql": queryparams})


def form_sql_query(resource_id, select_parameters, condition=None):
    main_statement = 'select ' + ','.join(str(name) for name in select_parameters) + ' from ' + '"{}"'.format(
        resource_id)
    if condition:
        return main_statement + ' where ' + ' and '.join('='.join(
            [key, (str(value) if isinstance(value, int) else "'{}'".format(value))]) for key, value in
                                                         condition.items())
    return main_statement


def form_sql_query_with_meta_data_table(select_parameters, condition=None):
    return form_sql_query(resource_id=meta_data_resource_id, select_parameters=select_parameters, condition=condition)


def form_sql_query_with_visual_table(select_parameters, condition=None):
    return form_sql_query(resource_id=visual_resource_id, select_parameters=select_parameters, condition=condition)


def get_resource_id_by_name(name):
    response = get_data_from_ckan(
        form_sql_query_with_meta_data_table(select_parameters=['resource_id'], condition={'name': name}))
    return validateAndExtractResult(response)


def validateAndExtractResult(response):
    if len(response['result']['records']) > 0:
        return response['result']['records'][0]['resource_id']
    else:
        return None


def get_parent_details(parent_name):
    response = get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'name': parent_name}))
    if len(response['result']['records']) > 0:
        return response['result']['records'][0]
    else:
        return None


def get_visual_data(id):
    response = get_data_from_ckan(
        form_sql_query_with_visual_table(select_parameters=['visual'], condition={'metadata_id': id}))
    return list(map(lambda x: x['visual'], response['result']['records']))


def get_home_page_data():
    response = get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'parent_id': 0}))
    return response['result']['records']


def get_category_data(parent_id):
    response = get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'parent_id': str(parent_id)}))
    return response['result']['records']


def get_species_data(parent_data):
    resource_id = get_resource_id_ckan(parent_data['_id'])
    response = get_data_from_ckan(
        form_sql_query(resource_id=resource_id, select_parameters=['species', 'kingdom', 'genus'],
                       condition={'category_level2': parent_data['name']}))
    return response['result']['records']


def get_resource_id_ckan(id):
    response = get_data_from_ckan(
        form_sql_query_with_meta_data_table(select_parameters=['resource_id'], condition={'_id': id}))
    return validateAndExtractResult(response)


def form_species_query(query, species_name):
    query = query + ' WHERE species LIKE ' + "'" + species_name + "%'"
    return query


def getSpeciesDetail(category_name, species_name):
    raw_query = form_sql_query(resource_id=get_resource_id_by_name(category_name), select_parameters=['*'])
    response = get_data_from_ckan(
        form_species_query(raw_query, species_name))
    species_record = response['result']['records'][0]
    return species_record


def form_species_query(resource_id, species_name):
    query = 'SELECT * from "' + resource_id + '"'
    query = query + ' WHERE species LIKE ' + "'" + species_name + "%'"
    return query


def get_all_species_details():
    url = api.get('datastore_search_sql', '')
    query = 'select * from "' + meta_data_resource_id + '"'
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    return response["result"]["records"]
    


