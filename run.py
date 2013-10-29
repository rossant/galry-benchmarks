import sys
import os
import json
import socket
import datetime
import time
import argparse

import numpy as np
import galry
import matplotlib
import matplotlib.pyplot as plt

from benchmarks import run_firstframe, run_memory, run_fps

def plot_values(x, y, yerr, xlabel='', ylabel='', title='', 
                xticks=[], yticks=[],
                ax=None):

    # discard empty values
    ind_mpl = y[:,1] > 0

    # plot y consumption
    # plt.axes(mplparams.aps['axes'])
    plt.errorbar(x, y[:,0], fmt='-ok', yerr=yerr[:,0], 
                 label='Galry')
    plt.errorbar(x[ind_mpl], y[ind_mpl, 1], fmt='--xk', yerr=yerr[ind_mpl,1], 
                 label='Matplotlib')
    plt.xticks(xticks)
    plt.yticks(yticks)
    
    ax.set_xscale("log", nonposx='clip')
    plt.grid()

    # legends
    plt.xlabel(xlabel, fontsize='x-large')
    plt.ylabel(ylabel, fontsize='x-large')
    plt.title(title, fontsize='x-large')

def get_lib_values(rr):
    """rr is a dict {size: [val1, val2..]}."""
    keys = sorted([int(x) for x in rr.keys()])
    return np.vstack([rr[str(key)] for key in keys])
    
def get_values(r, name):
    keys = sorted([int(x) for x in r['benchmarks'][name]['galry'].keys()])
    sizes = 10 * np.array(keys)
    galry = get_lib_values(r['benchmarks'][name]['galry'])
    matplotlib = get_lib_values(r['benchmarks'][name]['matplotlib'])
    
    m = np.empty((len(sizes), 2))
    m[:,0] = galry.mean(axis=1)
    m[:,1] = matplotlib.mean(axis=1)
    
    s = np.empty((len(sizes), 2))
    s[:,0] = galry.std(axis=1)
    s[:,1] = matplotlib.std(axis=1)
    
    return sizes, m, s
    
def plot_all(r):
    import mplparams
    plt.rcParams.update(mplparams.aps['params'])

    plt.figure(figsize=(14, 4))
    xticks = [1e2, 1e4, 1e6, 1e8]
    xlabel = "Number of points"
    
    # First frame.
    ax = plt.subplot(131)
    sizes, times, yerr = get_values(r, 'firstframe')
    plot_values(sizes, times, yerr, xlabel=xlabel, ylabel='First frame rendering time (s)',
                title='First frame rendering time', 
                xticks=xticks, yticks=[0, 5, 10, 15, 20],
                ax=ax)
    plt.ylim(0, 23)
    plt.legend(loc=2, numpoints=1, fontsize='x-large')

    # Memory.
    ax = plt.subplot(132)
    sizes, memory, yerr = get_values(r, 'memory')
    plot_values(sizes, memory, yerr, xlabel=xlabel, ylabel='Memory (MB)',
                title='Memory consumption', 
                xticks=xticks, yticks=[0, 500, 1000, 1500, 2000],
                ax=ax)
    plt.ylim(0, 2200)
    
    # FPS.
    ax = plt.subplot(133)
    sizes, fps, yerr = get_values(r, 'fps')
    plot_values(sizes, fps, yerr, xlabel=xlabel, ylabel='Frames per second',
                title='Frames per second', 
                xticks=xticks, yticks=range(0, 1001, 200),
                ax=ax)
    plt.ylim(0, 1000)
    
    plt.savefig(r['machine_name'] + '.pdf')
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument('machine_name', nargs='?')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()
    
    # Get the filename with the results in JSON: 
    # first command-line argument, or machine name.
    machine_name = args.machine_name or socket.gethostname()
    machine_name = ''.join(c for c in machine_name.lower()
        if c.isalnum() or c in ('_', '-')).rstrip()
    path = machine_name + '.json'
    
    # Force the execution of the tests.
    force = args.force
    if force and os.path.exists(path):
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
    print json.dumps(r, indent=4)
    plot_all(r)
    
    