
import unittest
import icon_supp


class TestColor(unittest.TestCase):

    def setUp(self):
        pass

    def testAscend(self):
        expected = 20
        colors = icon_supp.randrange(expected)
        n = len(colors)
        self.assertEqual(n, expected)
        first = colors[0]
        nf = len(first)
        self.assertEqual(nf, 3)
        prev = [-1, -1, -1]
        failed = False
        bade = None
        badf = None
        for _, e in enumerate(colors):
            for i in range(3):
                if e[i] < prev[i]:
                    failed = True
                    bade = e
                    badf = prev
                    break
            prev = e
        self.assertFalse(failed, msg="{} < {}".format(bade, badf))

    def testReshape(self):
        s = 5
        x = list(range(s * s))
        # print(x)
        box = icon_supp.reshape(x, s)
        nr = len(box)
        nc = len(box[0])
        # print(box[-1])
        self.assertEqual(nr, s)
        self.assertEqual(nc, s)

    def testSubList(self):
        s = 5
        c = icon_supp.randrange(s * s)
        box = icon_supp.reshape(c, s)
        self.assertEqual(len(box[0]), s)
        self.assertEqual(len(box[0][0]), 3)

    def testIndexed(self):
        s = 5
        icon = icon_supp.gen_matrix(s)
        self.assertEqual(len(icon[0]), s)
