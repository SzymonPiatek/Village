import pygame as pg


assets_dir = "assets/"
graphics_dir = assets_dir + "graphics/"

assets = {
    "lumbermill": {
        "image": pg.image.load(f"{graphics_dir}lumbermill.png"),
        "display_name": "Chatka drwala",
        "description": "Produkuje drewno",
        "buy_cost": {
            "wood": 7,
            "stone": 3
        },
        "resource": "wood",
        "efficiency": 2,
    },
    "stonemasonry": {
        "image": pg.image.load(f"{graphics_dir}stonemasonry.png"),
        "display_name": "Kopalnia kamienia",
        "description": "Produkuje kamień",
        "buy_cost": {
            "wood": 3,
            "stone": 5
        },
        "resource": "stone",
        "efficiency": 2,
    },
    "warehouse": {
        "image": pg.image.load(f"{graphics_dir}warehouse.png"),
        "display_name": "Magazyn",
        "description": "Przechowuje surowce",
        "buy_cost": {
            "wood": 5,
            "stone": 5
        },
        "resource": None,
        "efficiency": None,
    },
    "worker": {
        "image": pg.image.load(f"{graphics_dir}worker.png"),
        "display_name": "Robotnik",
        "speed": 2,
    },
    "block": {
        "image": pg.image.load(f"{graphics_dir}block.png"),
        "display_name": "Trawa",
    },
    "rock": {
        "image": pg.image.load(f"{graphics_dir}rock.png"),
        "display_name": "Kamień",
    },
    "tree": {
        "image": pg.image.load(f"{graphics_dir}tree.png"),
        "display_name": "Drzewo",
    },
}
