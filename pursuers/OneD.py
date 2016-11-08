#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import pygame
import pygame.gfxdraw
import icon_supp
from tween import Tween
from random import randint

from qedu import QL, StaticActionMap

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)
pprint = pp.pprint


class LineSegment():

    def __init__(self, length, ticks=5, seg_color=None):
        self.length = length
        self.thickness = 3
        self.ticks = ticks
        if seg_color is not None:
            self.seg_color = seg_color

    def seg_color(self, i):
        r = int(i * 255. / self.ticks)
        return (r, 10, 255)

    def render(self, screen):

        left = 0
        top = 0
        bot = self.thickness
        screen.fill((20, 80, 10))
        top = screen.get_height() / 2
        left = 0
        right = screen.get_width() - left * 2
        bot = self.thickness
        # self.draw_tick(screen, left)
        # self.draw_tick(screen, right + left - 2)
        spacing = int(screen.get_width() / self.ticks)
        for i in range(self.ticks):
            color = self.seg_color(i)
            self.draw_tick(screen, spacing * i, color)
            pygame.draw.rect(screen, color,
                             (spacing * i, top, spacing, bot))
        # print("{} / {} = {}, last at {}".format(
        #    screen.get_width(), self.ticks, spacing, spacing * i))
        # slightly off, but otherwise the last tick goes off surface
        color = self.seg_color(i + 1)
        self.draw_tick(screen, right - self.thickness, color)

    def draw_tick(self, screen, x, color):
        tick_height = self.thickness * 2
        top = screen.get_height() / 2 - tick_height
        left = x
        right = self.thickness
        bot = tick_height
        pygame.draw.rect(screen, color,
                         (left, top, right, bot))


class Randicon(pygame.sprite.Sprite):

    def __init__(self):
        super(Randicon, self).__init__()
        side = 5
        mult = 4
        self.width = 5 * mult
        self.height = 5 * mult
        self.mult = mult
        self.colors = icon_supp.randrange(side)
        self.matrix = icon_supp.gen_matrix(side * side)
        # matrix = [x % len(self.colors) for x in range(side * side)]
        # self.matrix = icon_supp.reshape(matrix, side)
        self.base = 0
        self.side = side

    def update(self):
        self.base += 1
        self.base = self.base % (len(self.colors))

    def draw(self):
        m = self.mult
        screen = pygame.Surface((self.side * m, self.side * m))
        # screen.fill(self.colors[self.base])
        for i in range(self.side):
            for j in range(self.side):
                cidx = (self.matrix[i][j] + self.base) % len(self.colors)
                color = self.colors[cidx]

                screen.fill(color, ((i * m, j * m), (m, m)))

        return screen

    @property
    def rect(self):
        """
        if rect is being called, it is expected
        to know it's position
        """
        r = self.cached_img.get_rect()
        self.tween.step()
        for i in range(2):
            r[i] = self.tween.cur[i]
        return r

    @property
    def image(self):
        img = self.draw()
        self.cached_img = img
        return img


class Sim():

    def __init__(self, width=1000, height=300, agent=None):
        self.width = width
        self.height = height
        self.winWidth = width
        self.winHeight = height
        self.screen = None
        self.bgcolor = (15, 0, 0)
        self.ticks = 10
        self.grid = LineSegment(length=width - 80, ticks=self.ticks)
        self.ql = agent
        self.left = 25
        self.top = 25

        self.tween = Tween((self.left, self.top),
                           (self.winWidth * 2 / 3 - self.left * 2,
                            self.winHeight - self.top * 2),
                           speed=3)

        self.players = pygame.sprite.Group()
        # self.players.add(Pursuer(self.mgr, 0))

    def initWindow(self):
        pygame.init()
        w = self.winWidth
        h = self.winHeight
        screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
        pygame.display.set_caption("Pursuers")
        self.screen = screen
        self.sub = self.gen_background()
        self.sample = Randicon()

    def gen_background(self):
        left = self.left
        top = self.top
        screen = pygame.Surface(
            (self.winWidth - left * 2, self.winHeight - top * 2))
        self.grid.render(screen)
        return screen

    def update_ploc(self):
        self.tween.step()
        self.pos = self.tween.cur
        x = 5
        if self.tween.finished:  # FIXME prevent cycles blocking user input
            pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        else:
            self.pos[0] += randint(-x, x)
            self.pos[1] += randint(-x, x)

    def rand_pos(self):
        newx = randint(self.left, self.winWidth - 20 - self.left)
        newy = randint(self.top, self.winHeight - 20 - self.top)
        return (newx, newy)

    def set_dest(self, pos):
        self.tween = Tween(self.tween.cur, pos, mode=Tween.xsmooth)

    def update_agent(self):
        x = self.tween.cur[0]
        game_width = self.winWidth - self.left * 2.
        state = (x - self.left * 2) / game_width * self.ticks
        state = int(round(state))
        y = self.winHeight / 2
        aid = self.ql.act(state)
        action = self.ql.actionMap[state][aid]
        e = self.ql.epsilon
        print("x {} s {} aid {} act {} e {}".format(x, state, aid, action, e))
        dist = action * game_width / self.ticks
        x += dist
        if x < 0:
            x = 0
        if x > self.winWidth:
            x = self.winWidth - self.left * 2
        # print("dist {}, x' {}".format(dist, x))
        if abs(dist) < 4:
            _, y = self.rand_pos()
        self.set_dest((x, y))

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
            elif event.type == pygame.MOUSEBUTTONUP:
                print("click")
                self.set_dest(pygame.mouse.get_pos())
                return True
            elif event.type == pygame.USEREVENT:
                self.update_agent()
                return True
        return True

    def render(self):
        self.screen.fill(self.bgcolor)
        self.sub = self.gen_background()
        self.screen.blit(self.sub, (self.left, self.top))
        # rec = self.screen.get_rect(center=(10, 10))
        self.players.update()
        self.sample.update()
        self.players.draw(self.screen)
        self.screen.blit(self.sample.draw(), self.pos)
        pygame.display.flip()

    def mainLoop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(500)
            running = self.handleEvents()
            self.update_ploc()
            self.render()


sam = StaticActionMap(actions=[-1, 0, 1])


def rfn(state, action):
    v = sam[state][action]
    sprime = state + v
    # print("in rfn ({}, {}) -> {}".format(state, action, sprime))
    return -abs(sprime)


class QSegColor():

    def __init__(self, lineseg, ql):
        self.lineseg = lineseg
        self.ql = ql
        self.ticks = dict()

    def seg_color(self, i):
        a = self.ql.bestNoRand(i)
        q = self.ql.getQ(i, a)
        self.ticks[i] = q
        if a == -1:
            return (0, 0, 0)
        l = min(self.ticks.values())
        h = max(self.ticks.values())
        interval = h - l
        q = q - l
        l = 0
        if interval is 0:
            r = 0
        else:
            r = int((q) * 255. / interval)
        # print("l {} h {} q {} r {}".format(l, interval, q, r))
        b = int(128 - r / 2)
        return (r, 0, 255 - b)


def main():

    agent = QL(alpha=1, actionMap=sam, rfn=rfn, epsilon=0.9)
    agent.epsilon_decay = 0.99
    sim = Sim(agent=agent)
    qsc = QSegColor(sim.grid, agent)
    sim.grid.seg_color = qsc.seg_color
    sim.initWindow()
    try:
        sim.mainLoop()
    except pygame.error:
        pass
    except KeyboardInterrupt:
        pass
    print("stats: random")
    pprint(sim.ql.rand_count)
    print("stats: policy")
    pprint(sim.ql.policy_count)
    pprint(["epsilon", sim.ql.epsilon])

if __name__ == "__main__":
    main()
