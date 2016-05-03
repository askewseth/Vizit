import re #regex module

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

#plot.circle([1,2], [3,4])

class Plotter:
    script = None
    div = None

    def scatter(self, data):
        # need to validate the data some more in here
        plot = figure(plot_width=400, plot_height=400)
        plot.scatter(data[0], data[1])
        # Get the components of the plot (HTML)
        self.script, self.div = components(plot)
        #show(plot)

    def annulus(self, data):
        plot = figure(plot_width=400, plot_height=400)
        plot.annulus(data[0], data[1], color='#7fc97f',
                     inner_radius=0.2, outer_radius=0.5)
        self.script, self.div = components(plot)

    def line(self, data):
        plot = figure(plot_width=400, plot_height=400)
        plot.line(data[0], data[1])
        self.script, self.div = components(plot)

    # the data for this must be two arrays of arrays
    # ex: x: [[1,2,3,...n],[...,...]] y: [[4,5,6,...,n],[...,...]]
    def multi_line(self, data):
        plot = figure(plot_width=400, plot_height=400)
        plot.multi_line(data[0], data[1], color=["red", "green"])
        show(plot)
        self.script, self.div = components(plot)

    # the data for this must be two arrays of arrays
    # ex: x: [[1,2,3,...n],[...,...]] y: [[4,5,6,...,n],[...,...]]
    def patch(self, data):
        plot = figure(plot_width=400, plot_height=400)
        plot.patch(data[0], data[1], color="#4c4c4c")
        self.script, self.div = components(plot)

    def plot(self, data, t):
        data = self.parse_data(data, t)
        if t == "scatter":
            self.scatter(data)
        elif t == "annulus":
            self.annulus(data)
        elif t == "line":
            self.line(data)
        elif t == "multi_line":
            self.multi_line(data)
        elif t == "patch":
            self.patch(data)

    # Parse the incoming json data into a dict of numbers
    def parse_data(self, data, t):
        # if the type requires multi arrays
        if t in ["multi_line", "patch"]:
            # parse the data differently
            # expect list of lists
            d = [data['x'], data['y']]
            return d
        else:
            # data: {'x' : '1,2,3,...,n', 'y' : '5,6,7,...,n'}
            xdata = data['x']
            ydata = data['y']

             # Sanitize
            xdata_clean = self.sanitize_data(xdata)
            ydata_clean = self.sanitize_data(ydata)

            # process the data
            xdata_split = xdata_clean.split(',')
            ydata_split = ydata_clean.split(',')
            xdata_float = []
            ydata_float = []

            #parse the data into floats
            for n in xdata_split:
                xdata_float.append(float(n))

            for n in ydata_split:
                ydata_float.append(float(n))

            return [xdata_float, ydata_float]

    # Scrub the data of anything that isn't a float or dec
    # Only allow certain characters
    # Data - list of data points ideally comma separated
    def sanitize_data(self, data):
        # iterate through data string
        # ^[-+]?([0-9]+\.?[0-9]*|[0-9]*\.?[0-9]+)$
        # Tokenize the data string
        str_split = data.split(',')
        clean_str = ""

        for s in str_split:
            if re.search(r'^[-+]?([0-9]+\.?[0-9]*|[0-9]*\.?[0-9]+)$', s) != None:
                # It's allowed
                clean_str = clean_str + s + ','
            # no else needed, simply don't use the unmatched strings
        clean_str = clean_str[:clean_str.rfind(',')]
        return clean_str

    def getscript(self):
        return self.script

    def getdiv(self):
        return self.div
