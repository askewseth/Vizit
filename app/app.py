"Plot a PNG using matplotlib in a web request, using Flask."
import random
import os
import StringIO
import flask
import csv
import math

from flask import Flask, make_response, render_template, request, redirect, url_for, session
from flask_restful import Resource, Api, reqparse
from flask.views import MethodView
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
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
import pandas as pd
import database as db


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
@app.route("/upload/")
def upload():
    if 'user' in session:
        mess = messages.returnCSVInstructions()
        status = messages.returnLoggedInMenuBar()
        return render_template("upload.html",
                               menubar=status,
                               tag=mess)
        
    else:
        return redirect ("/")

@app.route("/uploaded/", methods=["POST"])
def uploaded():
    """Upload csv file."""
    if 'user' in session:
        status = messages.returnLoggedInMenuBar()
        # Get the target path
        target = os.path.join(APP_ROOT, "uploads/")
        print target

        # Make sure Directory exists
        if not os.path.isdir(target):
            os.mkdir(target)

        # Save file(s)
        for f in request.files.getlist("file"):
            print f
            filename = f.filename
            destination = "/".join([target, filename])
            print destination
            f.save(destination)

        # Display CSV file contents
        try:
            with open(destination, 'r+') as f:
                reader = csv.reader(f)
                rows = [row for row in reader]
                assert type(rows[0]) == list, "ROW ELEMENT'S WEREN'T LISTS"

            avgs, stds, sters = [], [], []
            for row in rows:
                row = map(float, row)
                df = pd.DataFrame(row)
                avgs.append(float(df.mean().values[0]))
                stds.append(float(df.std().values[0]))
                sters.append(float(df.std().values[0]/math.sqrt(len(df))))

            data = zip(range(1, len(avgs)+1), avgs, stds, sters)
            return render_template("complete.html",
                               menubar=status,
                               rows=rows,
                               data=data
                               )
        except Exception as e:
            return render_template('error.html', error=e)
        
    else:
        return redirect ("/")
    


@app.route('/ngrid/', methods=["GET", "POST"])
@app.route('/ngrid/<dim>/', methods=["GET", "POST"])
def grid(dim='5,5'):
    status = messages.returnLoggedInMenuBar()
    try:
        try:
            if request.method == "POST":
                if request.form.get('submit', 'no') == 'results':
                    return redirect(url_for('report', data=[[5]]))
            ans = map(int, dim.split(','))
            assert len(ans) == 2
            x, y = ans
            orig = x, y
            if request.method == "POST":
                banner = request.form["0,0"]
            else:
                banner = "test banner"

        except Exception as e:
            return render_template('error.html', error=e)

        if request.method == "POST":
            rows = []
            for ix in range(x):
                cols = []
                for iy in range(y):
                    index = str(ix) + ',' + str(iy)
                    cols.append(request.form[index])
                rows.append(cols)
        else:
            rows = [[0]]
        newrows = map(lambda x: ",".join(x), map(str, rows))
        banner = "\n".join(map(str, newrows))
        #
        # # Displaying the results
        if request.method == 'POST':
            extra = True
            nrows = [filter(None, i) for i in rows]
            dfs = map(lambda x: pd.Series(x), nrows)
            averages = map(lambda x: x.mean(), dfs)
            stddev = map(lambda x: x.std(), dfs)
            averages, stddev = "", ""
        else:
            extra, averages, stddev = False, None, None
            extra = False
        rows = [["hello"], ["goodbye"]]

        try:
            dfs = [pd.DataFrame(i) for i in rows]
            averages = map(lambda x: x.mean(), dfs)
            standarddevs = map(lambda x: x.std(), dfs)
            solutions = reduce(zip, [averages, standarddevs])
        except:
            solutions = [[]]
        x, y = orig
        return render_template('grid.html',
                               menubar=status,
                               numrows=x,
                               numcols=y,
                               banner=banner,
                               rows=rows,
                               extra=extra,
                               averages=averages,
                               stddev=stddev
                               )
    except Exception as e:
        return render_template('error.html',error=e)
@app.route('/report/', methods=["GET", "POST"])
def report(data):
    return render_template('data.html', data=data)

@app.route('/try/', methods=["GET", "POST"])
def trydata():
    return redirect(url_for('report', data=[[1,2,3],[2,3,4]]))

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
        print type(data)
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

@app.route('/<dim>/', methods=["GET", "POST"])
def ngrid(dim='5,5'):
    try:
        # if request.method == "POST":
        #     if request.form.get('submit', 'no') == 'results':
        #         # return redirect(url_for('plot')
        #         return redirect("www.tsethaskew.me")
        ans = map(int, dim.split(','))
        assert len(ans) == 2
        x, y = map(int, ans)
        orig = x, y

        if request.method == "POST":
            rows = []
            for ix in range(x):
                cols = []
                for iy in range(y):
                    index = str(ix) + ',' + str(iy)
                    cols.append(request.form[index])
                rows.append(cols)
        else:
            rows = [[0]]

        try:
            rows = [map(float, r) for r in rows]
        except Exception as e:
            rows = [r for r in rows]

        rows = [filter(None, i) for i in rows]
        rows = [map(float, i) for i in rows]
        dfs = [pd.Series(i) for i in rows]
        print type(dfs)
        print type(dfs[0])
        print dfs[0].mean()
        try:
            averages = [x.mean() for x in dfs]
            # averages = map(lambda x: x.mean(), dfs)
        except Exception as e:
            return render_template('error.html', error=e)
        # averages = map(lambda x: x.mean().values[0], dfs)
        # standarddevs = map(lambda x: x.std().values[0], dfs)
        standarddevs = map(lambda x: x.std(), dfs)
        # stderr = [float(x.std())/math.sqrt(x.count()) for x in dfs if x.count() != 0 else 0]
        stderr = []
        for x in dfs:
            if x.count() == 0:
                stderr.append(0)
            else:
                stderr.append(float(x.std())/math.sqrt(x.count()))

        # stderr = map(lambda x: float(x.std())/math.sqrt(x.count()), dfs)
        # standarderrors = map(lambda x: x.std()/float(math.sqrt(x.count()), dfs)
        # solutions = reduce(zip, [averages, standarddevs, standarderrors])
        # solutions = reduce(zip, [averages, standarddevs])
        solutions = zip(averages, standarddevs, stderr)
        # except:
            # solutions = [[]]
        x, y = orig
        # rows = zip(solutions, rows)
        finalsolutions = zip(solutions, rows)
        return render_template('grid.html',
                               numcols=x,
                               numrows=y,
                               rows=rows,
                               finalsolutions=finalsolutions
                               )
    except Exception as e:
        return render_template('error.html', error=e)

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
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        if db.login(email,password):
            session["authed"] = True
            session["user"] = email
            return redirect("/")
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
            session["authed"] = False
            session.pop('user', None)
            return redirect ("/")
        else:
            return redirect ("/")

    return None

@app.route('/register', methods=["GET", "POST", "PUT"])
def register():
    if request.method == "GET":
        # Render the registration page
        mess = messages.returnDisclaimer()
        return render_template("register.html", tag=mess)
    elif request.method == "POST":
        # Create an account
        email = request.form['email'].strip()
        password = request.form['pass1'].strip()
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
    if 'user' in session:
        status = messages.returnLoggedInMenuBar()
        return render_template('plot.html', tag=status)
    else:
        stats = messages.returnLoggedOutMenuBar()
        mess = messages.returnWelcome()
        return redirect("/")


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
    # Create a random session key
    #app.secret_key = os.urandom(24)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #CONTEXT = ('./static/keys/server.crt', './static/keys/server.key')
    #app.run(host='127.0.0.1', port='5000', debug=True, ssl_context=CONTEXT)
    app.run(host='127.0.0.1', port=5000, debug=True)
