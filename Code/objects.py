import pygame as pg
import os
from collections import deque
from settings import *


class Static_Objects:
    def __init__(self, game, path=os.path.join('Sources', 'objects', 'stand', 'LampStand.png'), pos=(1.1, 1.1), scale=0.7, shift=0.50):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_h_width = self.image.get_width() // 2
        self.image_ratio = self.image_width / self.image.get_height()
        self.dx, self.dy, self.screen_x, self.theta, self.object_h_width, self.dist, self.norm_dist = 0, 0, 0, 0, 0, 1, 1
        self.scale = scale
        self.height_shift = shift
        self.alive = True

    def dlt(self):
        self.alive = False
        if self in self.game.objects_handler.objects:
            self.game.objects_handler.objects.remove(self)

    def render_objects(self):
        projection = SCREEN_DEPTH / self.norm_dist * self.scale
        projection_width, projection_height = projection * self.image_ratio, projection
        image = pg.transform.scale(self.image, (projection_width, projection_height))
        self.object_h_width = projection_width // 2
        height_shift = projection_height * self.height_shift
        pos = self.screen_x - self.object_h_width, H_HEIGHT - projection_height // 2 + height_shift
        self.game.raycast.objects.append((self.norm_dist, image, pos))

    def get_objects(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau
        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (H_CASTED_RAYS + delta_rays) * SCALE
        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.image_h_width < self.screen_x < (WIDTH + self.image_h_width) and self.norm_dist > .5:
            self.render_objects()

    def update(self):
        if self.alive:
            self.get_objects()


class Animated_Objects(Static_Objects):
    def __init__(self, game, path=os.path.join('Sources', 'objects', 'fire1', 'tile000.png'), pos=(1.05, 1.05), scale=0.3, shift=0.1, animation_time=40):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit('\\', 1)[0]
        self.frames = self.get_frames(self.path)
        self.time_prev = pg.time.get_ticks()
        self.animation_flag = False
    
    def update(self):
        super().update()
        self.check_animation()
        self.animate(self.frames)

    def animate(self, frames):
        if self.animation_flag:
            frames.rotate(-1)
            self.image = frames[0]

    def check_animation(self):
        self.animation_flag = False
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev >= self.animation_time:
            self.time_prev = time_now
            self.animation_flag = True

    def get_frames(self, path):
        frames = deque()
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                frame = pg.image.load(os.path.join(path, file)).convert_alpha()
                frames.append(frame)
        return frames