from os.path import join
from objects import *
from enemies import *


class Object_Handler:
    def __init__(self, game):
        self.game = game
        self.objects = []
        self.enemies = []
        self.animated_enemies_path = join('Sources', 'enemies')
        self.static_objects_path = join('Sources', 'objects')
        self.animated_objects_path = join('Sources', 'objects')
        add_objects = self.add_objects
        add_enemies = self.add_enemies
        self.enemy_pos = {}

        # objects
        add_objects(Static_Objects(game))
        add_objects(Animated_Objects(game))

        # enemies
        add_enemies(Enemy(game))
        add_enemies(Enemy(game, pos=(13.5, 15.5)))

    def update(self):
        self.enemy_pos = {enemy.map_pos for enemy in self.enemies if enemy.alive}
        [object.update() for object in self.objects]
        [enemy.update() for enemy in self.enemies]

    def add_objects(self, object):
        self.objects.append(object)

    def add_enemies(self, enemy):
        self.enemies.append(enemy)