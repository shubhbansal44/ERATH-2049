# imports
import pygame as pg
from os.path import join
from settings import *

class Renderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.SCREEN
        # self.base_path = os.path.dirname(os.path.abspath(__file__)).rsplit('\\', 1)[0]
        self.wall_textures = self.load_wall_textures()
        self.sky_images = [self.get_texture(join('Sources', 'sky', f'{i}.png'), (WIDTH, H_HEIGHT)) for i in range(1,6)]
        self.sky = 0
        self.pass_time = False
        self.duration = 720000
        self.time_prev = pg.time.get_ticks()
        # self.floor = self.get_texture(join('Sources', 'floors', '1.png'), (WIDTH, H_HEIGHT))
        self.blood_screen = self.get_texture(join('Sources', 'effects', 'blood', 'blood.png'), RES)
        self.death_screen = self.get_texture(join('Sources', 'effects', 'death', 'death.webp'), RES)
        self.digits_images = [self.get_texture(join('Sources', 'digits', f'{i}.png'), [DIGIT_SIZE] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digits_images))

    def blood(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def death(self):
        self.screen.blit(self.death_screen, (0, 0))

    def render(self):
        self.render_sky()
        self.render_floor()
        self.render_obstacles()
        self.render_health()

    def render_health(self):
        if self.game.player.view:
            health = str(int((self.game.player.health / MAX_HEALTH) * 100))
            for i, char in enumerate(health):
                self.screen.blit(self.digits[char], (10 + i * DIGIT_SIZE, 10))
            self.screen.blit(self.digits['10'], (10 + (i + 1) * DIGIT_SIZE, 10))

    def render_sky(self):
        self.time()
        self.sky = self.current_sky()
        self.sky_offset = (self.game.player.angle / math.tau * WIDTH) % WIDTH
        # self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_images[self.sky], (-self.sky_offset, 0))
        self.screen.blit(self.sky_images[self.sky], (-self.sky_offset + WIDTH, 0))

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
            FLOOR,
            (0, H_HEIGHT, WIDTH, H_HEIGHT)
        )

    def render_obstacles(self):
        obstacles = sorted(self.game.raycast.walls + self.game.raycast.objects, key=lambda x: x[0], reverse=True)
        for depth, image, pos in obstacles:
            self.screen.blit(image, pos)

    def render_objects(self):
        objects = sorted(self.game.raycast.objects, key=lambda x: x[0], reverse=True)
        for depth, image, pos in objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture(join('Sources', 'walls', '1.png')),
            2: self.get_texture(join('Sources', 'walls', '2.png')),
            3: self.get_texture(join('Sources', 'walls', '3.png')),
            4: self.get_texture(join('Sources', 'walls', '4.png')),
            5: self.get_texture(join('Sources', 'walls', '5.png')),
        }