#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import numpy as np

import begin


def hp(x, α=0.05):
    n = len(x)
    y = [0] * n
    g = [0] * n
    for i in range(1, n):
        g[i] = α * g[i - 1] + (1 - α) * x[i]
        y[i] = x[i] - g[i]
    return y


def lp(x, α=0.1):
    n = len(x)
    # y = [0] * n
    y = np.array(x)
    for i in range(1, n):
        y[i] = y[i - 1] + α * (x[i] - y[i - 1])
    return list(y)

n = 100
orig = np.linspace(0, 100, num=n)

# x = np.sin(x)
np.random.seed(42)
d = np.random.normal(scale=1.2, size=n)
# d = np.sin(200 * x)
x = orig + d


def iterplot(orig, x, y):
    plt.clf()
    plt.plot(orig, label="orig")
    plt.plot(x, label="noisy")
    plt.plot(y, label="lowpass")
    plt.axes().legend(loc="upper left")


@begin.subcommand
def iterate():
    e = []
    for i in range(100, 1, -1):
        α = i / 100.
        print("α is %0.2f" % α)
        y = lp(x, α)
        error = np.power(y - orig, 2)
        # print(error.shape)
        # print(np.vstack((x, y, orig, error)).T)
        e.append(np.sum(error))
        iterplot(orig, x, y)
        plt.title(r"$\alpha$ = %0.2f" % α)
        # plt.plot(z)
        plt.show(block=False)
        plt.waitforbuttonpress(0.01)

    idx = 100 - np.argmin(e)
    print("min error: %0.2f → %d" % (np.min(e), idx))
    y = lp(x, idx / 100.)
    iterplot(orig, x, y)
    plt.title("best = 0.%d" % idx)
    plt.show()


def fn(α):
    return lp(x, α) - orig


@begin.subcommand
def lstsq():
    out = leastsq(fn, 0.99, full_output=True)
    # print(out)

    idx = out[0][0]
    print("idx: %0.2f" % idx)
    y = lp(x, idx)

    iterplot(orig, x, y)
    plt.title("best = %0.2f" % idx)
    plt.show()


@begin.start
def main():
    pass
