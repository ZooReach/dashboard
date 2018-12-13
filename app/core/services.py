from flask import render_template, request
from ..utils.rest_client import get
from ..utils.constants import environment_details, api, display_details
from ..utils.extract_value import get_base_url_till_given_string
from .category import get_category, get_resource_id, get_species_from_path
from .file_operations import get_visual_files, get_json_file_path_from_data, get_json_file, \
    home_page_category_data


def render_home():
    return render_template('home/home.html', ckan_url=environment_details['ckan'], json_data=home_page_category_data())


def render_category(filename):
    category_path = filename.split('/')
    string = 'category'
    base_url = get_base_url_till_given_string(request, string)
    category_type = get_json_file(get_json_file_path_from_data(category_path[0]))
    species_str = get_species_from_path(category_type, category_path)

    if species_str:
        return render_species_details(category_path)

    return render_template('category/category.html', ckan_url=environment_details['ckan'], json_data=get_category(category_path, category_type),
                           fullpath=category_path,
                           js_files=get_visual_files(filename), base_url=base_url)


def render_species_details(path):
    species_name = path[len(path)-1]
    url = api['datastore_search']
    resource_id = get_resource_id(path)
    query_params = {'resource_id': resource_id, 'filters': '{"species":"'+species_name+'"}', 'limit':'1'}
    response = get(url=url, queryparams=query_params)
    species_record = response['result']['records'][0]
    species_display_info = _get_filtered_details(species_record, display_details)
    species_display_info['is_species'] = 'true'
    return render_template('species_detail/species_detail.html', ckan_url=environment_details['ckan'], species_name=species_name, json_data= species_display_info,
                           fullpath=path)


def _get_filtered_details(species_record,keys):
    species_display_info = {}
    for key in keys:
        species_display_info[key] = species_record[key]
    return species_display_info