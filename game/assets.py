import pygame as pg

assets_dir = "assets/"
graphics_dir = assets_dir + "graphics/"

assets = {
    "lumbermill": pg.image.load(f"{graphics_dir}lumbermill.png"),
    "stonemasonry": pg.image.load(f"{graphics_dir}stonemasonry.png"),
    "warehouse": pg.image.load(f"{graphics_dir}warehouse.png"),
    "worker": pg.image.load(f"{graphics_dir}worker.png"),
    "block": pg.image.load(f"{graphics_dir}block.png"),
    "rock": pg.image.load(f"{graphics_dir}rock.png"),
    "tree": pg.image.load(f"{graphics_dir}tree.png"),
}
