import wheel.bdist_wheel
from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
# This key is temp af
app.secret_key = 'oelwE=ZN#h~UrJv{+-d,-u`)i;34|Q'
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Image upload code is mostly privaterd from the flask documentation https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# This loads in the database file for the folder of the project.
def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "project.db")
    conn = sqlite3.connect(db_path)
    return conn


@app.route('/')
def index():
    return render_template("index.html", title="Homepage")


@app.route('/about')
def about():
    return render_template("about.html", title="About")


@app.route("/all_machines")
def machines():
    conn = get_db_connection()
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


# At least part of this block of code is sourced from another one of my projects at home.
@app.route("/machine/submit", methods=('GET', 'POST'))
def machine_submit():
    if request.method == 'POST':
        name = request.form["machine"]
        description = request.form["machine_description"]

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if not name:
            flash('Title is required!')
        elif not description:
            flash('Description is required!')
        elif file.filename == '':
            flash('No selected file')
        else:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            complete_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            conn = get_db_connection()
            conn.execute('INSERT INTO Machine (name, description, picture)'
                         'VALUES (?, ?, ?)', (name, description, complete_path))
            conn.commit()
            conn.close()

            flash("Success Creating entry")
            return redirect(url_for('machines'))
    return render_template('submission.html', title="Submit A Machine")


@app.route("/all_resources")
def all_resources():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Resource')
    results = cur.fetchall()
    return render_template('all_resources.html', results=results, title="Resources")


@app.route("/resources/<int:id>")
def resource(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Resource WHERE id=?",(id,))
    data = cur.fetchone()
    return render_template('resources.html', title="Resources", resource=data,)


# Account Login and signup
@app.route("/login")
def login():
    flash("Feature not implemted yet")
    return render_template('accounts/login.html', title="Login")


@app.route("/register")
def register():
    flash("Feature not implemted yet")
    return render_template('accounts/register.html', title="Register")


@app.errorhandler(404)
def error(e):
    return render_template("error.html", error=e)


# Start a basic inbuilt flask web server, should not use in a production but none of this is made for production.
if __name__ == '__main__':
    app.run(debug=True, port=8080)
