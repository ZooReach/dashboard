from flask import render_template, request
from ..utils.extract_value import get_base_url_till_given_string
from .category import get_category
from .file_operations import get_visual_files, get_json_file_path_from_data, get_json_file, \
    home_page_category_data
from ..utils.rest_client import get
from ..utils.constants import api, display_details


def render_home():
    return render_template('home/home.html', json_data=home_page_category_data())


def render_category(filename):
    category_path = filename.split('/')
    string = 'category'
    base_url = get_base_url_till_given_string(request, string)
    category_type = get_json_file(get_json_file_path_from_data(category_path[0]))
    species_str = get_species_from_path(category_type, category_path)

    if species_str:
        return render_species_details(category_path)

    return render_template('category/category.html', json_data=get_category(category_path, category_type),
                           fullpath=category_path,
                           js_files=get_visual_files(filename), base_url=base_url)


def render_species_details(path):
    species_name = path[len(path)-1]
    url = api['datastore_search']
    resource_id = _get_resource_id(path)
    query_params = {'resource_id': resource_id, 'filters': '{"species":"'+species_name+'"}', 'limit':'1'}
    response = get(url=url, queryparams=query_params)
    species_record = response['result']['records'][0]
    species_display_info = _get_filtered_details(species_record, display_details)
    species_display_info['is_species'] = 'true'
    return render_template('species_detail/species_detail.html',species_name=species_name, json_data=species_display_info,
                           fullpath=path)


def get_species_from_path(category_type, path):
    species_str = ''
    for idx, name in enumerate(path):
        if 'type' in category_type:
            category_type = category_type['type'][name]
        else:
            species_str = path[idx:]
    return species_str


def _get_resource_id(category_path):
    category_type = get_json_file(get_json_file_path_from_data(category_path[0]))
    return category_type['type'][category_path[0]]['resource_id']


def _get_filtered_details(species_record,keys):
    species_display_info = {}
    for key in keys:
        species_display_info[key] = species_record[key]
    return species_display_info