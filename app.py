from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
