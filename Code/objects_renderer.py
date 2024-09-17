# imports
import pygame as pg
from os.path import join
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.SCREEN
        self.wall_textures = self.load_wall_textures()
        self.sky = self.get_texture(join('Sources', 'sky', '1.png'), (WIDTH, H_HEIGHT))

    def render(self):
        self.render_background()
        self.render_walls()

    def render_background(self):
        # ceiling
        self.sky_offset = (self.game.player.angle / math.tau * WIDTH) % WIDTH
        # self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky, (-self.sky_offset, 0))
        self.screen.blit(self.sky, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(
            self.screen,
            FLOOR,
            (0, H_HEIGHT, WIDTH, H_HEIGHT)
        )

    def render_walls(self):
        walls = self.game.raycast.walls
        for depth, image, pos in walls:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture(join('Sources', 'walls', '1.png')),
            # 2: self.get_texture(join('Sources', 'wall-texture', '2.png'))
        }
