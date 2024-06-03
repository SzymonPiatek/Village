import pygame as pg
from game.settings import configuration


class Camera:
    def __init__(self, width, height):
        self.config = configuration
        self.width = width
        self.height = height

        self.scroll = pg.Vector2(
            -(self.config["world_size"]["x"] * self.config["tile_size"] / 2 - self.width / 2),
            -(self.config["world_size"]["y"] * self.config["tile_size"] / 2 - self.height / 2)
        )
        self.dx = 0
        self.dy = 0
        self.speed = self.config["camera_speed"]

    def update(self):
        mouse_pos = pg.mouse.get_pos()

        if mouse_pos[0] > self.width * 0.97:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.03:
            self.dx = self.speed
        else:
            self.dx = 0

        if mouse_pos[1] > self.height * 0.97:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.03:
            self.dy = self.speed
        else:
            self.dy = 0

        self.scroll.x += self.dx
        self.scroll.y += self.dy
