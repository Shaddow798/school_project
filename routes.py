import wheel.bdist_wheel
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", title="Homepage")


@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route("/all_machines")
def machines():
    # conn = sqlite3.connect('project.db')
    return render_template("all_machines.html", title="Machines")


# Start a basic inbuilt flask web server, should not use in a production but none of this is made for production.
if __name__ == '__main__':
    app.run(debug=True,port=8080)

