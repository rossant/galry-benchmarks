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
    
def plot_values(x, y, yerr, xlabel='', ylabel='', title='', 
                xticks=[], yticks=[]):

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
    
    plt.grid()

    # legends
    plt.xlabel(xlabel, fontsize='x-large')
    plt.ylabel(ylabel, fontsize='x-large')
    plt.title(title, fontsize='x-large')

def plot_all(r):
    import mplparams
    plt.rcParams.update(mplparams.aps['params'])

    plt.figure(figsize=(14, 4))
    xlabel = "Number of points"
    
    # First frame.
    ax = plt.subplot(131)
    ax.set_xscale("log", nonposx='clip')
    sizes, times, yerr = get_values(r, 'firstframe')
    xticks = 10 ** np.arange(2, np.log10(sizes.max()) + 1, 2)
    plot_values(sizes, times, yerr, xlabel=xlabel, ylabel='First frame rendering time (s)',
                title='First frame rendering time', 
                xticks=xticks, yticks=np.arange(0, times.max() + 1))
    plt.ylim(0, times.max()*1.1)
    plt.legend(loc=2, numpoints=1, fontsize='x-large')

    # Memory.
    ax = plt.subplot(132)
    ax.set_xscale("log", nonposx='clip')
    sizes, memory, yerr = get_values(r, 'memory')
    plot_values(sizes, memory, yerr, xlabel=xlabel, ylabel='Memory (MB)',
                title='Memory consumption', 
                xticks=xticks, yticks=np.arange(0, memory.max()+10, 10))
    plt.ylim(0, memory.max()*1.1)
    
    # FPS.
    ax = plt.subplot(133)
    ax.set_xscale("log", nonposx='clip')
    sizes, fps, yerr = get_values(r, 'fps')
    plot_values(sizes, fps, yerr, xlabel=xlabel, ylabel='Frames per second',
                title='Frames per second', 
                xticks=xticks, yticks=range(0, 1001, 200))
    plt.ylim(0, fps.max()*1.1)
    
    plt.savefig(r['machine_name'] + '.pdf')
    plt.show()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('machine_name', nargs='?')
    args = parser.parse_args()
    
    # Get the filename with the results in JSON: 
    # first command-line argument, or machine name.
    machine_name = args.machine_name or socket.gethostname()
    machine_name = ''.join(c for c in machine_name.lower()
        if c.isalnum() or c in ('_', '-')).rstrip()
    path = machine_name + '.json'
    
    # Load benchmarks from JSON file.
    print("Loading benchmarks from '{0:s}'...".format(path))
    with open(path, 'r') as f:
        r = json.load(f)
    
    # Plot results.
    print(json.dumps(r, indent=4))
    plot_all(r)
    
    