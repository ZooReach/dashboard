import os


def for_each_file(data, directory, function_reference):
    if os.path.isdir(directory):
        for files in os.listdir(directory):
            data = function_reference(data, directory, files)
    return data


def get_json_file(path):
    return 'data/' + path + '.json'


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
