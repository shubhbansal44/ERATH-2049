# IMPORTS
import pygame as pg
import sys
from settings import *
from player import *
from map import *
from ray_casting import *
from renderer import *
from objects_handler import *
from weapons import *
from sounds import *
from pathfinding import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.clock = pg.time.Clock()
        self.SCREEN = pg.display.set_mode(RES, pg.RESIZABLE)
        self.delta_time = 1
        self.global_flag = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 80)
        self.new_game()
        self.wasted = False

    def new_game(self):
        self.map = Game_Map(self)
        self.player = Player(self)
        self.renderer = Renderer(self)
        self.raycast = Ray_Caster(self)
        self.objects_handler = Object_Handler(self)
        self.weapon = Weapons(self)
        self.sound = Sounds(self)
        self.path_finder = Path_Finder(self)
        self.wasted = False

    def update(self):
        if not self.wasted:
            self.player.update()
            self.raycast.update()
            self.objects_handler.update()
            self.weapon.update()
            self.map.update()
            pg.display.update()
            self.delta_time = self.clock.tick(FPS)
            pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw_3D(self):
        if not self.wasted:
            self.renderer.render()  # 3D view
            self.weapon.draw()  # first person weapon view

    def draw_2D(self):
        if not self.wasted and self.map.view:
            self.map.draw()  # map view
            self.player.draw()  # player view

    def events(self):
        self.global_flag = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)
            elif event.type == self.global_event:
                self.global_flag  = True
            elif self.wasted and event.type == pg.KEYDOWN and event.key == pg.K_e:
                self.new_game()
            self.player.fire_event(event)

    def demolish(self):
        [object.dlt() for object in self.objects_handler.objects]
        [enemy.dlt() for enemy in self.objects_handler.enemies]

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw_3D()
            self.draw_2D()


if __name__ == '__main__':
    game = Game()
    game.run()