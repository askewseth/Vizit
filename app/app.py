"Plot a PNG using matplotlib in a web request, using Flask."
import random
import StringIO

from flask import Flask, make_response, render_template, request, session, redirect, url_for, escape
from flask_restful import Resource, Api, reqparse
from flask.views import MethodView
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

"""from OpenSSL import SSL

CONTEXT = SSL.Context(SSL.TLSv1_2_METHOD)
CONTEXT.use_privatekey_file('./static/keys/server.key')
CONTEXT.use_certificate_file('./static/keys/server.crt')
"""

import sys
sys.path.insert(0, "/home/extra/Desktop/tsite/scripts/")
import script as sc

app = Flask(__name__)
api = Api(app)

"""
Class to generate the plot data and return it as html

API Methods:
    GET - <id>
        Gets a stored plot based on the id of the plot data (user must be logged in)
    PUT
        Generates a plot based on the data passed in from the data form in the request.
        the plot is returned as html to the client? (not sure if flask will like that)
"""
get_parser = reqparse.RequestParser()
get_parser.add_argument("id",type=str, help="Data must be comma delimited.")

"""
class PlotApiUnauth(Resource):
    # Dict to temporarily hold the plots
    plots = {}
    def gen_plot(self, data):
        return None

    def get(self):
        #There has to be a better way to return just the html
        return {"ERROR" : "Not implemented, yet."}

    def put(self):
       # data = request.json['data']
       # print data
        return "{'name' : 'put_endpoint', 'value' : 'Not fully working'}"

api.add_resource(PlotApiUnauth, '/apiv1/plot')
"""

@app.route('/apiv1/plot', methods=["GET", "POST", "PUT"])
def api_plot():
    if request.method == 'GET':
        # Is the user authorized?
        if false:
            return '<p>Only authorized users may retreive plots</p>'

        return None


@app.route('/stats/', methods=["GET", "POST"])
def stats():
    """
    Display statistics on a given dataset.

    Takes a various number of statistical measurements on a dataset, either
    supplied as default or entered by the user, and outputs these measurements.
    """
    if request.method == 'GET':
        # Set default values when no input given
        val = 'NO INPUT'
        avginp = 'NO INPUT'
        otherval = str(avginp)
        avg, stderror, count, med, std, minn, q1, q2, q3, maxx = [0 for x in range(10)]
    else:
        val = 'INPUT'
        # Get Values from HTML
        otherval = request.form['inputtxt']
        # Format input as list
        avginp = sc.stripinputlist(otherval)
        # Take average
        avg = sc.avg(avginp)
        # Get standard deviation and standard error
        std, stderror = sc.std(avginp)
        # Get all of the pandas statistcal output
        count, med, std, minn, q1, q2, q3, maxx = sc.getDescription(avginp)
    return render_template('stats.html',
                           val=val,
                           ov=otherval,
                           avg=avg,
                           std=std,
                           q1=q1,
                           q2=q2,
                           q3=q3,
                           minn=minn,
                           maxx=maxx,
                           med=med,
                           count=count,
                           stderr=stderror)


@app.route('/')
def home():
    """Test home page."""
    return render_template('home.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    """Login in page
    handle server side logic here
    """
    if request.method == "GET":
        #render_template("login.html")
        return render_template("login.html")
    elif request.method == "POST":
        # Begin credential validation here
        return "{'ERROR' : 'Not implemented'}"

    return None

@app.route('/plot_data')
def plot_data():
    """ We need to render the page and get the data
    from the user and then generate the appropriate html"""
    return render_template('plot.html')

@app.route('/plot.png')
def plot_img():
    """Display plot of random numbers, just proof of concept."""
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = StringIO.StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response

if __name__ == '__main__':
    #CONTEXT = ('./static/keys/server.crt', './static/keys/server.key')
    #app.run(host='127.0.0.1', port='5000', debug=True, ssl_context=CONTEXT)
    app.run(host='127.0.0.1', port=5000, debug=True)
