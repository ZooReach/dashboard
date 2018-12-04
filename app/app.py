from flask import Flask, render_template, url_for, request
import json
import os

app = Flask(__name__)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


def for_each_file(data, directory, function_reference):
    if os.path.isdir(directory):
        for files in os.listdir(directory):
            data = function_reference(data, directory, files)
    return data


def update_json_from_file(json_data, directory, files):
    with app.open_resource(directory + '/' + files) as json_files:
        json_data.update(json.load(json_files)['type'])
    return json_data


@app.route('/')
@app.route('/home')
def home():
    directory = 'data'
    json_data = {}
    return render_template('home/home.html', json_data=for_each_file(json_data, directory, update_json_from_file))


@app.route('/category/<path:filename>')
def category(filename):
    path = filename.split('/')
    base_url = get_base_url_for_category(request)

    with app.open_resource(get_json_file(path[0])) as file:
        category_type = json.load(file)

    return render_template('category/category.html', json_data=get_category(path, category_type), fullpath=path,
                           js_files=get_visual_files(filename), base_url=base_url)


def get_json_file(path):
    return 'data/' + path + '.json'


def get_category(path, category_type):
    json_data = category_type
    for name in path:
        json_data = json_data['type'][name]
    return json_data


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


def get_base_url_for_category(request):
    return ''.join(request.base_url.split('category')[0])+'category/'


if __name__ == '__main__':
    app.run()
