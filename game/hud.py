import pygame as pg

from game.buildings import Lumbermill
from game.utils import draw_text
from game.settings import configuration


class Hud:
    def __init__(self, resource_manager, width, height):
        self.config = configuration
        self.width = width
        self.height = height

        self.resource_manager = resource_manager

        self.hud_colour = self.config["color"]["hud"]

        self.resources_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resources_rect = self.resources_surface.get_rect(topleft=(0, 0))
        self.resources_surface.fill(self.hud_colour)

        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_rect = self.build_surface.get_rect(topleft=(self.width * 0.85, self.height * 0.75))
        self.build_surface.fill(self.hud_colour)

        self.select_surface = pg.Surface((width * 0.3, height * 0.25), pg.SRCALPHA)
        self.select_rect = self.select_surface.get_rect(topleft=(self.width * 0.35, self.height * 0.79))
        self.select_surface.fill(self.hud_colour)

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None

    def create_build_hud(self):
        render_pos = [self.width * 0.85 + 10, self.height * 0.75 + 10]
        object_width = self.build_surface.get_width() // 5

        tiles = []

        i = 0
        for image_name, image in self.images.items():
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True
                }
            )

            if i == 3:
                render_pos[0] = self.width * 0.85 + 10
                render_pos[1] += (image_scale.get_height() * 2)
                i = 0
            else:
                render_pos[0] += (image_scale.get_width() + 10)
                i += 1

        return tiles

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False

            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):
        self.draw_examined_tile(screen)
        self.draw_building_hud(screen)
        self.draw_resource_hud(screen)

    def draw_examined_tile(self, screen):
        if self.examined_tile is not None:
            w, h = self.select_rect.width, self.select_rect.height
            screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.75))
            img = self.examined_tile.image.copy()
            img_scale = self.scale_image(img, h=h*0.7)
            screen.blit(img_scale, (self.width * 0.35 + 40, self.height * 0.75 + 40))
            draw_text(screen, self.examined_tile.name.capitalize(), self.config["font_size"]["h1"], self.config["color"]["white"], self.select_rect.topleft)

    def draw_resource_hud(self, screen):
        screen.blit(self.resources_surface, (0, 0))
        pos = self.width - 400
        for resource, resource_value in self.resource_manager.resources.items():
            txt = resource + ": " + str(resource_value)
            draw_text(screen, txt.capitalize(), self.config["font_size"]["h3"], self.config["color"]["white"], (pos, 0))
            pos += 150

    def draw_building_hud(self, screen):
        screen.blit(self.build_surface, (self.width * 0.85, self.height * 0.75))

        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

    def load_images(self):
        lumbermill = pg.image.load("assets/graphics/lumbermill.png")
        stonemasonry = pg.image.load("assets/graphics/stonemasonry.png")
        warehouse = pg.image.load("assets/graphics/warehouse.png")

        images = {
            "lumbermill": lumbermill,
            "stonemasonry": stonemasonry,
            "warehouse": warehouse
        }

        return images

    def scale_image(self, image, w=None, h=None):
        if (w is None) and (h is None):
            pass
        elif h is None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w is None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image
