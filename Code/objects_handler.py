from os.path import join
from objects import *
from enemies import *
from settings import PLAYER_SETTINGS
from random import choices, randrange
import json


class Object_Handler():
    def __init__(self, game):
        self.settings()
        self.game = game
        self.objects = []
        self.enemies = []
        self.animated_enemies_path = join('Sources', 'enemies')
        self.static_objects_path = join('Sources', 'objects')
        self.animated_objects_path = join('Sources', 'objects')
        self.enemy_pos = {}
        self.enemies_count = 30
        self.enemy_types = [Soldier, Chaos_Serpent, Octobrain, Cerberus, Cyber_Demon]
        self.freq = [40, 20, 20, 10, 10]
        self.restricted_area = {(i, j) for i in range(int(self.player_settings.PLAYER_X) - 5, int(self.player_settings.PLAYER_X) + 5, 1) for j in range(int(self.player_settings.PLAYER_Y) - 2, int(self.player_settings.PLAYER_Y) + 2, 1)}
        self.enemy_data = {}

        # objects
        self.add_objects(Static_Objects(game))
        self.add_objects(Animated_Objects(game))

        # enemies
        self.spawn_enemy()

    def settings(self):
        self.player_settings = PLAYER_SETTINGS()

    def spawn_enemy(self):
        for i in range(self.enemies_count):
            enemies = choices(self.enemy_types, weights=self.freq, k=self.enemies_count)
            Enemy = enemies[i]
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            self.add_enemies(Enemy(self.game, pos=(x + 0.5, y + 0.5)))

        self.enemy_id = {enemy: enemy.id for enemy in self.enemies}

    def update(self):
        self.enemy_pos = {enemy.map_pos for enemy in self.enemies if enemy.alive}
        self.enemy_data = {x: {'enemy': self.enemy_id[enemy], 'pos': enemy.pos, 'health': enemy.health} for x, enemy in enumerate(self.enemies) if enemy.alive}
        # with open(join('Code', 'saved_game.txt'), 'w') as file:
        #     json.dump(self.enemy_data, file)
        [object.update() for object in self.objects]
        [enemy.update() for enemy in self.enemies]

    def add_objects(self, object):
        self.objects.append(object)

    def add_enemies(self, enemy):
        self.enemies.append(enemy)