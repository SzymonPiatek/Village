import pygame as pg
from game.assets import assets


def draw_text(screen, text, size, color, pos):
    font = pg.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=pos)

    screen.blit(text_surface, text_rect)


def match_resource(resource):
    match resource:
        case "wood": return "Drewno"
        case "stone": return "Kamień"
