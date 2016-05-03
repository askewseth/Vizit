"Plot a PNG using matplotlib in a web request, using Flask."
import random
import os
import StringIO
import flask

from flask import Flask, make_response, render_template, request, redirect, url_for, session
#from flask_restful import Resource, Api, reqparse
#from flask.views import MethodView
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
from plotter import Plotter
import message as messages


"""from OpenSSL import SSL

CONTEXT = SSL.Context(SSL.TLSv1_2_METHOD)
CONTEXT.use_privatekey_file('./static/keys/server.key')
CONTEXT.use_certificate_file('./static/keys/server.crt')
"""

import sys
sys.path.insert(0, "/home/extra/Desktop/tsite/scripts/")
import script as sc
import database as db


app = Flask(__name__)

# Session stuff http://flask.pocoo.org/snippets/51/
class ItsdangerousSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = False


class ItsdangerousSessionInterface(SessionInterface):
    salt = 'cookie-session'
    session_class = ItsdangerousSession

    def get_serializer(self, app):
        if not app.secret_key:
            return None
        return URLSafeTimedSerializer(app.secret_key,
                                      salt=self.salt)

    def open_session(self, app, request):
        s = self.get_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            return self.session_class()
        max_age = app.permanent_session_lifetime.total_seconds()
        try:
            data = s.loads(val, max_age=max_age)
            return self.session_class(data)
        except BadSignature:
            return self.session_class()

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                   domain=domain)
            return
        expires = self.get_expiration_time(app, session)
        val = self.get_serializer(app).dumps(dict(session))
        response.set_cookie(app.session_cookie_name, val,
                            expires=expires, httponly=True,
                            domain=domain)

# Activate the session interface
app.session_interface = ItsdangerousSessionInterface()
# Session stuff http://flask.pocoo.org/snippets/51/

"""
Class to generate the plot data and return it as html

API Methods:
    GET - <id>
        Gets a stored plot based on the id of the plot data (user must be logged in)
    PUT
        Generates a plot based on the data passed in from the data form in the request.
        the plot is returned as html to the client? (not sure if flask will like that)
"""

@app.route('/apiv1/plot', methods=["GET", "POST", "PUT"])
def api_plot():
    if request.method == 'GET':
        # Is the user authorized? Check the session.
        if True:
            return '<p>Only authorized users may retreive plots</p>'
        return None
    elif request.method == "POST":
        # Update an existing plot
        return '<p>Eventually this will be a plot</p>'
    elif request.method == "PUT":
        # Create a new plot
        p = Plotter()
        # What was the type of plot selected?
        plot_type = request.json["type"]

        # probably need to format the data
        # parse it out into a dict
        data = request.json["data"]
        #process the data

        p.plot(data, plot_type)
        # process the script
        script = p.script.replace("<script", "<script id='plotscript'")
        html = p.div + "\n" + script
        return html

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
        if 'user' in session:
            status = messages.returnLoggedInMenuBar()
        else:
            status = messages.returnLoggedOutMenuBar()

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
        if 'user' in session:
            status = messages.returnLoggedInMenuBar()
        else:
            status = messages.returnLoggedOutMenuBar()
    return render_template('stats.html', menubar=status,
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
    if 'user' in session:
        status = messages.returnLoggedInMenuBar()
        mess = messages.returnWelcomeLoggedIn()

    else:
        status = messages.returnLoggedOutMenuBar()
        mess = messages.returnWelcome()

    return render_template('default.html', menubar=status, tag=mess)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Login in page
    handle server side logic here
    """
    if request.method == "GET":
        #render_template("login.html")
        return render_template("default.html")
    elif request.method == "POST":
        # Begin credential validation here
        """
        1. Get the data from the form
        2. Hash the password and check for username entry in DB
        3. If match set session["authed"] = True
        4. else set session["authed"] = False
        5. Redirect on True, error on False
        """
        email = request.form['email']
        password = request.form['password']
        if db.login(email,password):
            session["authed"] = True
            session["user"] = email
            status = messages.returnLoggedInMenuBar()
            mess = messages.returnWelcomeLoggedIn()
        else:
            session["authed"] = False
            status = messages.returnLoggedOutMenuBar()
            mess = messages.returnLoginError()

    return render_template('default.html', menubar=status, tag=mess)

@app.route('/logout', methods=["GET"])
def logout():
    """Login in page
    handle server side logic here
    """
    status = messages.returnLoggedOutMenuBar()
    mess = messages.returnWelcome()
    if request.method == "GET":
        #Log the user out if logged in.
        if 'user' in session:
            session.clear()
            return render_template('default.html',
                                   menubar=status,
                                   tag=mess)
        else:
            return render_template('default.html',
                                   menubar=status,
                                   tag=mess)

    return None

@app.route('/register', methods=["GET", "POST", "PUT"])
def register():
    if request.method == "GET":
        # Render the registration page
        mess = messages.returnDisclaimer()
        return render_template("register.html", tag=mess)
    elif request.method == "POST":
        # Create an account
        email = request.form['email']
        password = request.form['pass1']
        if db.addUser( email, password ):
            status = messages.returnLoggedInMenuBar
            mess = messages.returnNewAccountSuccessful()
            return render_template("default.html", menubar=status, tag=mess)
        else:
            status = messages.returnLoggedOutMenuBar
            mess = messages.returnNewAccountFailure()
            return render_template("register.html", menubar=status, tag=mess)

    elif request.method == "PUT":
        # Create an account
        pass
    return None


@app.route('/plot_data')
def plot_data():
    """ We need to render the page and get the data
    from the user and then generate the appropriate html"""
    return render_template('plot.html')
"""
@app.route('/plot.png')
def plot_img():
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
"""

if __name__ == '__main__':
    # Create a random session key
    #app.secret_key = os.urandom(24)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #CONTEXT = ('./static/keys/server.crt', './static/keys/server.key')
    #app.run(host='127.0.0.1', port='5000', debug=True, ssl_context=CONTEXT)
    app.run(host='127.0.0.1', port=5000, debug=True)
