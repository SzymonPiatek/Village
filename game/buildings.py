import pygame as pg


class Lumbermill:
    def __init__(self, pos, resource_manager):
        self.image = pg.image.load("assets/graphics/lumbermill.png").convert_alpha()
        self.name = "lumbermill"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources["wood"] += 1
            self.resource_cooldown = now


class Stonemasonry:
    def __init__(self, pos, resource_manager):
        self.image = pg.image.load("assets/graphics/stonemasonry.png").convert_alpha()
        self.name = "stonemasonry"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.resource_cooldown > 2000:
            self.resource_manager.resources["stone"] += 1
            self.resource_cooldown = now


class Warehouse:
    def __init__(self, pos, resource_manager):
        self.image = pg.image.load("assets/graphics/warehouse.png").convert_alpha()
        self.name = "warehouse"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
