"Plot a PNG using matplotlib in a web request, using Flask."
import random
import StringIO
import os

from flask import Flask, make_response, render_template, request, url_for, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import sys
sys.path.insert(0, "/home/extra/Desktop/tsite/scripts/")
import scripts.script as sc

import pandas as pd


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads/"
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/', methods=["GET", "POST"])
@app.route('/<dim>/', methods=["GET", "POST"])
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
                    # try:
                    cols.append(request.form[index])
                    # except Exception as e:
                        # print e
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
            dfs = map(lambda x: pd.DataFrame(x), nrows)
            averages = map(lambda x: float(x.mean()), dfs)
            stddev = map(lambda x: float(x.std()), dfs)
            averages, stddev = "", ""
        else:
            extra, averages, stddev = False, None, None
            extra = False
        rows = [["hello"], ["goodbye"]]

        try:
            dfs = [pd.DataFrame(x) for x in rows]
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

@app.route('/ngrid/', methods=["GET", "POST"])
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
            dfs = [pd.DataFrame(i) for i in rows]
            averages = map(lambda x: x.mean().values[0], dfs)
            standarddevs = map(lambda x: x.std().values[0], dfs)
            # standarderrors = map(lambda x: x.std().values[0]/float(np.sqrt(x.count().values[0])), dfs)
            # solutions = reduce(zip, [averages, standarddevs, standarderrors])
            # solutions = reduce(zip, [averages, standarddevs])
            solutions = zip([averages, standarddevs])
        except:
            solutions = [[]]
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



if __name__ == '__main__':
    app.run(debug=False)
