import pygame as pg
from settings import *
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.fired = False
        self.health = MAX_HEALTH
        self.min_health = (MAX_HEALTH / 100) * 15 # 15%
        self.rel = 0
        self.supplements = (MAX_HEALTH / 100) * .01 # .01%
        self.view = False

    def in_view(self):
        key = pg.key.get_just_pressed()
        if (key[pg.K_h] and not self.view) or self.health <= self.min_health:
            self.view = True
        elif key[pg.K_h]:
            self.view = False

    def regenerate(self):
        if self.health < MAX_HEALTH:
            self.health += self.supplements

    def get_murdered(self):
        if self.health < 1:
            self.game.renderer.death()
            self.game.demolish()
            self.game.wasted = True
            pg.display.update()

    def get_hurt(self, damage):
        self.health -= damage
        self.game.renderer.blood()
        # self.game.sound.player_pain.play()
        self.get_murdered()

    def fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.fired and not self.game.weapon.reloading:
                self.game.sound.shotgun_fire.play()
                self.fired = True
                self.game.weapon.reloading = True

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
        scale = PLAYER_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.circle(
            self.game.SCREEN,
            'blue',
            ((WIDTH - TILE_X * TILE_DIMENSION_X) + self.x * TILE_DIMENSION_X, self.y * TILE_DIMENSION_Y),
            4
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
        self.regenerate()
        self.in_view()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)