from flask import Flask, request,  url_for
import datetime

app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello World!" + datetime.datetime.today().strftime('%d%m%Y - %H%M%S') + repr(request.headers)

@app.route("/module/", methods=['POST', 'GET'])
def module():
    modhash = request.form['content']
    return 'the module was %s' % modhash


if __name__ == "__main__":
    app.debug = True
    app.run()
