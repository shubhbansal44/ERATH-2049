# IMPORTS
import pygame as pg
import sys
# import psutil as cpu
# import GPUtil as gpu
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
        self.stats_screen = pg.Surface((350, 200))
        self.stats_screen.fill((0, 0, 0))
        self.stats_screen.set_alpha(100)

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
        pg.display.set_caption('ERATH-2049')

    def update(self):
        if not self.wasted:
            self.player.update()
            self.raycast.update()
            self.objects_handler.update()
            self.weapon.update()
            self.map.update()
            pg.display.update()
            self.delta_time = self.clock.tick(MAX_FPS)

    def draw(self):
        self.draw_3D()
        self.draw_2D()
        self.draw_stats()

    def draw_3D(self):
        if not self.wasted:
            self.renderer.render()  # 3D view
            self.weapon.draw()  # first person weapon view

    def draw_2D(self):
        if not self.wasted and self.map.view:
            self.map.draw()  # map view
            self.player.draw()  # player view

    def draw_stats(self):
        if not self.wasted and self.raycast.stats_view:
            self.SCREEN.blit(self.stats_screen, (10, 10))
            FONT = pg.font.SysFont('', 30)
            LIVE_FPS = f'FPS: {self.clock.get_fps():.1f}'
            GAME_FPS = FONT.render(LIVE_FPS, True, (255, 2, 255))
            LIVE_SCREEN = f'SCREEN SIZE: {WIDTH} * {HEIGHT}'
            GAME_SCREEN = FONT.render(LIVE_SCREEN, True, (255, 2, 255))
            self.SCREEN.blit(GAME_FPS, (25, 25))
            self.SCREEN.blit(GAME_SCREEN, (25, 60))

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
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()