import os
import json
import functools
from .species_repository import get_visual_data


def get_os_directory():
    return os.path.dirname(os.path.dirname(__file__))


def list_dir(directory):
    if os.path.isdir(directory):
        return os.listdir(directory)
    return []


def get_visual_map_from_db(id):
    return get_visual_data(id)


def get_visual_files(id):
    return list(map(lambda files: os.path.join('js', 'visualization', '.'.join([files, 'js'])),
                    get_visual_map_from_db(id)))

def get_visual_file(species_name):
    return [os.path.join('js', 'visualization' , '.'.join([species_name,'js']))]

def get_json_file_path_from_data(root_category):
    return os.path.join(get_os_directory(), 'data', "".join([root_category, '.json']))


def get_json_file(path):
    with open(path) as file:
        return json.load(file)


def update_json(json_data, json_files):
    json_data.update(json.load(json_files)['type'])
    return json_data


def update_json_from_file(json_data, directory, files):
    with open(os.path.join(directory, files)) as json_files:
        return update_json(json_data, json_files)


def home_page_category_data():
    directory = os.path.join(get_os_directory(), "data")
    return functools.reduce(lambda data, files: update_json_from_file(data, directory, files), list_dir(directory), {})
