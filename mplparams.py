"""
mplparams.py

M.V. DePalatis, 2010-09-01
Licensed under the GNU GPL v3

matplotlib rc params and axes rects to generate figures of appropriate
size for different types of publication.
"""

# documentclass 'article' with package 'fullpage'
fullpage = {'params': {'axes.labelsize': 10*2,
                       'text.fontsize': 10*2,
                       'legend.fontsize': 10*2,
                       'xtick.labelsize': 8*2,
                       'ytick.labelsize': 8*2,
                       'text.usetex': False,
                       'font.family': 'serif',
                       'figure.figsize': (7, 7)},
            'axes': [0.150,0.175,0.95-0.15,0.95-0.25]}

# two-column APS journal format
aps = {'params': {'axes.labelsize': 10*2,
                  'text.fontsize': 10*2,
                  'legend.fontsize': 10*2,
                  'xtick.labelsize': 8*2,
                  'ytick.labelsize': 8*2,
                  'text.usetex': False,
                  'figure.figsize': (7, 7)},
       'axes': [0.125,0.2,0.95-0.125,0.95-0.2]}
       
