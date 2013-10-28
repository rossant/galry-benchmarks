# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import time
import numpy as np
from numpy.random import RandomState
import matplotlib.pyplot as plt
import galry.pyplot as glplt


# -----------------------------------------------------------------------------
# Plotting functions
# -----------------------------------------------------------------------------
def run_matplotlib(data):
    fig = plt.figure(figsize=(7.5, 7.5), dpi=80)
    ax = plt.subplot(111)
    ax.plot(data)
    fig.show()
    plt.close(fig)

def run_galry(data):
    fig = glplt.figure(figsize=(600, 600), autodestruct=1)
    fig.plot(data.T)
    glplt.show()


# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
def run(lib, N, seed=20130318):
    
    fun = globals()['run_' + lib]
    
    prng = RandomState(seed)
    data = prng.randn(N, 10)

    # Start the timer.
    t0 = time.clock()

    # Execute the function.
    try:
        fun(data)
    except Exception as e:
        print("An exception occurred: {0:s}".format(str(e)))
        return None

    # Stop the timer.
    t1 = time.clock()
    delay = (t1 - t0)

    return delay
    
if __name__ == "__main__":
    for lib in ('matplotlib', 'galry'):
        print("First frame rendering time {lib}: {time:.3f} s".format(lib=lib, 
                time=run(lib, 1e5)))

