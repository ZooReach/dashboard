from app.core.file_operations import get_json_file, get_json_file_path_from_data
from ..utils.rest_client import get
from ..utils.constants import api
import json
import functools


def get_category(path, json_data):
    categories_json = get_categories_json(path, json_data)

    if 'type' in categories_json.keys():
        for key in categories_json['type']:
            if 'type' not in categories_json['type'][key]:
                categories_json['type'][key]['type'] = get_species_list(path)
    else:
        categories_json['type'] = get_species_list(path)

    return categories_json


def get_categories_json(path, json_data):
    return functools.reduce(lambda result, name: result['type'][name], path, json_data)


def get_species_list(path):
    url = api['datastore_search']
    resource_id = get_resource_id(path)
    category_list = get_category_list(path)
    query_params = {'resource_id': resource_id, 'filters': category_list, 'limit': '1'}
    response = get(url=url, queryparams=query_params)
    ckan_species_list_response = response['result']['records']
    species_obj = {species['species']: {"Name": species['species'], "type": {}, "Kingdom": species['kingdom'],
                                        "image": "images/placeholder.svg"}
                   for species in ckan_species_list_response}
    return species_obj


def get_category_list(path):
    category_list = {}
    for index, category in enumerate(path[1:]):
        category_index = 'category_level' + str(index + 1)
        category_list[category_index] = category
        return json.dumps(category_list)


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
