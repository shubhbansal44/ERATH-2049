# imports
import pygame as pg
from os.path import join
import math
from settings import SCREEN_SETTINGS, TEXTURE_SETTINGS

class Renderer():
    def __init__(self, game):
        self.settings()
        self.game = game
        self.screen = game.SCREEN
        # self.base_path = os.path.dirname(os.path.abspath(__file__)).rsplit('\\', 1)[0]
        self.wall_textures = self.load_wall_textures()
        self.sky_images = [self.get_texture(join('Sources', 'sky', f'{i}.png'), (self.screen_settings.WIDTH, self.screen_settings.H_HEIGHT)) for i in range(1,6)]
        self.sky = 0
        self.pass_time = False
        self.duration = 360000
        self.time_prev = pg.time.get_ticks()
        # self.floor = self.get_texture(join('Sources', 'floors', '1.png'), (WIDTH, H_HEIGHT))
        self.blood_screen = self.get_texture(join('Sources', 'effects', 'blood', 'blood.png'), self.screen_settings.RES)
        self.death_screen = self.get_texture(join('Sources', 'effects', 'death', 'death.jpg'), self.screen_settings.RES)
        self.death_blit = False
        self.win_blit = False

    def settings(self):
        self.screen_settings = SCREEN_SETTINGS()
        self.texture_settings = TEXTURE_SETTINGS()

    def blood(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def death(self):
        if not self.death_blit:
            self.screen.blit(self.death_screen, (0, 0))
            self.death_blit = True
            pg.display.update()

    def render(self):
        self.render_sky()
        self.render_floor()
        if not self.game.x_mode:
            self.render_obstacles()

    def render_sky(self):
        self.time()
        self.sky = self.current_sky()
        self.sky_offset = (self.game.player.angle / math.tau * self.screen_settings.WIDTH) % self.screen_settings.WIDTH
        # self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_images[self.sky], (-self.sky_offset, 0))
        self.screen.blit(self.sky_images[self.sky], (-self.sky_offset + self.screen_settings.WIDTH, 0))

    def time(self):
        time_now = pg.time.get_ticks()
        if (time_now - self.time_prev > self.duration) and not self.pass_time:
            self.time_prev = time_now
            self.pass_time = True

    def current_sky(self):
        if self.pass_time:
            self.pass_time = False
            return int((self.sky + 1) % len(self.sky_images))
        return self.sky

    def render_floor(self):
        pg.draw.rect(
            self.screen,
            self.texture_settings.FLOOR,
            (0, self.screen_settings.H_HEIGHT, self.screen_settings.WIDTH, self.screen_settings.H_HEIGHT)
        )

    def render_obstacles(self):
        obstacles = sorted(self.game.raycast.walls + self.game.raycast.objects + self.game.raycast.enemies, key=lambda x: x[0], reverse=True)
        for depth, image, pos in obstacles:
            self.screen.blit(image, pos)

    def render_enemies(self):
        objects = sorted(self.game.raycast.enemies, key=lambda x: x[0], reverse=True)
        for depth, image, pos in objects:
            self.screen.blit(image, pos)

    def get_texture(self, path, res=(None)):
        texture = pg.image.load(path).convert_alpha()
        if res==None:
            res = (self.texture_settings.TEXTURE_SIZE, self.texture_settings.TEXTURE_SIZE)
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture(join('Sources', 'walls', '1.png')),
            2: self.get_texture(join('Sources', 'walls', '2.png')),
            3: self.get_texture(join('Sources', 'walls', '3.png')),
            4: self.get_texture(join('Sources', 'walls', '4.png')),
            5: self.get_texture(join('Sources', 'walls', '5.png')),
        }