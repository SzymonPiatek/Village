import pygame as pg


class Lumbermill:
    def __init__(self, pos):
        self.image = pg.image.load("assets/graphics/building01.png")
        self.name = "lumbermill"
        self.rect = self.image.get_rect(topleft=pos)
        self.counter = 0

    def update(self):
        self.counter += 1


class Stonemasonry:
    def __init__(self, pos):
        self.image = pg.image.load("assets/graphics/building02.png")
        self.name = "stonemasonry"
        self.rect = self.image.get_rect(topleft=pos)
        self.counter = 0

    def update(self):
        self.counter += 1
