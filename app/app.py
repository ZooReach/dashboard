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


@app.route('/')
@app.route('/home')
def home():
    with app.open_resource('data/nature.json') as f:
        species = json.load(f)
    return render_template('home/home.html', cards=species)


@app.route('/category/<category>')
def category(category):
    return render_template('category/category.html', category=category)


if __name__ == '__main__':
    app.run()
