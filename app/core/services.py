from flask import render_template, request

from .category import get_home_page, get_category
from .file_operations import get_visual_files, get_visual_file, get_all_visual_chart_files
from .species_repository import get_parent_details, getSpeciesDetail, get_all_species_details, get_home_page_data, \
    get_species_experts_data
from ..utils.constants import environment_details, display_details
from ..utils.extract_value import get_base_url_till_given_string, split_path
from ..utils.auto_suggestion_using_trie import autocomplete_main
from importlib import import_module
import json


def render_home():
    data = get_home_page()
    return render_template('home/home.html', ckan_url=environment_details['ckan'], json_data=data,
                           js_files=get_visual_files(0))


def render_category(path):
    path_array = path.split('/')
    parent_data = get_parent_details(path_array[-1])
    category_path = split_path(path)

    if parent_data:
        data = get_category(parent_data['_id'], parent_data, path_array[0])
    else:
        return render_species_details(path_array)
    return render_template('category/category.html', ckan_url=environment_details['ckan'],
                           json_data=data,
                           parent_data=parent_data,
                           parent_name=parent_data['name'],
                           fullpath=category_path,
                           js_files=get_visual_files(parent_data['id']),
                           base_url=get_base_url_till_given_string(request, 'category'))


def render_species_details(path):
    species_name = get_species_name(category_path=path)
    species_record = getSpeciesDetail(path[0], path[-1])
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
    return render_template('common/custom_error_view.html', message=e.description,
                           base_url=get_base_url_till_given_string(request, 'category')), 500


def get_json(filename):
    category_path = split_path(path=filename)
    my_module = import_module('.' + '.'.join(category_path), package='app.apis')
    return my_module.main()


def render_experts():
    data = get_home_page_data()
    return render_template('species_experts/find_experts.html', ckan_url=environment_details['ckan'], parent_data=data)


def render_report():
    return render_template('reports/report.html', ckan_url=environment_details['ckan'], js_files=get_all_visual_chart_files())


def find_auto_complete_species():
    search_key = request.args.get('search_key', '')
    species_data = get_all_species_details()
    autocompleted_data = autocomplete_main(search_key, species_data)
    if not autocompleted_data:
        return json.dumps(autocompleted_data)
    return json.dumps(autocompleted_data[:10])


def find_species_experts():
    selected_key = request.args.get('selected_key', '')
    species_expert_data = get_species_experts_data(selected_key)
    return json.dumps(species_expert_data)


def get_visual_report(filename):
    js_files = get_visual_file(filename)
    return json.dumps(js_files)


def get_visual_chart(filename):
    js_files = get_visual_file(filename)
    return render_template('common/visual_chart.html', js_files=js_files)

def about_us():
    return render_template('home/about.html')