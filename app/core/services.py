from flask import render_template, request
from app.utils.extract_value import get_base_url_till_given_string
from app.core.category import get_category
from app.core.file_operations import for_each_file, get_visual_files, get_json_file_path_from_data, get_json_file


def render_home():
    directory = 'data'
    json_data = {}
    return render_template('home/home.html', json_data=for_each_file(json_data, directory, update_json_from_file))


def render_category(filename):
    category_path = filename.split('/')
    string = 'category'
    base_url = get_base_url_till_given_string(request, string)
    category_type = get_json_file(get_json_file_path_from_data(category_path[0]))
    species_str = get_species_from_path(category_type, category_path)

    if species_str:
        return render_species_details(category_path)

    return render_template('category/category.html', json_data=get_category(category_path, category_type), fullpath=category_path,
                           js_files=get_visual_files(filename), base_url=base_url)


def render_species_details(path):
    ckan_species_info_response = {"Name": "species#", "Kingdom": "us"}
    ckan_species_info_response['is_species'] = 'true'
    return render_template('species_detail/species_detail.html', json_data=ckan_species_info_response,
                           fullpath=path)


def get_species_from_path(category_type, path):
    species_str = ''
    for idx, name in enumerate(path):
        if 'type' in category_type:
            category_type = category_type['type'][name]
        else:
            species_str = path[idx:]
    return species_str


def update_json_from_file(json_data, directory, files):
    json_file = get_json_file(directory + '/' + files)
    json_data.update(json_file['type'])
    return json_data
