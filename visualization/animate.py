#!/usr/bin/env python
# -*- coding: utf-8 -*-


from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import mlab as ML
import numpy as np
import begin
import logging
#import colored_traceback
# colored_traceback.add_hook(always=True)

"""
vimeval
nmap <leader>p :silent exec "!tmux last-pane" \| redraw!<CR>
nmap <leader>w :Tmux !!<CR>
nmap <leader>c :Tmux <c-v><c-c><cr>
endeval
"""


def dowork(X, Y, Z, gridsize):
    x = X.ravel()
    y = Y.ravel()
    if Z is not None:
        z = Z.ravel()
    else:
        z = Z
    plt.subplot(211)

    plt.hexbin(x, y, C=z, gridsize=gridsize, cmap=cm.jet, bins=None)
    plt.axis([x.min(), x.max(), y.min(), y.max()])

    # cb = plt.colorbar()
    # cb.set_label('mean value')
    plt.show()


@begin.subcommand
def rand(gridsize=40):
    "plot a random hexgrid"
    x = y = np.linspace(-5, 5, 100)
    print("x shape", x.shape)
    X, Y = np.meshgrid(x, y)
    print("X shape", X.shape)
    Z1 = ML.bivariate_normal(X, Y, 2, 2, 0, 0)
    Z2 = ML.bivariate_normal(X, Y, 4, 1, 1, 1)
    noise = np.random.normal(scale=0.005, size=10000).reshape(100, 100)
    ZD = Z2 - Z1 + noise
    print(x)
    dowork(X, Y, ZD, gridsize)


@begin.subcommand
@begin.convert(gridsize=int, actors=int, noise=float)
def mouse(filename, gridsize=60, actors=50, noise=20):
    "read a file of mouse coordinates and plot them"
    coords = np.loadtxt(filename, delimiter=",")
    xmin = 0
    ymin = 0
    xmax = 1920 * 2 + 2560
    ymax = 1600
    # xmin = coords[0].min()
    # ymin = coords[1].min()
    # xmax = coords[0].max()
    # ymax = coords[1].max()
    limits = [xmin, xmax, ymin, ymax]
    print("shape: {0}".format(coords.shape))
    events = int(coords.shape[0] / actors)
    trimline = events * actors
    print("trimline is {0}".format(trimline))
    coords = np.resize(coords, (trimline, 2))
    coords = np.split(coords, actors)
    print(coords)
    print("new shape: {0}".format(coords[0].shape))
    saved = np.array(coords)
    if (noise > 0):
        ndata = np.random.normal(
            scale=noise, size=saved.size).reshape(saved.shape)
        saved += ndata
    for i in range(10, events):
        coords = saved[:, i - 10:i]
        print("one inhabitant", coords.shape)
        coords = coords.reshape((actors * 10, 2))
        x = coords[:, 0]
        y = coords[:, 1]
        print("coords shape", coords.shape)
        size = (coords.max(axis=0) - coords.min(axis=0)) / gridsize
        print("grid limits", size)

        plt.clf()
        plt.subplot(212)
        plt.scatter(x, y)
        plt.axis(limits)
        plt.gca().invert_yaxis()

        plt.subplot(211)
        plt.hexbin(x, y, cmap=cm.jet, gridsize=(18, 12), extent=limits)
        ax = plt.gca()
        ax.set_axis_bgcolor([0, 0, 0.5, 1.])
        plt.axis(limits)
        ax.invert_yaxis()
        # plt.savefig("/tmp/heatmap%04d.png" % (i - 10), dpi=300)
        plt.show(block=False)
        plt.waitforbuttonpress(timeout=0.1)

    # plt.clf()
    # plt.imshow(heatmap, extent=extent)
    # plt.show()


@begin.start
@begin.logging
def run():
    "hexplot heatmap generator"
    logging.debug("started")
    pass
