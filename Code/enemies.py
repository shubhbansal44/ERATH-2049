from objects import *
from os.path import join
from random import randint, random
from settings import MAP_SETTINGS


class Enemy(Animated_Objects):
    def __init__(self, game, path=join('sources', 'enemies', 'soldier', '0.png'), pos=(1.5, 1.5), scale=0.7, shift=0.4, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.settings()
        self.attack_frames = self.get_frames(join(self.path, 'attack'))
        self.death_frames = self.get_frames(join(self.path, 'death'))
        self.idle_frames = self.get_frames(join(self.path, 'idle'))
        self.pain_frames = self.get_frames(join(self.path, 'pain'))
        self.walk_frames = self.get_frames(join(self.path, 'walk'))
        self.attack_dist = randint(2,4)
        self.speed = .04
        self.size = 30
        self.health = 150
        self.damage = 10
        self.accuracy = .1
        self.alive = True
        self.pain = False
        self.sight = False
        self.appetite = False
        self.death_progress = 0
        self.deletion_delay = 2000
        self.deleted = False
        self.time_prev = pg.time.get_ticks()
        self.view = False
        self.m_pressed = False

    def settings(self):
        self.render_settings = RENDER_SETTINGS()
        self.map_settings = MAP_SETTINGS()

    def update(self):
        self.in_view()
        self.draw_sight()
        self.get_objects()
        self.enemy_logic()
        if not self.alive:
            if not self.deleted:
                self.get_murdered()
            else:
                self.dlt()
                # pass
        else:
            self.check_animation()

    def in_view(self):
        key = pg.key.get_pressed()
        if key[pg.K_m] and not self.m_pressed:
            self.view = not self.view
            self.m_pressed = True
        if not key[pg.K_m]:
            self.m_pressed = False

    def get_murdered(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.deletion_delay:
            self.time_prev = time_now
            self.deleted = True

    def get_shot(self):
        if self.sight and self.game.player.fired:
            if self.render_settings.H_WIDTH - self.object_h_width < self.screen_x < self.render_settings.H_WIDTH + self.object_h_width:
                self.game.sound.pain.play()
                self.game.player.fired = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health <= 0:
            self.alive = False

    def dlt(self):
        self.alive = False
        if self in self.game.objects_handler.enemies:
            self.game.objects_handler.enemies.remove(self)

    def animate_death(self):
        if not self.alive:
            if self.game.global_flag and self.death_progress < len(self.death_frames) - 1:
                self.death_frames.rotate(-1)
                self.image = self.death_frames[0]
                self.death_progress += 1

    def attack(self):
        if self.animation_flag:
            self.game.sound.attack.play()
        if random() < self.accuracy:
            self.game.player.get_hurt(self.damage)


    def animate_pain(self):
        self.animate(self.pain_frames)
        if self.animation_flag:
            self.pain = False
    
    def movement(self):
        next_pos = self.game.path_finder.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos
        if next_pos not in self.game.objects_handler.enemy_pos:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.collision_detection(dx, dy)

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def collision_detection(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def enemy_logic(self):
        if self.alive:
            self.sight = self.in_sight()
            self.get_shot()
            if self.pain:
                self.animate_pain()
            elif self.sight:
                self.appetite = True
                if self.dist < self.attack_dist:
                    self.animate(self.attack_frames)
                    self.attack()
                else: 
                    self.animate(self.walk_frames)
                    self.movement()
            elif self.appetite:
                self.animate(self.walk_frames)
                self.movement()
            else:
                self.animate(self.idle_frames)
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return (int(self.x), int(self.y))
    
    def in_sight(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        # Player position and angle
        player_x, player_y = self.game.player.pos
        map_x, map_y = self.game.player.map_pos
        ray_angle = self.theta

        # Casting ray
        sin_a = math.sin(ray_angle) + .0001
        cos_a = math.cos(ray_angle) + .0001

        # Horizontal depth
        y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - 1e-6, -1)
        depth_hor = (y_hor - player_y) / sin_a
        x_hor = player_x + depth_hor * cos_a
        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        # Horizontal wall collision detection
        for depth in range(self.render_settings.MAX_DEPTH):
            tile_hor = (int(x_hor), int(y_hor))
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # Vertical depth
        x_vert, dx = (map_x + 1, 1) if cos_a > 0 else (map_x - 1e-6, -1)
        depth_vert = (x_vert - player_x) / cos_a
        y_vert = player_y + depth_vert * sin_a
        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        # Vertical wall collision detection
        for depth in range(self.render_settings.MAX_DEPTH):
            tile_vert = (int(x_vert), int(y_vert))
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_h, player_dist_v)
        wall_dist = max(wall_dist_h, wall_dist_v)
        
        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_sight(self):
        if ((self.alive or not self.deleted) and self.view) and not self.game.wasted and not self.game.x_mode:
            pg.draw.circle(
                self.game.SCREEN,
                'red',
                ((self.render_settings.WIDTH - self.map_settings.TILE_X * self.map_settings.TILE_DIMENSION_X) + self.x * self.map_settings.TILE_DIMENSION_X, self.y * self.map_settings.TILE_DIMENSION_Y),
                4
            )
            if self.sight:
                pg.draw.line(
                    self.game.SCREEN,
                    'yellow',
                    ((self.render_settings.WIDTH - self.map_settings.TILE_X * self.map_settings.TILE_DIMENSION_X) + self.game.player.x * self.map_settings.TILE_DIMENSION_X, self.game.player.y * self.map_settings.TILE_DIMENSION_Y),
                    ((self.render_settings.WIDTH - self.map_settings.TILE_X * self.map_settings.TILE_DIMENSION_X) + self.x * self.map_settings.TILE_DIMENSION_X, self.y * self.map_settings.TILE_DIMENSION_Y),
                    1
                )


class Soldier(Enemy):
    def __init__(self, game, path=join('sources', 'enemies', 'soldier', '0.png'), pos=(1.5, 1.5), scale=0.6, shift=0.4, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)


class Octobrain(Enemy):
    def __init__(self, game, path=join('sources', 'enemies', 'octobrain', '0.png'), pos=(9.5, 18.5), scale=0.7, shift=0.1, animation_time=220):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1
        self.speed = .05
        self.health = 100
        self.damage = 7
        self.accuracy = .25
        self.size = 15


class Chaos_serpent(Enemy):
    def __init__(self, game, path=join('sources', 'enemies', 'chaos_serpent', '0.png'), pos=(7.5, 31.5), scale=0.7, shift=0.4, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 2
        self.speed = .03
        self.health = 150
        self.damage = 10
        self.accuracy = .2


class Cyber_demon(Enemy):
    def __init__(self, game, path=join('sources', 'enemies', 'cyber_demon', '0.png'), pos=(7.5, 31.5), scale=1.1, shift=0.3, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 2
        self.speed = .03
        self.health = 250
        self.damage = 15
        self.accuracy = .2


class Cerberus(Enemy):
    def __init__(self, game, path=join('sources', 'enemies', 'cerberus', '0.png'), pos=(7.5, 31.5), scale=0.6, shift=0.4, animation_time=220):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1
        self.speed = .04
        self.health = 170
        self.damage = 12
        self.accuracy = .25