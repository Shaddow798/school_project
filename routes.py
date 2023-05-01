from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", title="Homepage")


# Start a basic inbuilt flask web server, should not use in a production but none of this is made for production.
if __name__ == '__main__':
    app.run(debug=True,port=6969)
