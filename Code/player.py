import pygame as pg
from settings import *
import math


class player:
    def __init__(self,game):
        self.game=game
        self.x, self.y=PLAYER_POS
        self.angle=PLAYER_ANGLE

    def movement(self):
        sin_a=math.sin(self.angle)
        cos_a=math.cos(self.angle)
        dx, dy=0, 0
        speed=PLAYER_SPEED*self.game.delta_time
        speed_sin=speed*sin_a
        speed_cos=speed*cos_a

        key=pg.key.get_pressed()
        if key[pg.K_w]:
            dx+=speed_cos
            dy+=speed_sin
        if key[pg.K_s]:
            dx+=-speed_cos
            dy+=-speed_sin
        # if key[pg.K_a]:
        #     dx+=speed_sin
        #     dy+=-speed_cos
        # if key[pg.K_d]:
        #     dx+=-speed_sin
        #     dy+=speed_cos

        self.collision_detection(dx,dy)

        if key[pg.K_a]:
            self.angle-=PLAYER_ROT_SPEED*self.game.delta_time
        if key[pg.K_d]:
            self.angle+=PLAYER_ROT_SPEED*self.game.delta_time
        self.angle%=math.tau

    def check_wall(self,x,y):
        return (x,y) not in self.game.map.world_map
    
    def collision_detection(self,dx,dy):
        if self.check_wall(int(self.x+dx),int(self.y)):
            self.x+=dx
        if self.check_wall(int(self.x),int(self.y+dy)):
            self.y+=dy

    def draw_player(self):
        pg.draw.circle(
            self.game.SCREEN,
            (255, 0, 0),
            (self.x*TILE_X,self.y*TILE_Y),
            8
        )

    def update(self):
        self.movement()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)