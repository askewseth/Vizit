from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

#plot.circle([1,2], [3,4])

class Plotter:
    script = None
    div = None

    def circle(self, data):
        # need to validate the data some more in here
        # just get it working for now
        output_file("plot.html")
        plot = figure(plot_width=400, plot_height=400)
        plot.circle(data[0], data[1])
        # Get the components of the plot (HTML)
        self.script, self.div = components(plot)
        #show(plot)

    def scatter(self, data):
        pass

    def bar(self,data):
        pass

    def histo(self, data):
        pass

    def getscript(self):
        return self.script

    def getdiv(self):
        return self.div
