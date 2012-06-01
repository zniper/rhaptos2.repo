from flask import Flask
import flask
import json

app = Flask(__name__)

@app.route("/")
def hello():
    jsontxt = json.dumps({"msg":"hello world"})
    resp = flask.make_response(jsontxt)
    resp.content_type='application/json'
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5005)
