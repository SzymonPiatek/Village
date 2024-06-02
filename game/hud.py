import pygame as pg
from game.utils import draw_text


class Hud:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.hud_color = (198, 155, 93, 175)

        self.resources_surface = pg.Surface((width, height * 0.02), pg.SRCALPHA)
        self.resources_surface.fill(self.hud_color)

        self.build_surface = pg.Surface((width * 0.15, height * 0.25), pg.SRCALPHA)
        self.build_surface.fill(self.hud_color)

        self.select_surface = pg.Surface((width * 0.3, height * 0.2), pg.SRCALPHA)
        self.select_surface.fill(self.hud_color)

        self.images = self.load_images()
        self.tiles = self.create_build_hud()

        self.selected_tile = None

    def create_build_hud(self):
        render_pos = [self.width * 0.84 + 10, self.height * 0.74 + 10]
        object_width = self.build_surface.get_width() // 5

        tiles = []

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
                    "rect": rect
                }
            )

            render_pos[0] += image_scale.get_width() + 10

        return tiles

    def update(self):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:
                    self.selected_tile = tile

    def draw(self, screen):
        if self.selected_tile is not None:
            img = self.selected_tile["image"].copy()
            img.set_alpha(100)
            screen.blit(img, pg.mouse.get_pos())

        screen.blit(self.resources_surface, (0, 0))

        screen.blit(self.build_surface, (self.width * 0.84, self.height * 0.74))

        screen.blit(self.select_surface, (self.width * 0.35, self.height * 0.79))

        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"].topleft)

        pos = self.width - 400
        for resource in ["wood:", "stone:", "gold:"]:
            draw_text(screen, resource, 30, (255, 255, 255), (pos, 0))
            pos += 100

    def load_images(self):
        building1 = pg.image.load("assets/graphics/building01.png").convert_alpha()
        building2 = pg.image.load("assets/graphics/building02.png").convert_alpha()
        rock = pg.image.load("assets/graphics/rock.png").convert_alpha()
        tree = pg.image.load("assets/graphics/tree.png").convert_alpha()

        return {
            "building1": building1,
            "building2": building2,
            "tree": tree,
            "rock": rock
        }

    def scale_image(self, image, w=None, h=None):
        if (w is None) and (h is None):
            pass
        else:
            if h is None:
                scale = w / image.get_width()
                h = scale * image.get_height()
            elif w is None:
                scale = w / image.get_width()
                h = scale * image.get_height()
            else:
                pass

            image = pg.transform.scale(image, (int(w), int(h)))
        return image
