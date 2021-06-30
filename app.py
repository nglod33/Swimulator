from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=['POST'])
def simulate_meet():
    teams = dict(json.loads(request.data))




app.run()
