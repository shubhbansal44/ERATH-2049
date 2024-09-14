# imports
import pygame as pg
import sys
from settings import *
from player import *
from map import *
from raycasting import *


class Game:
    def __init__(self):
        pg.init()
        self.clock=pg.time.Clock()
        self.SCREEN=pg.display.set_mode(RES)
        self.delta_time=1
        self.new_game()

    def new_game(self):
        self.map=game_map(self)
        self.player=player(self)
        self.raycast=ray_caster(self)

    def update(self):
        self.player.update()
        self.raycast.update()
        pg.display.update()
        self.delta_time=self.clock.tick(FPS)/1000
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.SCREEN.fill('black')
        self.map.draw_map()
        self.player.draw_player()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game=Game()
    game.run()