from flask import Flask
from .core.services import render_home, render_category, get_json, raise_exception,render_experts, find_species_experts, render_report, find_auto_complete_species, get_visual_report
from flask import send_file

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_home()


@app.route('/experts')
def experts():
    return render_experts()

@app.route('/report')
def report():
    return render_report()

@app.route('/find-experts')
def find_experts():
    return find_species_experts()


@app.route('/find-species')
def find_species():
    return find_auto_complete_species()


@app.route('/category/<path:filename>')
def category(filename): 
    return render_category(filename)


@app.route('/api/<path:filename>')
def api(filename):
    return get_json(filename)


@app.route("/<path:filename>")
def visual_report(filename):
    return get_visual_report(filename)


@app.route('/api/images/<path:filename>')
def images(filename):
    return send_file(filename)


@app.errorhandler(500)
def service_exception(e):
    return raise_exception(e)


if __name__ == '__main__':
    app.run()
