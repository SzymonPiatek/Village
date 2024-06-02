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

        self.world = World(100, 100, self.width, self.height)

        self.camera = Camera(self.width, self.height)

        self.hud = Hud(self.width, self.height)

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

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.world.grass_tiles, (self.camera.scroll.x, self.camera.scroll.y))

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                render_pos = self.world.world[x][y]["render_pos"]

                tile = self.world.world[x][y]["tile"]
                if tile != "":
                    self.screen.blit(
                        self.world.tiles[tile],
                        (render_pos[0] + self.world.grass_tiles.get_width() / 2 + self.camera.scroll.x,
                         render_pos[1] - (self.world.tiles[tile].get_height() - TILE_SIZE) + self.camera.scroll.y))

        self.hud.draw(self.screen)

        draw_text(
            screen=self.screen,
            text=f"FPS: {round(self.clock.get_fps())}",
            size=25,
            color=(255, 255, 255),
            pos=(10, 10)
        )

        pg.display.flip()
