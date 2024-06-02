import pygame as pg
import random
from perlin_noise import PerlinNoise
from game.settings import *


class World:
    def __init__(self, grid_length_x, grid_length_y, width, height):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.perlin_scale = self.grid_length_x / 2
        self.noise = PerlinNoise(octaves=4, seed=random.randint(0, 100))

        self.grass_tiles = pg.Surface(
            (self.grid_length_x * TILE_SIZE * 2,
             self.height * TILE_SIZE + 2 * TILE_SIZE)
        ).convert_alpha()
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
                    (
                        render_pos[0] + self.grass_tiles.get_width() / 2,
                        render_pos[1]
                    )
                )

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
        perlin = self.noise([grid_x / self.perlin_scale, grid_y / self.perlin_scale])

        if (perlin >= 0.15) or (perlin <= -0.35):
            tile = "tree"
        else:
            if r <= 1:
                tile = "tree"
            elif r <= 2:
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
        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        rock = pg.image.load("assets/graphics/rock.png").convert_alpha()
        tree = pg.image.load("assets/graphics/tree.png").convert_alpha()

        return {
            "block": block,
            "tree": tree,
            "rock": rock
        }
