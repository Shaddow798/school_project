from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


# Start a basic inbuilt flsak web server, should not use in a production but none of this is made for production.
if __name__ == '__main__':
    app.run(debug=True)
