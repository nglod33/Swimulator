from flask import Flask

app = Flask(__name__)


@app.route("/simulate")
def hello_world():
    print("Hello world!")


app.run()