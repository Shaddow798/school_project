import wheel.bdist_wheel
from flask import Flask, render_template, url_for
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
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Machine')
    results = cur.fetchall()
    return render_template("all_machines.html", results=results, title="Machines")


@app.route("/machine/<int:id>")
def machine(id):
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Machine WHERE id=?",(id,))
    data = cur.fetchone()
    return render_template('machine.html', title="Machine", machine=data,)


@app.route("/all_resources")
def all_resources():
    conn = sqlite3.connect('project.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Resource')
    results = cur.fetchall()
    return render_template('all_resources.html', results=results, title="Resources")


# Start a basic inbuilt flask web server, should not use in a production but none of this is made for production.
if __name__ == '__main__':
    app.run(debug=True,port=8080)

