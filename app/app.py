from flask import Flask, render_template, url_for
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


def for_each_file(data, directory, function):
    if os.path.isdir(directory):
        for files in os.listdir(directory):
            data = function(data, directory, files)
    return data


def update_json_from_file(jsonData, directory, files):
    with app.open_resource(directory + '/' + files) as jsonfiles:
        jsonData.update(json.load(jsonfiles)['type'])
    return jsonData


@app.route('/')
@app.route('/home')
def home():
    directory = 'data'
    jsonData = {}
    return render_template('home/home.html', jsonData=for_each_file(jsonData, directory, update_json_from_file))


@app.route('/category/<path:filename>')
def category(filename):
    path = filename.split('/')

    with app.open_resource(getJsonFile(path[0])) as file:
        type = json.load(file)

    return render_template('category/category.html', jsonData=getType(path, type), fullpath=path,
                           jsfiles=getVisualFiles(filename))


def getJsonFile(path):
    return ('data/' + path + '.json')


def getType(path, type):
    jsonData = type
    for name in path:
        jsonData = jsonData['type'][name]
    return jsonData


def append_files(jsfiles, filename, files):
    jsfiles.append(filename + '/' + files)
    return jsfiles


def getVisualFiles(filename):
    directory = 'static/js/visualization/' + filename
    jsfiles = []
    if os.path.isdir(directory):
        for files in os.listdir(directory):
            jsfiles.append(filename + '/' + files)
    return jsfiles


if __name__ == '__main__':
    app.run()
