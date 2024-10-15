import pygame as pg
import sys
from parser import *


class Static_Button():
    def __init__(self, game, text='click', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        self.game = game
        self.screen = game.SCREEN
        self.btn_top_rect = pg.Rect(pos, (width, height))
        self.btn_color_1 = btn_color_1
        self.btn_color_2 = btn_color_2
        self.btn_color_3 = btn_color_3
        self.btn_color = btn_color_1
        self.text = text
        self.elevation = dynamic_elevation
        self.dynamic_elevation = dynamic_elevation
        self.static_elevation = static_elevation
        self.y = pos[1]
        self.font_color = font_color
        self.border_radius = border_radius
        self.btn_bottom_rect = pg.Rect(pos, (width, dynamic_elevation))
        self.font = pg.font.SysFont(font, font_size)
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
    def __init__(self, game, text='New Game', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
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
    def __init__(self, game, text='Settings', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.options = self.game.menu.main_menu = True
            self.active = False


class Load_Game(Static_Button):
    def __init__(self, game, text='Load Game', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.load_game = self.game.menu.main_menu = True
            self.active = False


class Save_Game(Static_Button):
    def __init__(self, game, text='Save Game', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.save_game = self.game.menu.main_menu = True
            self.active = False


class Credits(Static_Button):
    def __init__(self, game, text='Credits', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.game.menu.menu = False
            self.game.menu.credits = self.game.menu.main_menu = True
            self.active = False


class Quit(Static_Button):
    def __init__(self, game, text='Quit', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            pg.quit()
            sys.exit(0)


class Back(Static_Button):
    def __init__(self, game, text='Back', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12, prev='menu'):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.prev = prev

    def function(self):
        if self.active:
            self.game.menu.navigate_back(self.prev)
            self.active = False


class Resolution(Static_Button):
    def __init__(self, game, text='Resolution', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.parser = Parser()
        self.res = [[(self.parser.parse_attr('width'), self.parser.parse_attr('height')), '#475F77'], [(1280, 800), '#475F77'], [(1024, 768), '#475F77']]
        self.id = 0
        self.flashed = False


    def function(self):
        if self.active:
            self.id = (self.id + 1) % len(self.res)
            for id, res in enumerate(self.res):
                if id == self.id:
                    res[1] = '#486a47'
                else:
                    res[1] = '#475F77'
            self.game.menu.res1.btn_color_1 = self.game.menu.res1.btn_color_3 = self.res[0][1]
            self.game.menu.res2.btn_color_1 = self.game.menu.res2.btn_color_3 = self.res[1][1]
            self.game.menu.res3.btn_color_1 = self.game.menu.res3.btn_color_3 = self.res[2][1]
            self.flashed = False
            self.flash_res_screen()
            self.active = False

    def flash_res_screen(self):
        if not self.flashed:
            res_screen = pg.Surface(self.res[self.id][0], pg.SRCALPHA)
            res_screen.fill((0, 0, 0, 128))
            self.screen.blit(res_screen, ((self.res[0][0][0] - self.res[self.id][0][0]) / 2, (self.res[0][0][1] - self.res[self.id][0][1]) / 2))
            pg.display.update()
            pg.time.delay(300)
            self.flashed = True


class Save_Settings(Static_Button):
    def __init__(self, game, text='Save Settings', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)

    def function(self):
        if self.active:
            self.active = False


class Up(Static_Button):
    def __init__(self, game, text='>', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12, attr='player_speed'):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.speed_increment = 0.0005
        self.sensitivity_increment = 0.00005
        self.attr = attr

    def function(self):
        if self.active:
            if self.attr == 'player_speed':
                self.game.menu.player_speed_value += self.speed_increment
                self.game.menu.player_speed_value = max(min(self.game.menu.player_speed_value, 0.006), 0.002)
                self.game.menu.player_speed.text = f'{((self.game.menu.player_speed_value / 0.006) * 100):.1f}%'
            elif self.attr == 'player_rot_speed':
                self.game.menu.player_rot_speed_value += self.speed_increment
                self.game.menu.player_rot_speed_value = max(min(self.game.menu.player_rot_speed_value, 0.006), 0.002)
                self.game.menu.player_rot_speed.text = f'{((self.game.menu.player_rot_speed_value / 0.006) * 100):.1f}%'
            elif self.attr == 'mouse_sensitivity':
                self.game.menu.mouse_sensitivity_value += self.sensitivity_increment
                self.game.menu.mouse_sensitivity_value = max(min(self.game.menu.mouse_sensitivity_value, 0.0006), 0.0002)
                self.game.menu.mouse_sensitivity.text = f'{((self.game.menu.mouse_sensitivity_value / 0.0006) * 100):.1f}%'
            pg.display.update()
            self.active = False


class Down(Static_Button):
    def __init__(self, game, text='<', width=200, height=40, pos=(0, 0), btn_color_1='#475F77', btn_color_2='#354B5E', btn_color_3='#D74B4B', font='Arial', font_size=30, font_color='#FFFFFF', dynamic_elevation=6, static_elevation=0, border_radius=12, attr='player_speed'):
        super().__init__(game, text, width, height, pos, btn_color_1, btn_color_2, btn_color_3, font, font_size, font_color, dynamic_elevation, static_elevation, border_radius)
        self.speed_increment = -0.0005
        self.sensitivity_increment = -0.00005
        self.attr = attr

    def function(self):
        if self.active:
            if self.attr == 'player_speed':
                self.game.menu.player_speed_value += self.speed_increment
                self.game.menu.player_speed_value = max(min(self.game.menu.player_speed_value, 0.006), 0.002)
                self.game.menu.player_speed.text = f'{((self.game.menu.player_speed_value / 0.006) * 100):.1f}%'
            elif self.attr == 'player_rot_speed':
                self.game.menu.player_rot_speed_value += self.speed_increment
                self.game.menu.player_rot_speed_value = max(min(self.game.menu.player_rot_speed_value, 0.006), 0.002)
                self.game.menu.player_rot_speed.text = f'{((self.game.menu.player_rot_speed_value / 0.006) * 100):.1f}%'
            elif self.attr == 'mouse_sensitivity':
                self.game.menu.mouse_sensitivity_value += self.sensitivity_increment
                self.game.menu.mouse_sensitivity_value = max(min(self.game.menu.mouse_sensitivity_value, 0.0006), 0.0002)
                self.game.menu.mouse_sensitivity.text = f'{((self.game.menu.mouse_sensitivity_value / 0.0006) * 100):.1f}%'
            pg.display.update()
            self.active = False