import pygame as pg
import sys
from game.world import World
from game.settings import *
from game.utils import draw_text
from game.camera import Camera
from game.hud import Hud
from game.resource_manager import ResourceManager
from game.workers import Worker


class Game:
    def __init__(self, screen, clock):
        self.config = configuration
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.entities = []

        self.resource_manager = ResourceManager()

        self.hud = Hud(
            resource_manager=self.resource_manager,
            width=self.width,
            height=self.height
        )
        self.world = World(
            resource_manager=self.resource_manager,
            entities=self.entities,
            hud=self.hud,
            grid_length_x=self.config["world_size"]["x"],
            grid_length_y=self.config["world_size"]["y"],
            width=self.width,
            height=self.height
        )

        for _ in range(self.config["worker"]["start_amount"]):
            Worker(
                tile=self.world.world[25][25],
                world=self.world
            )

        self.camera = Camera(
            width=self.width,
            height=self.height
        )

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(self.config["clock_speed"])
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
        for e in self.entities:
            e.update()

        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)

    def draw(self):
        self.screen.fill(self.config["color"]["black"])
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

        draw_text(
            screen=self.screen,
            text=f"FPS: {round(self.clock.get_fps())}",
            size=self.config["font_size"]["h4"],
            color=self.config["color"]["white"],
            pos=(10, 0)
        )

        pg.display.flip()
