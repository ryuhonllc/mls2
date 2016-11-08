

import unittest
from tween import Tween


class TestTween(unittest.TestCase):

    def testDone(self):
        t = Tween((0, 0), (0, 0))
        assert t.finished is True

    def testOneD(self):
        steps = 100
        t = Tween((0, 0), (steps, 0))

        assert t.N == steps, [t.N, steps]
        assert t.finished is False
        for i in range(steps):
            t.step()
            self.assertEqual(t.i, i + 1)
            self.assertEqual(t.cur[0], i + 1)

        assert t.finished is True
        self.assertEqual(i, steps - 1)

    def testClose(self):
        t = Tween((0, 0), (0, 2), mode=Tween.smooth, speed=3)
        self.assertEqual(t.N, 0)
        t.step()  # should not throw exception

    def testOffOrigin(self):
        t = Tween((4, 5), (16, 25),  speed=1)
        x = []
        xex = [5.0, 5.0, 6.0, 6.0, 7.0, 7.0, 8.0, 8.0,
               9.0, 9.0, 10.0, 10.0, 11.0, 11.0, 12.0,
               12.0, 13.0, 13.0, 14.0, 14.0, 15.0, 15.0, 16.0]
        y = []
        yex = [6.0, 7.0, 8.0, 8.0, 9.0, 10.0, 11.0,
               12.0, 13.0, 14.0, 15.0, 15.0, 16.0,
               17.0, 18.0, 19.0, 20.0, 21.0, 22.0,
               22.0, 23.0, 24.0, 25.0]
        while not t.finished:
            t.step()
            x.append(t.cur[0])
            y.append(t.cur[1])
        self.assertEqual(x, xex)
        self.assertEqual(y, yex)

    def testSmooth(self):
        steps = 100
        t = Tween((0, 0), (steps, 0), mode=Tween.smooth)
        expected = [0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 5, 5, 6, 7, 8,
                    9, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 22,
                    23, 24, 25, 27, 28, 30, 31, 32, 34, 35, 37, 38, 40,
                    41, 43, 44, 46, 47, 49, 50, 51, 53, 54, 56, 57, 59,
                    60, 62, 63, 65, 66, 68, 69, 70, 72, 73, 75, 76, 77,
                    78, 80, 81, 82, 83, 84, 85, 87, 88, 89, 90, 91, 91,
                    92, 93, 94, 95, 95, 96, 97, 97, 98, 98, 99, 99, 99,
                    100, 100, 100, 100, 100]

        x = []
        for i in range(steps):
            t.step()
            x.append(t.cur[0])
            # self.assertEqual(t.i, i + 1)
            # self.assertEqual(t.cur[0], i + 1)

        # print(x)
        # print(expected)
        self.assertEqual(x, expected)
