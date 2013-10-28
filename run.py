import sys
import os
import json
import socket
import datetime
import time

import numpy as np
import galry
import matplotlib
import matplotlib.pyplot as plt

from benchmarks import run_firstframe, run_memory, run_fps

def plot_values(x, y, xlabel='', ylabel='', title='', xticks=[], yticks=[]):

    # discard empty values
    ind_mpl = y[:,1] > 0

    # plot y consumption
    # plt.axes(mplparams.aps['axes'])
    plt.semilogx(x, y[:,0], '-ok', label='Galry')
    plt.semilogx(x[ind_mpl], y[ind_mpl, 1], '--xk', label='Matplotlib')
    plt.xticks(xticks)
    plt.yticks(yticks)
    plt.grid()

    # legends
    plt.xlabel(xlabel, fontsize='x-large')
    plt.ylabel(ylabel, fontsize='x-large')
    plt.title(title, fontsize='x-large')

def get_fps(r):
    # TODO
    return sizes, fps
    
def get_firstframe(r):
    # TODO
    return sizes, time
    
def get_memory(r):
    # TODO
    return sizes, memory
    
def plot_all(dir=''):
    import mplparams
    plt.rcParams.update(mplparams.aps['params'])

    plt.figure(figsize=(14, 4))
    xticks = [1e2, 1e4, 1e6, 1e8]
    xlabel = "Number of points"
    
    # First frame
    # -----------
    plt.subplot(131)
    
    sizes, times = get_firstframe(r)
    # d = np.load(os.path.join(dir, 'firstframe.npz'))
    # sizes = d['sizes'] * 10  # 10 plots on each figure
    # times = d['times'] * .001

    plot_values(sizes, times, xlabel=xlabel, ylabel='First frame rendering time (s)',
            title='First frame rendering time', xticks=xticks, yticks=[0, 5, 10, 15, 20])
    plt.ylim(0, 23)
    # plt.legend(loc=2)
    plt.legend(loc=2, numpoints=1, fontsize='x-large')#bbox_to_anchor=(0, 0, 1, 1), 
        # bbox_transform=plt.gcf().transFigure, borderaxespad=0)

    # Memory
    # ------
    plt.subplot(132)

    sizes, memory = get_memory(r)
    # d = np.load(os.path.join(dir, 'memory.npz'))
    # sizes = d['sizes'] * 10  # 10 plots on each figure
    # memory = d['memory']

    plot_values(sizes, memory, xlabel=xlabel, ylabel='Memory (MB)',
            title='Memory consumption', xticks=xticks, yticks=[0, 500, 1000, 1500, 2000])
    plt.ylim(0, 2200)
    

    # FPS
    # ---
    plt.subplot(133)

    # TODO
    sizes, fps = get_fps(r)
    # sizes = d['sizes'] * 10  # 10 plots on each figure
    # times = 1. / d['times']

    plot_values(sizes, fps, xlabel=xlabel, ylabel='Frames per second',
            title='Frames per second', xticks=xticks, yticks=[0, 100, 200, 300, 400, 500])
    plt.ylim(0, 520)
    
    plt.savefig(os.path.join(dir, 'benchmarks.pdf'))
    
    plt.show()

def run_all(machine_name):
    
    seeds = [20130318, 20131028, 123456789]
    
    r = {
        'machine_name': machine_name,
        'seeds': seeds,
        'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
        'versions': {
            'matplotlib': matplotlib.__version__,
            'galry': galry.__version__,
        }
    }
    # TODO: further machine characteristics
    
    sizes = 10 ** np.arange(1, 3 + 1)
    r['benchmarks'] = {
        name : {lib: {
                        N: [globals()['run_' + name](lib, N, 
                                                     seed=seed)
                                for seed in seeds]
                                    for N in sizes
                                        if lib == 'galry' or N <= 1e6
                     }
                     for lib in ('matplotlib', 'galry')
                }
                for name in ( 
                    'fps',
                    'memory', 
                    'firstframe', 
                    )
        }
    return r
                    
                    
if __name__ == '__main__':
    
    # HACK: ensure that matplotlibrc is not used for benchmarks
    os.chdir('benchmarks')
    
    
    # Get the filename with the results in JSON: 
    # first command-line argument, or machine name.
    if len(sys.argv) <= 1:
        machine_name = socket.gethostname()
    else:
        machine_name = sys.argv[1]
    machine_name = ''.join(c for c in machine_name.lower()
        if c.isalnum() or c in ('_', '-')).rstrip()
    path = machine_name + '.json'
    
    
    
    # DEBUG
    if os.path.exists(path):
        os.remove(path)
    
    
    
    # Launch or load benchmarks from JSON file.
    if os.path.exists(path):
        print("Loading benchmarks from '{0:s}'...".format(path))
        with open(path, 'r') as f:
            r = json.load(f)
    else:
        print("Launching benchmarks...")
        r = run_all(machine_name)
        with open(path, 'w') as f:
            json.dump(r, f, indent=4)
    
    # Plot results.
    # plot_all(r)
    print json.dumps(r, indent=4)
    
    