# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import sys, os, random, time
from time import sleep
from qtools.qtpy.QtCore import *
from qtools.qtpy.QtGui import *

import numpy as np
from numpy.random import RandomState

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from galry import show_window, get_application
import galry.pyplot as glplt


# -----------------------------------------------------------------------------
# Matplotlib
# -----------------------------------------------------------------------------
class AppForm(QMainWindow):
    def __init__(self, parent=None, N=None, dt=None, duration=None, seed=None):
        QMainWindow.__init__(self, parent)
        self.N = N
        self.dt = dt
        self.duration = duration
        self.seed = seed
        self.create_main_frame(N)
        
        self.times = []
        self.t00 = time.clock()
        self.t0 = time.clock()

        self.timer = QTimer()
        self.timer.setInterval(self.dt)
        self.timer.timeout.connect(self.on_draw)
        self.timer.start()

    def on_draw(self):
        i = len(self.times)
        
        xlim = [i*self.N*.01,self.N-1-i*self.N*.01]
        
        if xlim[0] < xlim[1]:
            # update canvas
            self.axes.set_xlim(xlim)
            self.canvas.draw()
        
            # record the delay
            delay = time.clock() - self.t0
            self.times.append(delay)
            
            self.t0 = time.clock()
            
            # print the delay
            sys.stdout.write(str(delay) + '\r')
        else:
            self.close()
            
        # close the window after TOTAL_FRAMES frames
        if time.clock() >= self.t00 + self.duration:
            self.close()
    
    def create_main_frame(self, N):
        self.main_frame = QWidget()
        self.dpi = 100
        self.fig = Figure(figsize=(7.5, 7.5), dpi=80)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        
        # plot
        prng = RandomState(self.seed)
        data = prng.randn(N, 10)
        plot = self.axes.plot(data)
        self.axes.set_ylim(-5, 5)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
        self.show()

def run_matplotlib(N, dt=1, duration=10, seed=20130318):
    """Return the median time interval between two successive paint refresh."""
    prng = RandomState(seed)
    window = show_window(AppForm, N=N, seed=seed, dt=dt, duration=duration)
    return 1. / np.median(window.times)

    
# -----------------------------------------------------------------------------
# Galry
# -----------------------------------------------------------------------------
def callback(self, (t,)):
    i = len(self.times)
    
    xlim = [-1+i*.01, 1-i*.01]
    
    # time intervals are not recorded after the animation stops
    if xlim[0] < xlim[1]:
        # update canvas
        viewbox = (xlim[0], -5, xlim[1], 5)
        self.process_interaction('SetViewbox', viewbox)
    
        # record the delay
        delay = time.clock() - self.t0
        self.times.append(delay)
        
        self.t0 = time.clock()
        
        # print the delay
        sys.stdout.write(str(delay) + '\r')
    else:
        self.widget.close_widget()
    
def run_galry(N, dt=1, duration=10, seed=20130318):
    """Return the median time interval between two successive paint refresh."""
    prng = RandomState(seed)
    data = prng.randn(N, 10)        

    fig = glplt.figure(figsize=(600, 600), autodestruct=duration * 1000)
    fig.t0 = time.clock()
    fig.times = []
    fig.N = N
    fig.plot(data.T)
    fig.animate(callback, dt=dt * .001)
    fig.show()
    
    return 1. / np.median(fig.times)
    
def run_fps(lib, *args, **kwargs):
    return globals()['run_' + lib](*args, **kwargs)
    
if __name__ == "__main__":
    for lib in ('matplotlib', 'galry'):
        print "FPS {lib}: {fps:.1f} FPS".format(lib=lib, fps=1./run_fps(lib, 1e4))

