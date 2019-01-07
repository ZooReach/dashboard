from flask import render_template, request

from .category import get_home_page, get_category
from .file_operations import get_visual_files
from .species_repository import get_parent_details, getSpeciesDetail
from ..utils.constants import environment_details, display_details
from ..utils.extract_value import get_base_url_till_given_string, split_path
from importlib import import_module


def render_home():
    data = get_home_page()
    return render_template('home/home.html', ckan_url=environment_details['ckan'], json_data=data)


def render_category(path):
    if '/' in path:
        parent_name = path.split('/')[-1:][0]
    else:
        parent_name = path

    parent_data = get_parent_details(parent_name)

    category_path = split_path(path=path)

    if parent_data:
        data = get_category(parent_data['_id'],parent_data)
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
    species_record = getSpeciesDetail(category_name, species_name)
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


def get_species_name(category_path):
    return category_path[len(category_path) - 1]


def get_category_name(category_path):
    return category_path[len(category_path) - 2]


def raise_exception(e):
    return render_template('common/custom_error_view.html', message=e.description,base_url=get_base_url_till_given_string(request, 'category')), 500


def get_json(filename):
    category_path = split_path(path=filename)
    my_module = import_module('.' + '.'.join(category_path), package='apis')
    return my_module.main()


