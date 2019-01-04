from flask import render_template, request
from ..utils.rest_client import get
from ..utils.constants import environment_details, api, display_details
from ..utils.extract_value import get_base_url_till_given_string
from .category import get_category, get_resource_id, get_resource_id_ckan_by_name, get_home_page, get_category_ckan, get_parent_details
from .file_operations import get_visual_files, get_json_file_path_from_data, get_json_file, \
    home_page_category_data
from importlib import import_module
import json


def render_home():
    data = get_home_page()
    return render_template('home/home.html', ckan_url=environment_details['ckan'], json_data=data)


def render_category(path):
    if '/' in path:
        parent_name = path.split('/')[-1:][0]
    else:
        parent_name = path

    parent_data = get_parent_details(parent_name)

    category_path = get_array_from_string_path(path=path)

    #species_str = get_species_from_path(category_type, category_path)

    if parent_data:
        data = get_category_ckan(parent_data['_id'],parent_data)
    else :
       return render_species_details(category_path)


    return render_template('category/category.html', ckan_url=environment_details['ckan'],
                            json_data=data,
                            parent_data=parent_data,
                            parent_name=parent_data['name'],
                            fullpath=category_path,
                            js_files=get_visual_files(parent_data['name']),
                            base_url=get_base_url_till_given_string(request, 'category'))


def render_species_details(path):
    species_name = get_species_name(category_path=path)
    category_name = get_category_name(path)
    response = get(url=api['datastore_search_sql'],
                   queryparams=form_species_query(resource_id=get_resource_id_ckan_by_name(category_name), species_name=species_name, limit=1))
    species_record = response['result']['records'][0]
    species_display_info = _get_filtered_details(species_record=species_record, keys=display_details)
    species_display_info['is_species'] = 'true'
    return render_template('species_detail/species_detail.html', ckan_url=environment_details['ckan'],
                           species_name=species_name, json_data=species_display_info,
                           fullpath=path)


def _get_filtered_details(species_record, keys):
    available_data = species_record.keys()
    species_display_info = {display_key: (species_record[display_key] if display_key in available_data else '')
                            for display_key in keys}
    return species_display_info

def form_species_query(resource_id, species_name, limit=10):

    query = 'SELECT * from "' + resource_id + '"'
    query = query + ' WHERE species LIKE ' + "'" +species_name+"%'"

    query_param = {"sql": query}

    return query_param

def form_query_params(resource_id, species_name, limit=10):
    species_name+='%'
    filter_condition = json.dumps({'species': species_name})
    return {'resource_id': resource_id, 'filters': filter_condition, 'limit': limit}


def get_species_name(category_path):
    return category_path[len(category_path) - 1]

def get_category_name(category_path):
    return category_path[len(category_path) - 2]


def get_array_from_string_path(path):
    return path.split('/')


def get_json(filename):
    category_path = get_array_from_string_path(path=filename)
    my_module = import_module('.' + '.'.join(category_path), package='apis')
    return my_module.main()


def raise_exception(e):
    return render_template('common/custom_error_view.html', message=e.description,base_url=get_base_url_till_given_string(request, 'category')), 500


