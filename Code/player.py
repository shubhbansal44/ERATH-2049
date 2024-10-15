import pygame as pg
from settings import PLAYER_SETTINGS, MAP_SETTINGS, CONTROL_SETTINGS, TEXTURE_SETTINGS
import math
from os.path import join


class Player():
    def __init__(self, game):
        self.settings()
        self.game = game
        self.x, self.y = self.player_settings.PLAYER_POS
        self.angle = self.player_settings.PLAYER_ANGLE
        self.fired = False
        self.health = self.player_settings.MAX_HEALTH
        self.min_health = (self.player_settings.MAX_HEALTH / 100) * 15 # 15%
        self.rel = 0
        self.supplements = (self.player_settings.MAX_HEALTH / 100) * .01 # .01%
        self.view = False
        self.digits_images = [self.game.renderer.get_texture(join('Sources', 'digits', f'{i}.png'), [self.texture_settings.DIGIT_SIZE] * 2) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digits_images))
        self.h_presssed = False

    def settings(self):
        self.player_settings = PLAYER_SETTINGS()
        self.map_settings = MAP_SETTINGS()
        self.control_settings = CONTROL_SETTINGS()
        self.texture_settings = TEXTURE_SETTINGS()

    def in_view(self):
        key = pg.key.get_pressed()
        if (key[pg.K_h] and not self.h_pressed) or self.health <= self.min_health:
            self.view = not self.view
            self.h_pressed = True
        if not key[pg.K_h]:
            self.h_pressed = False

    def regenerate(self):
        if self.health < self.player_settings.MAX_HEALTH:
            self.health += self.supplements

    def get_murdered(self):
        if self.health < 1:
            self.game.wasted = True
            self.game.game = False
            self.game.demolish()

    def get_hurt(self, damage):
        self.health -= damage
        self.game.renderer.blood()
        # self.game.sound.player_pain.play()
        self.get_murdered()

    def fire(self):
        if pg.mouse.get_pressed()[0] and not self.fired and not self.game.weapon.reloading:
            self.game.sound.shotgun_fire.play()
            self.fired = True
            self.game.weapon.reloading = True

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = self.player_settings.PLAYER_SPEED * self.game.stats.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        key = pg.key.get_pressed()
        if key[pg.K_w] or key[pg.K_UP]:
            dx += speed_cos
            dy += speed_sin
            if key[pg.K_LSHIFT]:
                dx += dx*1.5
                dy += dy*1.5
        if key[pg.K_s] or key[pg.K_DOWN]:
            dx += -speed_cos
            dy += -speed_sin

        self.collision_detection(dx, dy)

        if key[pg.K_a] or key[pg.K_LEFT]:
            self.angle -= self.player_settings.PLAYER_ROT_SPEED * self.game.stats.delta_time
        if key[pg.K_d] or key[pg.K_RIGHT]:
            self.angle += self.player_settings.PLAYER_ROT_SPEED * self.game.stats.delta_time
        self.angle %= math.tau  # Keep the angle within 0 to 2π

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def collision_detection(self, dx, dy):
        scale = self.player_settings.PLAYER_SCALE / self.game.stats.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        if self.game.map.view and not self.game.x_mode:
            pg.draw.circle(
                self.game.SCREEN,
                'blue',
                ((self.control_settings.WIDTH - self.map_settings.TILE_X * self.map_settings.TILE_DIMENSION_X) + self.x * self.map_settings.TILE_DIMENSION_X, self.y * self.map_settings.TILE_DIMENSION_Y),
                4
            )

    def draw_health(self):
        if self.view and not self.game.x_mode:
            health = str(int((self.game.player.health / self.player_settings.MAX_HEALTH) * 100))
            for i, char in enumerate(health):
                self.game.SCREEN.blit(self.digits[char], (10 + i * self.texture_settings.DIGIT_SIZE, 10))
            self.game.SCREEN.blit(self.digits['10'], (10 + (i + 1) * self.texture_settings.DIGIT_SIZE, 10))

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < self.control_settings.MOUSE_BORDER_LEFT or mx > self.control_settings.MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([self.control_settings.H_WIDTH, self.control_settings.H_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-self.control_settings.MOUSE_MAX_RELATIVE, min(self.control_settings.MOUSE_MAX_RELATIVE, self.rel))
        self.angle += self.rel * self.control_settings.MOUSE_SENSITIVITY * self.game.stats.delta_time

    def update(self):
        self.movement()
        self.mouse_control()
        self.fire()
        self.regenerate()
        self.in_view()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)