import pygame as pg
import math
from settings import *


class ray_caster:
    def __init__(self,game):
        self.game=game

    def cast_rays(self):

        player_x, player_y=self.game.player.pos
        map_x, map_y=self.game.player.map_pos
        ray_angle=self.game.player.angle - H_FOV + .0001

        for rays in range(CASTED_RAYS):

            sin_a=math.sin(ray_angle)
            cos_a=math.cos(ray_angle)

            # horizontals
            y_hor, dy=(map_y+TILE_DIMENSIONS_Y,TILE_DIMENSIONS_Y) if sin_a>0 else (map_y-1e-6,-TILE_DIMENSIONS_Y)

            depth_hor=(y_hor-player_y)/sin_a
            x_hor=player_x+depth_hor*cos_a

            delta_depth=dy/sin_a
            dx=delta_depth*cos_a

            for depth in range(MAX_DEPTH):
                if (int(x_hor//TILE_DIMENSIONS_X),int(y_hor//TILE_DIMENSIONS_Y)) in self.game.map.world_map:
                    break
                x_hor+=dx
                y_hor+=dy
                depth_hor+=delta_depth

            # verticals
            x_vert, dx=(map_x+TILE_DIMENSIONS_X,TILE_DIMENSIONS_X) if cos_a>0 else (map_x-1e-6,-TILE_DIMENSIONS_X)

            depth_vert=(x_vert-player_x)/cos_a
            y_vert=player_y+depth_vert*sin_a
            
            delta_depth=dx/cos_a
            dy=delta_depth*sin_a

            for depth in range(MAX_DEPTH):
                if (int(x_vert//TILE_DIMENSIONS_X),int(y_vert//TILE_DIMENSIONS_Y)) in self.game.map.world_map:
                    break
                x_vert+=dx
                y_vert+=dy
                depth_vert+=delta_depth
            
            # required ray depth
            depth = min(depth_hor, depth_vert)

            # casting rays
            pg.draw.line(
                self.game.SCREEN,
                'white',
                (player_x,player_y),
                (player_x+depth*cos_a,player_y+depth*sin_a),
                2
            )

            ray_angle+=DELTA_ANGLE
                
                
    def update(self):
        self.cast_rays()