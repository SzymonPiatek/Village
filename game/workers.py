import pygame as pg
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from game.settings import configuration
from game.assets import assets


class Worker:
    def __init__(self, tile, world):
        self.config = configuration
        self.assets = assets
        self.world = world
        self.world.entities.append(self)
        self.name = "worker"
        image = self.assets[self.name]
        self.image = pg.transform.scale(image, (image.get_width()*2, image.get_height()*2))
        self.tile = tile
        self.speed = self.config["worker"]["speed"]

        self.world.workers[tile["grid"][0]][tile["grid"][1]] = self
        self.move_timer = pg.time.get_ticks()

        self.create_path()

    def create_path(self):
        searching_for_path = True
        while searching_for_path:
            x = random.randint(0, self.world.grid_length_x - 1)
            y = random.randint(0, self.world.grid_length_y - 1)
            dest_tile = self.world.world[x][y]
            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x, y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path_index = 0
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False

    def change_tile(self, new_tile):
        self.world.workers[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.workers[new_tile.x][new_tile.y] = self
        self.tile = self.world.world[new_tile.x][new_tile.y]

    def update(self):
        now = pg.time.get_ticks()
        if (now - self.move_timer) > (1000 // self.speed):
            new_pos = self.path[self.path_index]
            self.change_tile(new_pos)
            self.path_index += 1
            self.move_timer = now
            if self.path_index == len(self.path) - 1:
                self.create_path()
