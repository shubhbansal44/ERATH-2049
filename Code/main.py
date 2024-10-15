# IMPORTS
import pygame as pg
import sys
from settings import SCREEN_SETTINGS
from player import *
from map import *
from ray_casting import *
from renderer import *
from objects_handler import *
from weapons import *
from sounds import *
from pathfinding import *
from stats import *
from menu import *


class Game():
    def __init__(self):
        self.settings()
        pg.mouse.set_visible(True)
        self.SCREEN = pg.display.set_mode(self.screen_settings.RES, pg.RESIZABLE)
        self.global_flag = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 100)
        self.wasted = False
        self.win = False
        self.x_mode = False
        self.start = False
        self.game = False
        self.menu = Menu(self)

    def settings(self):
        self.screen_settings = SCREEN_SETTINGS()
        
    def new_game(self):
        pg.mouse.set_visible(False)
        self.wasted = False
        self.win = False
        self.map = Game_Map(self)
        self.renderer = Renderer(self)
        self.player = Player(self)
        self.raycast = Ray_Caster(self)
        self.objects_handler = Object_Handler(self)
        self.weapon = Weapons(self)
        self.sound = Sounds(self)
        self.path_finder = Path_Finder(self)
        self.stats = Stats(self)
        pg.display.set_caption('ERATH-2049')

    def update(self):
        if self.game:
            self.player.update()
            self.raycast.update()
            self.objects_handler.update()
            self.weapon.update()
            self.map.update()
            self.stats.update()
            pg.display.update()
        if self.menu.main_menu:
            self.menu.update()

    def draw(self):
        if self.game:
            self.draw_3D()
            self.draw_2D()
            self.draw_stats()
        elif self.wasted and not self.menu.main_menu:
            self.renderer.death()
        else:
            self.menu.draw()

    def draw_3D(self):
        self.renderer.render()  # 3D view
        if not self.x_mode:
            self.weapon.draw()  # first person weapon view

    def draw_2D(self):
        self.map.draw()  # map view
        self.player.draw()  # player view
        self.player.draw_health()

    def draw_stats(self):
        self.stats.draw()

    def events(self):
        self.global_flag = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit(0)
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not self.menu.pause and self.start:
                    if self.game or self.menu.menu or self.wasted or self.win:
                        self.menu.toggle_menu()
                        pg.mouse.set_visible(False)
                        if self.menu.main_menu:
                            pg.mouse.set_visible(True)
                            self.renderer.death_blit = self.renderer.win_blit = False
            if event.type == pg.KEYDOWN and event.key == pg.K_p and not self.menu.main_menu and not self.wasted:
                self.menu.toggle_pause()
            if (event.type == pg.KEYDOWN and event.key == pg.K_n):
                if self.wasted or self.menu.menu or self.win:
                    self.menu.menu = self.menu.main_menu = False
                    self.start = True
                    self.game = True
                    self.new_game()
            if not self.menu.pause and not self.menu.main_menu and event.type == self.global_event:
                self.global_flag = True

    def demolish(self):
        [object.dlt() for object in self.objects_handler.objects]
        [enemy.dlt() for enemy in self.objects_handler.enemies]

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()