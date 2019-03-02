from ..utils.rest_client import get
from ..utils.constants import api, meta_data_resource_id


def get_data_from_ckan(queryparams):
    return get(url=api['datastore_search_sql'], queryparams={"sql": queryparams})


def form_sql_query_with_meta_data_table(select_parameters, condition=None):
    main_statement = 'select ' + ','.join(str(name) for name in select_parameters) + ' from ' + meta_data_resource_id
    if condition:
        return main_statement + ' where ' + ' and '.join('='.join(
            [key, (str(value) if isinstance(value, int) else '"{}"'.format(value))]) for key, value in
                                                         condition.items())
    return main_statement


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
    filter_condition = "name='" + parent_name + "'"
    query = frame_select_query_to_list_category(meta_data_resource_id, filter_condition)
    response = get_data_from_ckan(query)
    if len(response['result']['records']) > 0:
        return response['result']['records'][0]
    else:
        return None


def get_visual_data(id):
    filter_condition = "metadata_id='" + id + "'"
    query = frame_visual_query('847896c8-ad47-4bf7-a5e0-05c2c41d0c64', filter_condition)
    response = get_data_from_ckan(query)
    return list(map(lambda x: x['visual'], response['result']['records']))


def get_home_page_data():
    response = get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'parent_id': '0'}))
    return response['result']['records']


def get_category_data(parent_id):
    response = get_data_from_ckan(form_sql_query_with_meta_data_table(
        select_parameters=['_id', 'id', 'name', 'kingdom', 'description', 'image', 'parent_id'],
        condition={'parent_id': str(parent_id)}))
    return response['result']['records']


def frame_select_query_to_list_category(resource_id, filter_condition):
    query = 'SELECT _id,id,name,kingdom,description,image,parent_id from "' + resource_id + '"'
    if filter_condition is not '':
        query = query + ' WHERE ' + filter_condition
    return query


def frame_visual_query(resource_id, filter_condition):
    query = 'SELECT visual from "' + resource_id + '"'
    if filter_condition is not '':
        query = query + ' WHERE ' + filter_condition
    return query


def get_species_data(parent_data):
    resource_id = get_resource_id_ckan(parent_data['_id'])
    filter_condition = get_category_list_sql_condition_ckan(parent_data)
    query = frame_select_query_to_list_species(resource_id, filter_condition)
    response = get_data_from_ckan(query)
    return response['result']['records']


def get_resource_id_ckan(id):
    query_param = query_for_resource_id_from(id)
    response = get_data_from_ckan(query_param)
    return validateAndExtractResult(response)


def query_for_resource_id_from(id):
    query = 'select resource_id from "' + meta_data_resource_id + '" where _id=' + str(id)
    return query


def get_category_list_sql_condition_ckan(parent_data):
    name = parent_data['name']
    return 'category_level2' + "='" + name + "'"


def frame_select_query_to_list_species(resource_id, filter_condition):
    query = 'SELECT species,kingdom,genus from "' + resource_id + '"'
    if filter_condition is not '':
        query = query + ' WHERE ' + filter_condition
    return query


def getSpeciesDetail(category_name, species_name):
    response = get_data_from_ckan(form_species_query(resource_id=get_resource_id_by_name(category_name),
                                                     species_name=species_name))
    species_record = response['result']['records'][0]
    return species_record


def form_species_query(resource_id, species_name):
    query = 'SELECT * from "' + resource_id + '"'
    query = query + ' WHERE species LIKE ' + "'" + species_name + "%'"
    return query
