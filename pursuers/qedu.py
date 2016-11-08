
from collections import defaultdict
import numpy as np

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)
pprint = pp.pprint

# all states have the same actions


class StaticActionMap(object):  # should it be a dict?

    def __init__(self, actions):
        self.actionMap = actions

    def __getitem__(self, state):
        """
        since this is a static action map
        all states return the same action
        """
        return self.actionMap

    def __len__(self):
        return len(self.actionMap)


class QL:

    def __init__(self, alpha=1.,
                 gamma=0., epsilon=0.999,
                 actionMap=None,
                 rfn=None):
        """
        alpha: learning rate
        gamma: decay of propagation
        actionMap: function returning actions available for a given state
        rfn: function return reward for a given state/action combo
        """

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = 0.999999
        self.rand_count = defaultdict(int)
        self.policy_count = defaultdict(int)
        self.rfn = rfn
        self.actionMap = actionMap
        # [
        #     (-1, 0),
        #     (1, 0),
        #     (0, 1),
        #     (0, -1),
        # (1, 1),
        # (1, -1),
        # (-1, 1),
        # (-1, -1),
        # ]
        self.table = dict()

    def getReward(self, percept, action):
        return self.rfn(percept, action)

    # for sampling
    def bestNoRand(self, percept):  # FIXME naming
        bi = -1
        bv = float('-inf')
        for q, v in self.table.iteritems():
            if q[0] != percept:
                continue
            if v > bv:
                bi = q[1]
                bv = v
        return bi

    def bestAction(self, percept):
        bi = self.bestNoRand(percept)
        if bi == -1 or np.random.rand() < self.epsilon:
            self.epsilon *= self.epsilon_decay
            bi = np.random.randint(0, len(self.actionMap))
            self.rand_count[bi] += 1
            # print("random bi", bi)
        else:
            self.policy_count[bi] += 1
        return bi

    def getQ(self, s, a):
        q = self.table.get((s, a))
        if q is None:
            return 0
        return q

    def transition(self, s, aid):
        v = np.array(self.actionMap[s][aid]) * 1
        sprime = s + v
        # print("s", s, "v", v, "s'", sprime)
        if isinstance(sprime, np.int64):
            return int(sprime)
        else:
            return tuple(sprime)

    def act(self, percept):
        action = self.bestAction(percept)
        # now get reward
        R = self.getReward(percept, action)
        # pprint(["result", percept, action, R])
        oldq = self.getQ(percept, action)
        sprime = self.transition(percept, action)
        # sprime = tuple(percept + self.actionVector(action))
        aprime = self.bestAction(sprime)
        qprime = self.getQ(sprime, aprime)
        a = self.alpha
        g = self.gamma
        newq = (1 - a) * oldq + a * (R + g * qprime)
        self.table[percept, action] = newq
        # force = np.round(5 * (v / np.linalg.norm(v)))
        return action
