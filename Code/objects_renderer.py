# imports
import pygame as pg
from os.path import join
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.SCREEN
        self.wall_textures = self.load_wall_textures()

    def draw_walls(self):
        self.render_objects()

    def render_objects(self):
        objects = self.game.raycast.objects
        for depth, image, pos in objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture(join('Sources', 'wall-texture', '1.png')),
            # 2: self.get_texture(join('Sources', 'wall-texture', '2.png'))
        }
