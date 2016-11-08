#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def randrange(n):
    a = []
    r = sorted([random.randint(0, 255) for _ in range(n)])
    g = sorted([random.randint(0, 255) for _ in range(n)])
    b = sorted([random.randint(0, 255) for _ in range(n)])

    for i in range(n):
        t = [r[i], g[i], b[i]]
        a.append(t)
    # print(a)
    return a


def reshape(l, width):
    l2 = zip(*[iter(l)] * width)
    return l2


def gen_matrix(nSide=5, nColors=10):
    """
    generate an icon with a certain set of colors
    identicon style
    """
    m = [random.randint(0, 10) for _ in range(nSide * nSide)]
    return reshape(m, nSide)
