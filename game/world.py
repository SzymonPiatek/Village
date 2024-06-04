import pygame as pg
import random
from perlin_noise import PerlinNoise
from game.settings import *
from game.buildings import Lumbermill, Stonemasonry, Warehouse
from game.assets import assets


class World:
    def __init__(self, resource_manager, entities, hud, grid_length_x, grid_length_y, width, height):
        self.config = configuration
        self.assets = assets
        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.perlin_scale = grid_length_x / 2
        self.noise = PerlinNoise(octaves=4, seed=random.randint(0, 100))

        self.grass_tiles = pg.Surface(
            (
                grid_length_x * self.config["tile_size"] * 2,
                grid_length_y * self.config["tile_size"] + 2 * self.config["tile_size"]
            )
        ).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.workers = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.temp_tile = None
        self.examine_tile = None

    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        self.temp_tile = None
        if self.hud.selected_tile is not None:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.is_valid_grid_pos(grid_pos) and self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }

                if mouse_action[0] and not collision and self.hud.selected_tile["affordable"]:
                    if self.hud.selected_tile["name"] in ["lumbermill", "stonemasonry", "warehouse"]:
                        if self.hud.selected_tile["name"] == "lumbermill":
                            ent = Lumbermill(render_pos, self.resource_manager)
                        elif self.hud.selected_tile["name"] == "stonemasonry":
                            ent = Stonemasonry(render_pos, self.resource_manager)
                        elif self.hud.selected_tile["name"] == "warehouse":
                            ent = Warehouse(render_pos, self.resource_manager)

                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent

                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.collision_matrix[grid_pos[1]][grid_pos[0]] = 0
        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.is_valid_grid_pos(grid_pos) and self.can_place_tile(grid_pos):
                building = self.buildings[grid_pos[0]][grid_pos[1]]

                if mouse_action[0] and (building is not None):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = building

    def is_valid_grid_pos(self, grid_pos):
        return 0 <= grid_pos[0] < self.grid_length_x and 0 <= grid_pos[1] < self.grid_length_y

    def draw(self, screen, camera):
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (self.tiles[tile].get_height() - self.config["tile_size"]) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline()
                            mask = [
                                (x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 y + render_pos[1] - (self.tiles[tile].get_height() - self.config["tile_size"]) + camera.scroll.y) for x, y in mask
                            ]
                            pg.draw.polygon(screen, self.config["color"]["white"], mask, 3)

                building = self.buildings[x][y]
                if building is not None:
                    screen.blit(building.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (building.image.get_height() - self.config["tile_size"]) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(building.image).outline()
                            mask = [
                                (x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 y + render_pos[1] - (building.image.get_height() - self.config["tile_size"]) + camera.scroll.y) for x, y in mask
                            ]
                            pg.draw.polygon(screen, self.config["color"]["white"], mask, 3)

                worker = self.workers[x][y]
                if worker is not None:
                    screen.blit(worker.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (worker.image.get_height() - self.config["tile_size"]) + camera.scroll.y))

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, self.config["color"]["red"], iso_poly, 3)
            else:
                pg.draw.polygon(screen, self.config["color"]["white"], iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - self.config["tile_size"]) + camera.scroll.y
                )
            )

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
            (grid_x * self.config["tile_size"], grid_y * self.config["tile_size"]),
            (grid_x * self.config["tile_size"] + self.config["tile_size"], grid_y * self.config["tile_size"]),
            (grid_x * self.config["tile_size"] + self.config["tile_size"], grid_y * self.config["tile_size"] + self.config["tile_size"]),
            (grid_x * self.config["tile_size"], grid_y * self.config["tile_size"] + self.config["tile_size"]),
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
            "tile": tile,
            "collision": False if tile == "" else True
        }

        return output

    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0
        return collision_matrix

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y)/2

        return iso_x, iso_y

    def mouse_to_grid(self, x, y, scroll):
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y

        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x

        grid_x = int(cart_x // self.config["tile_size"])
        grid_y = int(cart_y // self.config["tile_size"])

        return grid_x, grid_y

    def load_images(self):
        images = {
            "tree": self.assets["tree"].convert_alpha(),
            "rock": self.assets["rock"].convert_alpha(),
            "block": self.assets["block"].convert_alpha()
        }

        return images

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_hud.rect, self.hud.buildings_hud.rect, self.hud.selected_tile_hud.rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False
