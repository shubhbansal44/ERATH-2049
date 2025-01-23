# IMPORTS
import json
import pygame as pg
import sys
from os.path import join
from parser import Parser
from settings import PLAYER_SETTINGS, SCREEN_SETTINGS, RENDER_SETTINGS, VIEWPORT_SETTINGS, CONTROL_SETTINGS


class Static_Button():
    def __init__(self, game, text='click', width=15.625, height=6.48, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        self.game = game
        self.settings()
        self.screen = game.SCREEN
        self.width_precent = width
        self.height_precent = height
        self.pos_x_percent = pos[0]
        self.pos_y_percent = pos[1]
        self.screen_width = self.screen_settings.WIDTH
        self.screen_height = self.screen_settings.HEIGHT
        self.width = (self.width_precent * self.screen_width) / 100
        self.height = (self.height_precent * self.screen_height) / 100
        self.pos_x = (self.pos_x_percent * self.screen_width) / 100
        self.pos_y = (self.pos_y_percent * self.screen_height) / 100
        self.btn_top_rect = pg.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        self.btn_color_1 = btn_color_1
        self.btn_color_2 = btn_color_2
        self.btn_color_3 = btn_color_3
        self.btn_color = btn_color_1
        self.text = text
        self.elevation = dynamic_elevation
        self.dynamic_elevation = dynamic_elevation
        self.static_elevation = static_elevation
        self.y = (self.pos_y_percent * self.screen_height) / 100
        self.font_color = font_color
        self.border_radius = border_radius
        self.btn_bottom_rect = pg.Rect((self.pos_x, self.pos_y), (self.width, self.elevation))
        self.font_size_percent = font_size
        self.font_design = font
        self.font_size = int((self.font_size_percent * (self.screen_width + self.screen_height)) / 100)
        self.font = pg.font.SysFont(self.font_design, self.font_size)
        self.pressed = False
        self.active = False

    def draw(self):
        self.text_surf = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surf.get_rect(center=self.btn_top_rect.center)
        self.btn_top_rect.y = self.y - self.dynamic_elevation
        self.text_rect.center = self.btn_top_rect.center
        self.btn_bottom_rect.midtop = self.btn_top_rect.midtop
        self.btn_bottom_rect.height = self.btn_top_rect.height + self.dynamic_elevation + self.static_elevation
        pg.draw.rect(self.screen, self.btn_color_2, self.btn_bottom_rect, border_radius=self.border_radius)
        pg.draw.rect(self.screen, self.btn_color, self.btn_top_rect, border_radius=self.border_radius)
        self.screen.blit(self.text_surf, self.text_rect)
        self.click()

    def settings(self):
        self.screen_settings = SCREEN_SETTINGS()
        self.player_settings = PLAYER_SETTINGS()
        self.control_settings = CONTROL_SETTINGS()
        self.viewport_settings = VIEWPORT_SETTINGS()
        self.render_settings = RENDER_SETTINGS()
        self.parser = Parser()

    def update(self):
        self.screen_width = self.screen_settings.WIDTH
        self.screen_height = self.screen_settings.HEIGHT
        self.width = (self.width_precent * self.screen_width) / 100
        self.height = (self.height_precent * self.screen_height) / 100
        self.pos_x = (self.pos_x_percent * self.screen_width) / 100
        self.pos_y = (self.pos_y_percent * self.screen_height) / 100
        self.btn_top_rect = pg.Rect((self.pos_x, self.pos_y), (self.width, self.height))
        self.y = (self.pos_y_percent * self.screen_height) / 100
        self.btn_bottom_rect = pg.Rect((self.pos_x, self.pos_y), (self.width, self.elevation))
        self.font_size = int((self.font_size_percent * (self.screen_width + self.screen_height)) / 100)
        self.font = pg.font.SysFont(self.font_design, self.font_size)
    
    def click(self):
        if self.btn_top_rect.collidepoint(pg.mouse.get_pos()):
            self.btn_color = self.btn_color_3
            if pg.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.active = True
                    self.pressed = False
        else:
            self.btn_color = self.btn_color_1
            self.dynamic_elevation = self.elevation


class New_Game(Static_Button):
    def __init__(self, game, text='New Game', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = self.game.menu.main_menu = False
            if self.game.start:
                self.game.demolish()
            self.game.start = True
            self.game.game = True
            self.game.new_game()
            self.active = False


class Settings(Static_Button):
    def __init__(self, game, text='Settings', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.options = self.game.menu.main_menu = True
            self.game.menu.settings_saved = False
            self.game.menu.settings_reset = False
            self.game.menu.settings_changed = False
            self.active = False


class Load_Game(Static_Button):
    def __init__(self, game, text='Load Game', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.load_game = self.game.menu.main_menu = True
            self.active = False


class Save_Game(Static_Button):
    def __init__(self, game, text='Save Game', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.save_game = self.game.menu.main_menu = True
            self.active = False


class Credits(Static_Button):
    def __init__(self, game, text='Credits', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.credits = self.game.menu.main_menu = True
            self.active = False


class Quit(Static_Button):
    def __init__(self, game, text='Quit', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            pg.quit()
            sys.exit(0)
            self.active = False


class Back(Static_Button):
    def __init__(self, game, text='Back', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12, prev='menu'):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.prev = prev

    def function(self):
        if self.active:
            self.game.menu.navigate_back(self.prev)
            self.active = False


class Resolution(Static_Button):
    def __init__(self, game, text='Resolution', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.res = [(self.parser.default_data['width'], self.parser.default_data['height']), (1280, 800), (1024, 768)]
        self.flashed = False


    def function(self):
        if self.active:
            self.id = self.game.menu.saved_settings['id']
            self.id = (self.id + 1) % len(self.res)
            for id in range(len(self.res)):
                if id == self.id:
                    self.game.menu.saved_settings[f'res{self.id + 1}'] = '#486a47'
                else:
                    self.game.menu.saved_settings[f'res{id + 1}'] = '#475F77'
            self.game.menu.res1.btn_color_1 = self.game.menu.res1.btn_color_3 = self.game.menu.saved_settings['res1']
            self.game.menu.res2.btn_color_1 = self.game.menu.res2.btn_color_3 = self.game.menu.saved_settings['res2']
            self.game.menu.res3.btn_color_1 = self.game.menu.res3.btn_color_3 = self.game.menu.saved_settings['res3']
            self.game.menu.saved_settings['width'], self.game.menu.saved_settings['height'] = self.res[self.id]
            self.game.menu.saved_settings['id'] = self.id
            self.flashed = False
            self.flash_res_screen()
            self.active = False

    def flash_res_screen(self):
        if not self.flashed:
            res_screen = pg.Surface(self.res[self.id], pg.SRCALPHA)
            res_screen.fill((0, 0, 0, 128))
            self.screen.blit(res_screen, (((self.screen_width - self.res[self.id][0]) / 2), (self.screen_height - self.res[self.id][1]) / 2))
            pg.display.update()
            pg.time.delay(300)
            self.flashed = True


class Save_Settings(Static_Button):
    def __init__(self, game, text='Save Settings', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            with open(join('Code', 'saved_settings.txt'), 'w') as settings:
                json.dump(self.game.menu.saved_settings, settings)
            self.parser.update("SAVE")                                  
            self.screen_settings.update()
            self.player_settings.update()
            self.control_settings.update()
            self.viewport_settings.update()
            self.render_settings.update()
            self.game.update_settings()
            for buttons in self.game.menu.all_buttons:
                buttons.update()
            self.game.menu.settings_saved = True
            self.game.menu.settings_changed = True
            self.active = False


class Reset_Settings(Static_Button):
    def __init__(self, game, text='Reset Settings', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            with open(join('Code', 'saved_settings.txt'), 'w') as settings:
                pass
            self.revert_btn_data()                             
            self.parser.update("RESET")
            self.screen_settings.update()
            self.player_settings.update()
            self.control_settings.update()
            self.viewport_settings.update()
            self.render_settings.update()
            self.game.update_settings()
            for buttons in self.game.menu.all_buttons:
                buttons.update()
            self.game.menu.settings_reset = True
            self.game.menu.settings_changed = True
            self.active = False

    def revert_btn_data(self):
        self.game.menu.res1.btn_color_1 = self.game.menu.res1.btn_color_3 = self.parser.default_data['res1']
        self.game.menu.res2.btn_color_1 = self.game.menu.res2.btn_color_3 = self.parser.default_data['res2']
        self.game.menu.res3.btn_color_1 = self.game.menu.res3.btn_color_3 = self.parser.default_data['res3']
        self.game.menu.player_speed.text = f'{format(((self.parser.default_data['player_speed'] / 0.006) * 100), ".2f")}%'
        self.game.menu.player_rot_speed.text = f'{format(((self.parser.default_data['player_rot_speed'] / 0.006) * 100), ".2f")}%'
        self.game.menu.mouse_sensitivity.text = f'{format(((self.parser.default_data['mouse_sensitivity'] / 0.0006) * 100), ".2f")}%'


class Up(Static_Button):
    def __init__(self, game, text='>', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12, id=0):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.attr = (['player_speed', 0.0005], ['player_rot_speed', 0.0005], ['mouse_sensitivity', 0.00005])
        self.limits = ([0.002, 0.006], [0.002, 0.006], [0.0002, 0.0006])
        self.id = id

    def function(self):
        if self.active:
            val = self.game.menu.saved_settings[self.attr[self.id][0]] + self.attr[self.id][1]
            val = format(max(min(val, self.limits[self.id][1]), self.limits[self.id][0]), ".7f")
            self.game.menu.saved_settings[self.attr[self.id][0]] = float(val)
            self.game.menu.player_speed.text = f'{format(((self.game.menu.saved_settings['player_speed'] / 0.006) * 100), ".2f")}%'
            self.game.menu.player_rot_speed.text = f'{format(((self.game.menu.saved_settings['player_rot_speed'] / 0.006) * 100), ".2f")}%'
            self.game.menu.mouse_sensitivity.text = f'{format(((self.game.menu.saved_settings['mouse_sensitivity'] / 0.0006) * 100), ".2f")}%'
            pg.display.update()
            self.active = False


class Down(Static_Button):
    def __init__(self, game, text='<', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=1, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12, id=0):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.attr = (['player_speed', -0.0005], ['player_rot_speed', -0.0005], ['mouse_sensitivity', -0.00005])
        self.limits = ([0.002, 0.006], [0.002, 0.006], [0.0002, 0.0006])
        self.id = id

    def function(self):
        if self.active:
            val = self.game.menu.saved_settings[self.attr[self.id][0]] + self.attr[self.id][1]
            val = format(max(min(val, self.limits[self.id][1]), self.limits[self.id][0]), ".7f")
            self.game.menu.saved_settings[self.attr[self.id][0]] = float(val)
            self.game.menu.player_speed.text = f'{format((((self.game.menu.saved_settings['player_speed']) / 0.006) * 100), ".2f")}%'
            self.game.menu.player_rot_speed.text = f'{format(((self.game.menu.saved_settings['player_rot_speed'] / 0.006) * 100), ".2f")}%'
            self.game.menu.mouse_sensitivity.text = f'{format(((self.game.menu.saved_settings['mouse_sensitivity'] / 0.0006) * 100), ".2f")}%'
            pg.display.update()
            self.active = False
