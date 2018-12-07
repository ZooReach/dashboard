import os
import json
import functools


def list_dir(directory):
    if os.path.isdir(directory):
        return os.listdir(directory)
    return []


def get_visual_files(filename):
    directory = 'static/js/visualization/' + filename
    return list(map(lambda files: os.path.join(filename, files), list_dir(directory)))


def get_json_file_path_from_data(root_category):
    return os.path.join('data', "".join([root_category, '.json']))


def append_files(js_files, filename, files):
    js_files.append(os.path.join(filename, files))
    return js_files


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
    directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    return functools.reduce(lambda data, files: update_json_from_file(data, directory, files), list_dir(directory), {})
