import pygame as pg
from game.settings import configuration
from game.utils import match_resource
from game.assets import assets


class Building:
    def __init__(self, name=None, display_name=None, description=None, resource=None, resources=None, pos=None, resource_manager=None):
        self.config = configuration
        self.assets = assets
        self.name = name
        self.display_name = display_name
        self.description = description
        self.image = self.assets[name] if self.name else None
        self.rect = self.image.get_rect(topleft=pos)
        self.resource = resource
        self.resources = resources
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_cooldown = pg.time.get_ticks() if self.resource else 0
        self.efficiency = int(self.config["buildings"]["efficiency"][self.name])

    def generate_efficiency(self):
        return f"1 {match_resource(self.resource)} / {round((self.config["buildings"]["resource_cooldown"] / 1000 / self.efficiency), 2)} s"

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
            display_name="Chatka drwala",
            description="Produkuje drewno",
            resource="wood",
            pos=pos,
            resource_manager=resource_manager
        )


class Stonemasonry(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            name="stonemasonry",
            display_name="Kopalnia kamienia",
            description="Produkuje kamień",
            resource="stone",
            pos=pos,
            resource_manager=resource_manager
        )


class Warehouse(Building):
    def __init__(self, pos, resource_manager):
        super().__init__(
            name="warehouse",
            display_name="Magazyn",
            description="Magazynuje przedmioty",
            pos=pos,
            resources={
              "wood": 0,
              "stone": 0
            },
            resource_manager=resource_manager
        )
