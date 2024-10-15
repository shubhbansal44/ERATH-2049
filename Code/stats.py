import pygame as pg
import psutil as cpu
import GPUtil as gpu
from settings import SCREEN_SETTINGS


class Stats():
    def __init__(self, game):
        self.settings()
        self.game = game
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.stats_screen = pg.Surface((350, 200))
        self.stats_screen.fill((0, 0, 0))
        self.stats_screen.set_alpha(80)
        self.stats_timer = False
        self.duration = 30000
        self.time_prev = pg.time.get_ticks()
        self.stats_view = False
        self.g_pressed = False

    def settings(self):
        self.screen_settings = SCREEN_SETTINGS()

    def stats(self):
        key = pg.key.get_pressed()
        if key[pg.K_g] and not self.g_pressed:
            self.stats_view = not self.stats_view
            self.g_pressed = True
        if not key[pg.K_g]:
            self.g_pressed = False

    def update(self):
        self.delta_time = self.clock.tick(self.screen_settings.MAX_FPS)
        self.stats()

    def draw(self):
        if not self.game.wasted and self.stats_view and not self.game.x_mode:
            self.game.SCREEN.blit(self.stats_screen, (10, 10))
            FONT = pg.font.SysFont('', 30)
            LIVE_FPS = f'FPS: {self.clock.get_fps():.1f}'
            GAME_FPS = FONT.render(LIVE_FPS, True, (255, 2, 255))
            LIVE_SCREEN = f'SCREEN SIZE: {self.screen_settings.WIDTH} * {self.screen_settings.HEIGHT}'
            GAME_SCREEN = FONT.render(LIVE_SCREEN, True, (255, 2, 255))
            self.game.SCREEN.blit(GAME_FPS, (25, 25))
            self.game.SCREEN.blit(GAME_SCREEN, (25, 60))