import pygame as pg
from game.game import Game
from game.settings import configuration


def main():
    running = True
    playing = True

    pg.init()
    pg.mixer.init()

    if configuration["fullscreen"]:
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode((1200, 1200))
    clock = pg.time.Clock()

    game = Game(screen, clock)

    while running:
        while playing:
            game.run()


if __name__ == "__main__":
    main()
