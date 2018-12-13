from app.core.file_operations import get_json_file, get_json_file_path_from_data
from ..utils.rest_client import get
from ..utils.constants import api
import json


def get_category(path, json_data):
    print(path)
    for name in path:
        json_data = json_data['type'][name]
        for key in json_data['type']:
            if 'type' not in json_data['type'][key]:
                ckan_species_list_response = _get_species_list(path)
                species_obj = {species['species']: species for species in ckan_species_list_response}
                json_data['type'][key]['type'] = species_obj
    return json_data


def _get_species_list(path):
    url = api['datastore_search']
    resource_id = get_resource_id(path)
    category_list = _get_category_list(path)
    query_params = {'resource_id': resource_id, 'filters': category_list}
    response = get(url=url, queryparams=query_params)
    return response['result']['records']


def _get_category_list(path):
    category_list = {}
    for index, category in enumerate(path[1:]):
        category_index = 'category_level'+str(index+1)
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