import pygame as pg
import random
from game.settings import *


class World:
    def __init__(self, grid_length_x, grid_length_y, width, height):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.grass_tiles = pg.Surface((self.width, self.height))
        self.tiles = self.load_images()
        self.world = self.create_world()

    def create_world(self):
        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(
                    self.tiles["block"],
                    (render_pos[0] + self.width / 2,
                     render_pos[1] + self.height / 4))

        return world

    def grid_to_world(self, grid_x, grid_y):
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        min_x = min([x for x, y in iso_poly])
        min_y = min([y for x, y in iso_poly])

        r = random.randint(1, 100)

        if r <= 5:
            tile = "tree"
        elif r <= 10:
            tile = "rock"
        else:
            tile = ""

        output = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [min_x, min_y],
            "tile": tile
        }

        return output

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2
        return iso_x, iso_y

    def load_images(self):
        block = pg.image.load("assets/graphics/block.png")
        rock = pg.image.load("assets/graphics/rock.png")
        tree = pg.image.load("assets/graphics/tree.png")

        return {
            "block": block,
            "tree": tree,
            "rock": rock
        }
