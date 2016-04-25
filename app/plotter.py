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
        plot.multi_line(data[0], data[1], color["red", "green"])

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
            return None
        else:
            # data: {'x' : '1,2,3,...,n', 'y' : '5,6,7,...,n'}
            xdata = data['x']
            ydata = data['y']

            # process the data
            xdata_split = xdata.split(',')
            ydata_split = ydata.split(',')
            xdata_float = []
            ydata_float = []

            #parse the data into ints
            for n in xdata_split:
                xdata_float.append(float(n))

            for n in ydata_split:
                ydata_float.append(float(n))

            return [xdata_float, ydata_float]

    def getscript(self):
        return self.script

    def getdiv(self):
        return self.div
