import pygame as pg
from game.assets import assets
from game.settings import configuration


class ResourceManager:
    def __init__(self):
        self.config = configuration
        self.assets = assets
        self.resources = self.config["start_resources"]

        self.costs = {
            "lumbermill": self.assets["lumbermill"]["buy_cost"],
            "stonemasonry": self.assets["stonemasonry"]["buy_cost"],
            "warehouse": self.assets["warehouse"]["buy_cost"],
        }

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable
