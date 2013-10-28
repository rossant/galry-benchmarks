# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import subprocess

import numpy as np
from numpy.random import RandomState
from memory_profiler import memory_usage


# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
def run(lib, N, dt=1, duration=10, seed=20130318):
    return float(subprocess.check_output(['python', 'memory_tool.py',
                                    str(lib), str(N), 
                                    '--duration='+str(duration),
                                    '--dt='+str(dt),
                                    '--seed='+str(seed),
                                    ]))

if __name__ == "__main__":
    for lib in ('matplotlib', 'galry'):
        print("RAM {lib}: {mem:.1f} MB".format(lib=lib, mem=run(lib, 1e4)))
