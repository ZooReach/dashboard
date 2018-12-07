import os
from flask import Flask, url_for
from core.services import render_home, render_category

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_home()


@app.route('/category/<path:filename>')
def category(filename):
    return render_category(filename)


if __name__ == '__main__':
    app.run()
