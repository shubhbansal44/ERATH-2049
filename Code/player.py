import pygame as pg
from settings import *
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        key = pg.key.get_pressed()
        if key[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if key[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin

        # if key[pg.K_a]:
        #     dx += speed_sin
        #     dy += -speed_cos
        # if key[pg.K_d]:
        #     dx += -speed_sin
        #     dy += speed_cos

        self.collision_detection(dx, dy)

        if key[pg.K_a]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if key[pg.K_d]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau  # Keep the angle within 0 to 2π

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def collision_detection(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw_player(self):
        pg.draw.circle(
            self.game.SCREEN,
            (255, 0, 0),
            (self.x * TILE_X, self.y * TILE_Y),
            8
        )

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([H_WIDTH, H_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_RELATIVE, min(MOUSE_MAX_RELATIVE, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
