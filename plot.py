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
    ng = galry.shape[0]
    nm = matplotlib.shape[0]
    
    m = np.empty((len(sizes), 2))
    m[:,0] = np.mean(galry, axis=1)
    m[:nm,1] = np.mean(matplotlib, axis=1)
    m[nm:,1] = np.nan
    
    s = np.empty((len(sizes), 2))
    s[:,0] = np.std(galry, axis=1)
    s[:nm,1] = np.std(matplotlib, axis=1)
    s[nm:,1] = np.nan
    
    return sizes, m, s
    
def plot_values(x, y, yerr, xlabel='', ylabel='', title='', 
                xticks=None, yticks=None):

    # discard empty values
    ind_mpl = ~np.isnan(y[:,1])
    
    # plot y consumption
    plt.errorbar(x, y[:,0], fmt='-ok', yerr=yerr[:,0], 
                 label='Galry')
    plt.errorbar(x[ind_mpl], y[ind_mpl, 1], fmt='--xk', yerr=yerr[ind_mpl,1], 
                 label='Matplotlib')
    if xticks is not None:
        plt.xticks(xticks)
    if yticks is not None:
        plt.yticks(yticks)
    
    plt.grid()

    # legends
    plt.xlabel(xlabel, fontsize='x-large')
    plt.ylabel(ylabel, fontsize='x-large')
    plt.title(title, fontsize='x-large')

def plot_all(r, filename):
    import mplparams
    plt.rcParams.update(mplparams.aps['params'])

    plt.figure(figsize=(14, 4))
    plt.locator_params(axis='y', nbins=4)
    xlabel = "Number of points"
    
    # First frame.
    ax = plt.subplot(131)
    ax.set_xscale("log", nonposx='clip')
    # ax.set_yscale("log", nonposy='clip')
    sizes, times, yerr = get_values(r, 'firstframe')
    xticks = 10 ** np.arange(2, np.log10(sizes.max()) + 1, 2)
    plot_values(sizes, times, yerr, xlabel=xlabel, ylabel='First frame rendering time (s)',
                title='First frame rendering time', 
                xticks=xticks,)# yticks=np.arange(0, times.max() + 1))
    plt.ylim(0, times[~np.isnan(times)].max()*1.1)
    plt.legend(loc=2, numpoints=1, fontsize='x-large')

    # Memory.
    ax = plt.subplot(132)
    ax.set_xscale("log", nonposx='clip')
    # ax.set_yscale("log", nonposy='clip')
    sizes, memory, yerr = get_values(r, 'memory')
    plot_values(sizes, memory, yerr, xlabel=xlabel, ylabel='Memory (MB)',
                title='Memory consumption', 
                xticks=xticks,)#yticks=np.arange(0, memory.max()+10, 10))
    plt.ylim(0, memory[~np.isnan(memory)].max()*1.1)
    
    # FPS.
    ax = plt.subplot(133)
    ax.set_xscale("log", nonposx='clip')
    # ax.set_yscale("log", nonposy='clip')
    sizes, fps, yerr = get_values(r, 'fps')
    plot_values(sizes, fps, yerr, xlabel=xlabel, ylabel='Frames per second',
                title='Frames per second', 
                xticks=xticks,)#yticks=range(0, 1001, 200))
    plt.ylim(0, fps[~np.isnan(fps)].max()*1.1)
    
    plt.savefig(os.path.splitext(filename)[0] + '.pdf')
    plt.show()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?')
    args = parser.parse_args()
    path = args.filename
    if not path:
        files = [_ for _ in os.listdir('.') if _.endswith('.json')]
        assert files, "Please specify the path to a JSON file."
        path = files[0]
    
    # Load benchmarks from JSON file.
    print("Loading benchmarks from '{0:s}'...".format(path))
    with open(path, 'r') as f:
        r = json.load(f)
    
    # Plot results.
    # print(json.dumps(r, indent=4))
    plot_all(r, path)
    
    