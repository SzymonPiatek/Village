import pygame as pg
from game.settings import *


class Building:
    def __init__(self, name=None, resource=None, pos=None, resource_manager=None):
        self.config = configuration
        self.name = name
        self.image = pg.image.load(f"assets/graphics/{self.name}.png").convert_alpha() if self.name else None
        self.rect = self.image.get_rect(topleft=pos)
        self.resource = resource
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks() if self.resource else 0
        self.efficiency = self.config["buildings"]["efficiency"][self.name]

    def update(self):
        if self.resource:
            now = pg.time.get_ticks()
            if (now - self.resource_cooldown) > (self.config["buildings"]["resource_cooldown"] / self.efficiency):
                self.resource_manager.resources[self.resource] += 1
                self.resource_cooldown = now


class Lumbermill(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            name="lumbermill",
            resource="wood",
            pos=pos,
            resource_manager=resource_manager
        )


class Stonemasonry(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            name="stonemasonry",
            resource="stone",
            pos=pos,
            resource_manager=resource_manager
        )


class Warehouse(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            name="warehouse",
            pos=pos,
            resource_manager=resource_manager
        )
