import os
import json


def for_each_file(data, directory, function_reference):
    if os.path.isdir(directory):
        for files in os.listdir(directory):
            data = function_reference(data, directory, files)
    return data


def get_json_file_path_from_data(root_category):
    return 'data/' + root_category + '.json'


def append_files(js_files, filename, files):
    js_files.append(filename + '/' + files)
    return js_files


def get_visual_files(filename):
    directory = 'static/js/visualization/' + filename
    js_files = []
    if os.path.isdir(directory):
        for files in os.listdir(directory):
            js_files.append(filename + '/' + files)
    return js_files


def get_json_file(path):
    with open(path) as file:
        return json.load(file)
