from app.core.file_operations import get_json_file, get_json_file_path_from_data
from ..utils.rest_client import get
from ..utils.constants import api
import functools


def get_category(path, json_data):
    categories_json = get_categories_json(path, json_data)

    if 'type' in categories_json.keys():
        for key in categories_json['type']:
            if 'type' not in categories_json['type'][key]:
                path_with_category_level_2 = path[:]
                path_with_category_level_2.append(key) #adding category level 2 to get specific resul of it
                species_list = get_species_list(path_with_category_level_2)
                if bool(species_list):
                    categories_json['type'][key]['type'] = species_list
    else:
        categories_json['type'] = get_species_list(path)

    return categories_json


def get_categories_json(path, json_data):
    return functools.reduce(lambda result, name: result['type'][name], path, json_data)


def get_species_list(path):
    url = api['datastore_search_sql']
    resource_id = get_resource_id(path)
    filter_condition = get_category_list_sql_condition(path)
    query = frame_select_query_to_list_species(resource_id,filter_condition)
    query_param = {"sql": query}
    response = get(url=url, queryparams=query_param)
    ckan_species_list_response = response['result']['records']
    species_obj = {species['species']: {"Name": species['species'], "type": {}, "Kingdom": species['kingdom'],
                                        "image": "images/placeholder.svg"}
                   for species in ckan_species_list_response}
    return species_obj


def get_category_list_sql_condition(path):
    category_list = ''
    for index, category in enumerate(path[1:]):
        if category_list != '':
            category_list = category_list + ' AND '
        category_index = 'category_level' + str(index+1)
        category_list = category_list + category_index + "='" + category + "'"
    return category_list


def frame_select_query_to_list_species(resource_id,filter_condition):
    query = 'SELECT species,kingdom from "' + resource_id+'"'
    if filter_condition is not '':
        query = query + ' WHERE ' + filter_condition
    return query


def get_species_from_path(category_type, path):
    species_str = ''
    for idx, name in enumerate(path):
        if 'type' in category_type:
            category_type = category_type['type'][name]
        else:
            species_str = path[idx:]
    return species_str


def get_resource_id(category_path):
    category_type = get_json_file(get_json_file_path_from_data(category_path[0]))
    return category_type['type'][category_path[0]]['resource_id']
