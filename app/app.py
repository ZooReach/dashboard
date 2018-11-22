from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def hello():
    return render_template('extend.html', name="zooreach")

if __name__=='__main__':
	app.run()