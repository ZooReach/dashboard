from ..utils.rest_client import get
from ..utils.constants import api, meta_data_resource_id


def get_resource_id_by_name(name):
    url = api['datastore_search_sql']
    query_param = query_to_get_resourceid(name)
    response = get(url=url, queryparams=query_param)
    return validateAndExtractResult(response)


def query_to_get_resourceid(name):
    query = 'select resource_id from "' + meta_data_resource_id + '" where name' + "='" + name + "'"
    query_param = {"sql": query}
    return query_param


def validateAndExtractResult(response):
    if len(response['result']['records']) > 0:
        return response['result']['records'][0]['resource_id']
    else:
        return None


def get_parent_details(parent_name):
    url = api['datastore_search_sql']
    filter_condition = "name='" + parent_name + "'"
    query = frame_select_query_to_list_category(meta_data_resource_id, filter_condition)
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    if len(response['result']['records']) > 0:
        return response['result']['records'][0]
    else:
        return None


def get_visual_data(id):
    url = api['datastore_search_sql']
    filter_condition = "metadata_id='" + id + "'"
    query = frame_visual_query('847896c8-ad47-4bf7-a5e0-05c2c41d0c64', filter_condition)
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    return list(map(lambda x: x['visual'], response['result']['records']))


def get_home_page_data():
    url = api['datastore_search_sql']
    filter_condition = filtercondition_home_page()
    query = frame_select_query_to_list_category(meta_data_resource_id, filter_condition)
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    return response['result']['records']


def filtercondition_home_page():
    return "parent_id = 0"


def get_category_data(parent_id):
    url = api['datastore_search_sql']
    filter_condition = parent_id_query(parent_id)
    query = frame_select_query_to_list_category(meta_data_resource_id, filter_condition)
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    return response['result']['records']


def parent_id_query(parent_id):
    return "parent_id =" + str(parent_id)


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
    url = api['datastore_search_sql']
    resource_id = get_resource_id_ckan(parent_data['_id'])
    filter_condition = get_category_list_sql_condition_ckan(parent_data)
    query = frame_select_query_to_list_species(resource_id, filter_condition)
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    return response['result']['records']


def get_resource_id_ckan(id):
    url = api['datastore_search_sql']
    query_param = query_for_resource_id_from(id)
    response = get(url=url, queryparams=query_param)
    return validateAndExtractResult(response)


def query_for_resource_id_from(id):
    query = 'select resource_id from "' + meta_data_resource_id + '" where _id=' + str(id)
    query_param = {"sql": query}
    return query_param


def get_category_list_sql_condition_ckan(parent_data):
    name = parent_data['name']
    return 'category_level2' + "='" + name + "'"


def frame_select_query_to_list_species(resource_id, filter_condition):
    query = 'SELECT species,kingdom,genus from "' + resource_id + '"'
    if filter_condition is not '':
        query = query + ' WHERE ' + filter_condition
    return query


def getSpeciesDetail(category_name, species_name):
    response = get(url=api['datastore_search_sql'],
                   queryparams=form_species_query(resource_id=get_resource_id_by_name(category_name),
                                                  species_name=species_name))
    species_record = response['result']['records'][0]
    return species_record


def form_species_query(resource_id, species_name):
    query = 'SELECT * from "' + resource_id + '"'
    query = query + ' WHERE species LIKE ' + "'" + species_name + "%'"

    query_param = {"sql": query}

    return query_param