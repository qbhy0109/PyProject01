"""
import flask
app = flask.Flask(__name__)

@app.route("/")
def index():
    try:
        fobj = open("index.html","rb")
        data = fobj.read()
        fobj.close()
        return data
    except Exception as err:
        return str(err)
"""
import flask
app = flask.Flask(__name__)
@app.route("/")
def index():
    f = open("index.html","rb")
    data = f.read()
    f.close()
    return data
app.run()




