import pygame as pg
import math
from settings import *

class RayCaster:
    def __init__(self, game):
        self.game = game
        self.results = []
        self.objects = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects(self):
        self.objects = []
        for ray, values in enumerate(self.results):
            depth, projection_height, texture, offset = values
            if projection_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    (offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, projection_height))
                wall_pos = (ray * SCALE, H_HEIGHT - projection_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / projection_height
                wall_column = self.textures[texture].subsurface(
                    (offset * (TEXTURE_SIZE - SCALE), H_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height)
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects.append((depth, wall_column, wall_pos))

    def cast_rays(self):
        self.results = []

        # Player position and angle
        player_x, player_y = self.game.player.pos
        map_x, map_y = self.game.player.map_pos
        ray_angle = self.game.player.angle - H_FOV + .0001  # Initial ray angle

        # Casting rays
        for rays in range(CASTED_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # Horizontal depth
            y_hor, dy = (map_y + 1, 1) if sin_a > 0 else (map_y - 1e-6, -1)
            depth_hor = (y_hor - player_y) / sin_a
            x_hor = player_x + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            # Horizontal wall collision detection
            for depth in range(MAX_DEPTH):
                tile_hor = (int(x_hor), int(y_hor))
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
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
            for depth in range(MAX_DEPTH):
                tile_vert = (int(x_vert), int(y_vert))
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Determine the closer depth and texture
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            #  Casting rays for debugging (uncomment for visual debugging)
            # pg.draw.line(
            #     self.game.SCREEN,
            #     'white',
            #     (player_x * TILE_X, player_y * TILE_Y),
            #     (player_x * TILE_X + depth * cos_a * TILE_X, player_y * TILE_X + depth * sin_a * TILE_Y),
            #     2
            # )

            # Fisheye effect correction
            depth *= math.cos(self.game.player.angle - ray_angle)

            # Calculate wall height based on depth
            projection_height = SCREEN_DEPTH / (depth + .0001)

            # Shadow effect (uncomment to enable shading)
            # color = [255 / (1 + depth ** 5 * .00002)] * 3

            # 3D (2.5D) wall rendering (uncomment to visualize 3D walls directly)
            # pg.draw.rect(
            #     self.game.SCREEN,
            #     color,
            #     (rays * SCALE, H_HEIGHT - projection_height // 2, SCALE, projection_height)
            # )

            # Store the results for further object rendering
            self.results.append((depth, projection_height, texture, offset))

            # Move to the next ray
            ray_angle += DELTA_ANGLE
                
    def update(self):
        self.cast_rays()
        self.get_objects()
