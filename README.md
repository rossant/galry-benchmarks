# Performance comparison between Galry and Matplotlib

This repository contains benchmarks that compare the performance of Galry and Matplotlib in terms of:

* Frames Per Seconds (FPS) while zooming on a plot
* Memory consumption
* First frame rendering time

These values are computed on plots containing 10 white noise signals with (N/10) points in each, with N varying from 100 to a maximum of 100,000,000 on systems that support such huge plots.

To run the benchmarks:

  * You need Matplotlib and the latest version of Galry (>0.2.0dev)
  * Clone this repository, cd into it, and run:
    
        python run.py
        
  * After several minutes, you'll find a JSON file in this repository with the benchmark results. Just run
  
        python plot.py
        
    to plot the results.

