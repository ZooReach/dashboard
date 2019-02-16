from flask import Flask
from .core.services import render_home, render_category, get_json, raise_exception
from flask import send_file

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_home()


@app.route('/category/<path:filename>')
def category(filename):
    return render_category(filename)


@app.route('/api/<path:filename>')
def api(filename):
    return get_json(filename)


@app.route('/api/images/<path:filename>')
def images(filename):
    return send_file(filename)


@app.errorhandler(500)
def service_exception(e):
    return raise_exception(e)


if __name__ == '__main__':
    app.run()
