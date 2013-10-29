"""Command-line tool to estimate the mean RAM consumption of a plot."""
import os
import sys
import argparse

from memory_profiler import memory_usage
import numpy as np
from numpy.random import RandomState

def benchmark(function, N, dt=1, duration=10, seed=20130318):
    prng = RandomState(seed)
    data = prng.randn(N, 10)
    mem_usage = memory_usage((function, (data,)), interval=duration, timeout=duration)
    return np.mean(mem_usage)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('type')
    parser.add_argument('N')
    parser.add_argument('--seed')
    parser.add_argument('--duration', help='in seconds')
    parser.add_argument('--dt', help='in ms')
    
    args = parser.parse_args()
    type = args.type
    N = int(float(args.N))
    seed = int(args.seed or 20130318)
    duration = int(args.duration or 10)
    dt = int(args.dt or 1)
    
    if type == 'matplotlib':
        from memory_matplotlib import load
    else:
        from memory_galry import load
    print(benchmark(load, N, dt=dt, duration=duration, seed=seed))
    
    