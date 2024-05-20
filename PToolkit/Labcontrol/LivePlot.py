import tkinter as tk
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class TkLivePlot(tk.LabelFrame):
    def __init__(self, master, text=None, interval=1000, blit=False, maxpoints=50):
        super().__init__(master, text=text)
        self.x = []
        self.y = []
        self.z = []
        self.maxpoints = maxpoints
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=master)
        self.ani = FuncAnimation(plt.gcf(), self.Animation, interval=interval, blit=blit)

    def grid(self,**kwargs):
        self.canvas.get_tk_widget().grid(kwargs)

    def Animation(self, i):
        self.ax.cla()
        self.ax.plot(self.x, self.y)

    def Update(self): 
        if len(self.x) >= self.maxpoints + 1:
            self.x = self.x[1:self.maxpoints + 1]

        if len(self.y) >= self.maxpoints + 1:
            self.y = self.y[1:self.maxpoints + 1]


    def UpdatePlot(self, x=[], y=[], z=[]):
        self.x = x
        self.y = y
        self.z = z
        self.Update()

    def AppendPlot(self, x=None, y=None, z=None):
        if x:
            self.x.append(x)

        if y:
            self.y.append(y)

        if z:
            self.z.append(z)

        self.Update()

    def Increment(self, variable):
        if variable == "x":
            if len(self.x) > 0:
                self.x.append(self.x[-1]+1)
            else:
                self.x.append(1)
        
        if variable == "y":
            if len(self.y) > 0:
                self.y.append(self.y[-1]+1)
            else:
                self.y.append(1)
        

        if variable == "z":
            pass

        self.Update()