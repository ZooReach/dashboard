from flask import render_template, request
from app.utils.extract_value import get_base_url_till_given_string
from app.core.category import get_category
from app.core.file_operations import for_each_file, get_visual_files, get_json_file
import json


def render_home():
    directory = 'data'
    json_data = {}
    return render_template('home/home.html', json_data=for_each_file(json_data, directory, update_json_from_file))


def render_category(filename):
    path = filename.split('/')
    string = 'category'
    base_url = get_base_url_till_given_string(request, string)

    with open(get_json_file(path[0])) as file:
        category_type = json.load(file)

    json_check = category_type
    species_str = ''
    for idx, name in enumerate(path):
        if 'type' in json_check:
            json_check = json_check['type'][name]
        else:
            species_str = path[idx:]
    if species_str:
        ckan_species_info_response = {"Name": "species#", "Kingdom": "us"}
        ckan_species_info_response['is_species'] = 'true'
        return render_template('species_detail/species_detail.html', json_data=ckan_species_info_response,
                               fullpath=path)
    return render_template('category/category.html', json_data=get_category(path, category_type), fullpath=path,
                           js_files=get_visual_files(filename), base_url=base_url)


def update_json_from_file(json_data, directory, files):
    with open(directory + '/' + files) as json_files:
        json_data.update(json.load(json_files)['type'])
    return json_data
