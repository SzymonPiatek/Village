import pygame as pg
from game.buildings import Lumbermill
from game.utils import draw_text, match_resource
from game.settings import configuration
from game.assets import assets


class HudComponent:
    def __init__(self, hud_width=0, hud_height=0, width=0, height=0, start_pos=(0, 0), color=configuration["color"]["black"]):
        self.hud_width = hud_width
        self.hud_height = hud_height
        self.width = width
        self.height = height
        self.start_pos = start_pos
        self.color = color

        self.create_surface()

    def create_surface(self):
        self.surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=self.start_pos)
        self.surface.fill(self.color)


class Hud:
    def __init__(self, resource_manager, width, height):
        self.config = configuration
        self.assets = assets
        self.width = width
        self.height = height

        self.resource_manager = resource_manager

        self.resources_hud = HudComponent(
            hud_width=self.width, hud_height=self.height,
            width=self.width, height=20,
            start_pos=(0, 0),
            color=self.config["color"]["hud"]
        )

        self.buildings_hud = HudComponent(
            hud_width=self.width, hud_height=self.height,
            width=300, height=300,
            start_pos=(self.width-300, self.height-300),
            color=self.config["color"]["hud"]
        )

        self.selected_tile_hud = HudComponent(
            hud_width=self.width, hud_height=self.height,
            width=500, height=300,
            start_pos=(0, self.height-300),
            color=self.config["color"]["hud"]
        )

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None
        self.examined_tile = None

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
        self.draw_examined_tile_hud(screen)
        self.draw_building_hud(screen)
        self.draw_resource_hud(screen)

    def create_build_hud(self):
        render_pos = [self.width - 300 + 10, self.height - 300 + 10]
        object_width = (self.buildings_hud.surface.get_width() - 40) // 3

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

    def draw_examined_tile_hud(self, screen):
        if self.examined_tile is not None:
            h = self.selected_tile_hud.height
            img = self.examined_tile.image.copy()
            img_scale = self.scale_image(img, h=h * 0.7)

            padding = int((h - img_scale.get_height()) // 2)
            new_width = img_scale.get_width() + padding * 2 + 300

            self.selected_tile_hud.width = new_width
            self.selected_tile_hud.create_surface()

            screen.blit(self.selected_tile_hud.surface, (0, self.height - 300))

            screen.blit(img_scale,
                        (self.selected_tile_hud.start_pos[0] + padding, self.selected_tile_hud.start_pos[1] + padding))

            draw_text(
                screen,
                self.examined_tile.display_name,
                self.config["font_size"]["h1"],
                self.config["color"]["white"],
                (self.selected_tile_hud.start_pos[0] + padding * 2 + img_scale.get_width(),
                 self.selected_tile_hud.start_pos[1] + int(padding // 4))
            )
            draw_text(
                screen,
                self.examined_tile.description,
                self.config["font_size"]["h4"],
                self.config["color"]["white"],
                (self.selected_tile_hud.start_pos[0] + padding * 2 + img_scale.get_width(),
                 self.selected_tile_hud.start_pos[1] + int(padding // 4) + padding)
            )
            if self.examined_tile.resource:
                draw_text(
                    screen,
                    self.examined_tile.generate_efficiency(),
                    self.config["font_size"]["h4"],
                    self.config["color"]["white"],
                    (self.selected_tile_hud.start_pos[0] + padding * 2 + img_scale.get_width(),
                     self.selected_tile_hud.start_pos[1] + int(padding // 4) + padding * 2)
                )
            elif self.examined_tile.resources:
                i = 3
                for resource, resource_amount in self.examined_tile.resources.items():
                    draw_text(
                        screen,
                        f"{resource}: {resource_amount}",
                        self.config["font_size"]["h4"],
                        self.config["color"]["white"],
                        (self.selected_tile_hud.start_pos[0] + padding * 2 + img_scale.get_width(),
                         self.selected_tile_hud.start_pos[1] + int(padding // 4) + padding * i)
                    )
                    i += 1

    def draw_resource_hud(self, screen):
        screen.blit(self.resources_hud.surface, (0, 0))
        pos = self.width - 400
        for resource, resource_value in self.resource_manager.resources.items():
            txt = match_resource(resource) + ": " + str(resource_value)
            draw_text(
                screen,
                txt.capitalize(),
                self.config["font_size"]["h3"],
                self.config["color"]["white"],
                (pos, 0)
            )
            pos += 150

    def draw_building_hud(self, screen):
        screen.blit(self.buildings_hud.surface, (self.width - 300, self.height - 300))

        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)

    def load_images(self):
        images = {
            "lumbermill": self.assets["lumbermill"].convert_alpha(),
            "stonemasonry": self.assets["stonemasonry"].convert_alpha(),
            "warehouse": self.assets["warehouse"].convert_alpha()
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
