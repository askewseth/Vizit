"""Plot a PNG using matplotlib in a web request, using Flask."""
import random
import StringIO
import os
import csv
import math

from flask import Flask, make_response, render_template, request, url_for, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import sys
sys.path.insert(0, "/home/extra/Desktop/tsite/scripts/")
import scripts.script as sc

import pandas as pd


app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/upload/")
def upload():
    return render_template("upload.html")

@app.route("/uploaded/", methods=["POST"])
def uploaded():
    """Upload csv file."""
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
            row = filter(None, row)
            row = map(float, row)
            df = pd.Series(row)
            avgs.append(float(df.mean()))
            stds.append(float(df.std()))
            sters.append(float(df.std()/math.sqrt(len(df))))
        data = zip(range(1, len(avgs)+1), avgs, stds, sters)

        return render_template("complete.html",
                               rows=rows,
                               data=data
                               )

    except Exception as e:
        return render_template('error.html', error=e)


@app.route('/ngrid/', methods=["GET", "POST"])
@app.route('/ngrid/<dim>/', methods=["GET", "POST"])
def grid(dim='5,5'):
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

        # Displaying the results
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
            dfs = [pd.Series(i) for i in rows]
            averages = map(lambda x: x.mean(), dfs)
            standarddevs = map(lambda x: x.std(), dfs)
            solutions = reduce(zip, [averages, standarddevs])
        except:
            solutions = [[]]
        x, y = orig
        return render_template('grid.html',
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

@app.route('/', methods=["GET", "POST"])
@app.route('/<dim>/', methods=["GET", "POST"])
def ngrid(dim='5,5'):
    try:
        # change table size if button is clicked
        if request.method == "POST":
            if request.form.get('submit', None) == "Change Table Size":
                rows = request.form['numrows']
                cols = request.form['numcols']
                if not rows:
                    # if no input was given return same page
                    if not cols:
                        return redirect(url_for('ngrid'))
                    rows = 5
                if not cols:
                    cols = 5
                dims = str(rows) + "," + str(cols)
                # return page with correct dimensions
                return redirect(url_for('ngrid', dim=dims))
        # get and save the original dimensions
        ans = map(int, dim.split(','))
        assert len(ans) == 2
        x, y = map(int, ans)
        orig = x, y

        # if data is entered get that data
        if request.method == "POST":
            rows = []
            for ix in range(x):
                cols = []
                for iy in range(y):
                    index = str(ix) + ',' + str(iy)
                    cols.append(request.form[index])
                rows.append(cols)

            # Save the entered data to a csv file
            csvname = request.form.get('dataname', 'OTHERNAME')
            print "CSV NAME: ", csvname
            print request.form.get('dname', "DIDN'T WORK")
            saveCSV(rows, name=csvname)
        else:
            rows = [[0]]

        # make sure all of the entries are numerical
        rows = [filter(None, i) for i in rows]
        rows = [map(float, i) for i in rows]
        dfs = [pd.Series(i) for i in rows]
        print type(dfs)
        print type(dfs[0])
        print dfs[0].mean()
        averages = [x.mean() for x in dfs]
        standarddevs = map(lambda x: x.std(), dfs)
        stderr = []
        for x in dfs:
            if x.count() == 0:
                stderr.append(0)
            else:
                stderr.append(float(x.std())/math.sqrt(x.count()))

        solutions = zip(averages, standarddevs, stderr)
        x, y = orig
        finalsolutions = zip(solutions, rows)
        if request.method == 'POST':
            post = True
        else:
            post = False
        return render_template('grid.html',
                               numcols=x,
                               numrows=y,
                               rows=rows,
                               finalsolutions=finalsolutions,
                               post=post
                               )
    except Exception as e:
        return render_template('error.html', error=e)


@app.route('/report/', methods=["GET", "POST"])
def report(data):
    return render_template('data.html', data=data)

@app.route('/try/', methods=["GET", "POST"])
def trydata():
    return redirect(url_for('report', data=[[1,2,3],[2,3,4]]))

@app.route('/grid/', methods=["GET", "POST"])
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
                           stderr=stderror
                           )


@app.route('/home/')
def home():
    """Test home page."""
    return render_template('home.html')


@app.route('/plot.png')
def plot():
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




def saveCSV(data, name=None):
    # get name for file if one not given
    if name is None:
        name = getRandomName()

    # make sure diretory exists
    target = os.path.join(APP_ROOT, "entered/")
    if not os.path.isdir(target):
        os.mkdir(target)

    # make sure name given has extinsion
    if not name.endswith(".csv"):
        name = name + ".csv"

    # tack path on name to avoid changing paths
    fullname = "entered/" + name

    # filter out any blank entries
    data = map(lambda x: filter(None, x), data)
    data = filter(None, data)

    # save the remaining data to the given filename
    with open(fullname, "wb") as f:
        print 'OPENING FILE'
        writer = csv.writer(f, delimiter=",")
        writer.writerows(data)

    return name

def getRandomName():
    target = os.path.join(APP_ROOT, "entered/")
    files = os.listdir(target)
    current_names = map(lambda x: x.split('.')[0], files)

    def rname():
        return str(random.randrange(10**6)) + ".csv"

    name = rname()
    while name in current_names:
        name = rname()
    return name

if __name__ == '__main__':
    app.run(debug=False)
