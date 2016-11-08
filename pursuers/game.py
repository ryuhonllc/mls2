#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import print_function
import pygame
import pygame.gfxdraw

from vidfeed import VidFeed

from OneD import Randicon  # TODO move to new file
from tween import Tween
from qedu import QL, StaticActionMap
from math import sqrt
from random import randint

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)
pprint = pp.pprint


def calc_dist(a, b):
    raise NotImplementedError("TODO")


class Grid():

    def __init__(self):
        self.grid_size = (8, 6)
        self.cell_size = (100, 100)
        self.left = 50
        self.top = 50
        self.vf = VidFeed()

    def get_img(self):
        """Convert cvimage into a pygame image"""
        img = self.vf.getFrame()
        s = img.tostring()
        return pygame.image.frombuffer(s, img.shape[1::-1], "RGB")

    def render(self, screen):
        w, h = self.grid_size
        ch, cw = self.cell_size
        left = self.left
        top = self.top

        bot = h * ch
        right = w * cw
        pygame.draw.rect(screen, (0, 0, 240),
                         (left, top, right, bot))
        frame = self.get_img()
        rect = frame.get_rect()
        rect[0] = 150
        rect[1] = 50
        print("rect", rect)
        screen.blit(frame, rect)

        for i in range(w + 1):
            pygame.draw.line(screen,
                             (0, 255, 0),
                             (left + i * cw, top), (left + i * cw, bot + top),
                             3
                             )
        for j in range(h + 1):
            pygame.draw.line(screen,
                             (0, 245, 0),
                             (left, top + j * ch), (
                                 left + right, top + j * ch),
                             3
                             )

sam = StaticActionMap(actions=[(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)])


def rfn(state, action):
    x, y = state
    dx, dy = sam[state][action]
    nx = x + dx
    ny = x + dy
    r = -sqrt(nx**2 + ny**2)
    print("rfn ({}) -> {}".format((nx, ny), r))
    return -r


class Sim():

    def __init__(self):
        self.winWidth = 900
        self.winHeight = 700
        self.screen = None
        self.bgcolor = (15, 0, 0)
        self.grid = Grid()
        self.ql = QL(actionMap=sam, rfn=rfn, epsilon=0.9)
        self.epsilon_decay = 0.99
        nTargets = 12
        self.nTargets = nTargets
        self.players = pygame.sprite.Group()
        for i in range(nTargets):
            r = Randicon()
            r.tween = self.set_dest()
            self.players.add(r)

    def initWindow(self):
        pygame.init()
        w = self.winWidth
        h = self.winHeight
        screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
        pygame.display.set_caption("Pursuers")
        self.screen = screen

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        return True

    def render(self):
        self.screen.fill(self.bgcolor)
        self.grid.render(self.screen)
        self.players.update()
        self.players.draw(self.screen)
        pygame.display.flip()

    def set_dest(self, old=None):
        ql = self.ql
        tw = 100
        left = self.grid.left
        top = self.grid.top
        gw = (self.winWidth - left * 2) / tw
        gh = (self.winHeight - top * 2) / tw
        if old is None:
            old = (randint(left, gw * tw), randint(top, gh * tw))
            print("initial", old)
        # print("gw", gw, "gh", gh)
        x, y = old
        x /= tw
        y /= tw
        aid = ql.act((x, y))
        dx, dy = sam[(x, y)][aid]
        x += dx
        y += dy
        # gotta be a way to dry this up
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > gw:
            x = gw
        if y > gh:
            y = gh
        x *= tw
        y *= tw
        x += left
        y += top
        x += randint(-5, 5)
        y += randint(-5, 5)
        t = Tween(old, (x, y), speed=1, mode=Tween.xsmooth)
        return t

    def doLogic(self):
        for p in self.players:
            if p.tween.finished:
                p.tween = self.set_dest(p.tween.cur)

    def mainLoop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(30)
            print(clock.get_fps())
            running = self.handleEvents()
            self.doLogic()
            self.render()


def main():

    sim = Sim()
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
