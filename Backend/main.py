from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Some text"

app.run("localhost", 8080)