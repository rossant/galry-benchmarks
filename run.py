import sys
import os
import json
import socket
import datetime
import time
import argparse
import multiprocessing
import platform

import numpy as np
import galry
import matplotlib
import OpenGL

from benchmarks import run_firstframe, run_memory, run_fps

def run_all(machine_name, maxlogsize=5):
    
    seeds = [20130318,]# 20131028, 123456789]
    
    r = {
        'machine_name': machine_name,
        'machine_info': {
            'ncpus': multiprocessing.cpu_count(),
            'system': platform.system(),
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': platform.processor(),
        },
        'seeds': seeds,
        'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
        'versions': {
            'python': platform.python_version(),
            'matplotlib': matplotlib.__version__,
            'galry': galry.__version__,
            'numpy': np.__version__,
            'pyopengl': OpenGL.__version__,
        }
    }
    
    
    sizes = 10 ** np.arange(1, maxlogsize + 1)
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
    
    