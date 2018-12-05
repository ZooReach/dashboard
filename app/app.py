import os
from flask import Flask, url_for
from app.core.services import render_home, render_category

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
    return render_home()


@app.route('/category/<path:filename>')
def category(filename):
    return render_category(filename)


if __name__ == '__main__':
    app.run()
