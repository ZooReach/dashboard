from flask import Flask, render_template
import json
 
app = Flask(__name__)
 
@app.route('/')
@app.route('/home')
def home():
    with app.open_resource('data/nature.json') as f:
        species = json.load(f)
    return render_template('home.html', cards=species)
        
if __name__ == '__main__':
    app.run()