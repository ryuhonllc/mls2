
from __future__ import print_function
from math import sqrt, pow


class Tween:

    def __init__(self, start=(0, 0), end=(0, 0), mode=None, speed=1):
        if mode is None:
            self.mode = Tween.lerp
        else:
            self.mode = mode

        x1, y1 = start
        x2, y2 = end
        self.start = list(start)
        self.end = list(end)
        self.cur = list(start)
        dist = self.distance(end, start)
        self.speed = speed  # fewer steps == faster animations
        # but watch for div by zero
        self.N = int(dist / self.speed)
        self.i = 0
        if self.i >= self.N or self.N == 0:
            self.finished = True
        else:
            self.finished = False

    @staticmethod
    def distance(a, b):
        x1, y1 = a
        x2, y2 = b
        return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

    def step(self):
        if self.finished:
            return
        self.i += 1
        self.mode(self)
        if self.cur == self.end or self.i >= self.N:
            self.finished = True

    def lerp(self):
        v = float(self.i) / self.N
        # print(v)
        for i in range(2):
            c = self.start[i] * (1 - v) + self.end[i] * v
            self.cur[i] = round(c)
        # print(self.cur)

    def smooth(self):
        v = float(self.i) / self.N
        v = pow(v, 2) * (3. - 2. * v)
        # print(v)
        for i in range(2):
            c = self.start[i] * (1 - v) + self.end[i] * v
            self.cur[i] = int(round(c))

    @staticmethod
    def SMOOTHERSTEP(x):
        # return ((x) * (x) * (x) * ((x) * ((x) * 6 - 15) + 10))
        return pow(x, 3) * (x * (6 * x - 15) + 10)

    def xsmooth(self):
        v = float(self.i) / self.N
        v = self.SMOOTHERSTEP(v)

        # print(v)
        for i in range(2):
            c = self.start[i] * (1 - v) + self.end[i] * v
            self.cur[i] = int(round(c))
