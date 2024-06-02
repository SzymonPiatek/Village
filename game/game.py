import pygame as pg
import sys
from game.world import World
from game.settings import *
from game.utils import draw_text
from game.camera import Camera
from game.hud import Hud


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.hud = Hud(self.width, self.height)
        self.world = World(self.hud, 100, 100, self.width, self.height)
        self.camera = Camera(self.width, self.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

        draw_text(
            screen=self.screen,
            text=f"FPS: {round(self.clock.get_fps())}",
            size=25,
            color=(255, 255, 255),
            pos=(10, 0)
        )

        pg.display.flip()
