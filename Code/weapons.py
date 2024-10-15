from objects import *
from os.path import join


class Weapons(Animated_Objects):
    def __init__(self, game, path=join('Sources', 'weapons', 'revolver', '1.png'), scale=4, animation_time=120):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.scale = scale
        self.frames = self.get_frames(self.path)
        self.weapon_pos = (self.render_settings.H_WIDTH - self.frames[0].get_width() // 2, self.render_settings.HEIGHT - self.frames[0].get_height())
        self.reloading = False
        self.frames_count = len(self.frames)
        self.reloading_progress = 0
        self.damage = 25
        self.damages = [25, 50, 75, 100]
        self.id = 0
        self.target = True
        self.weapons = ['revolver', 'shotgun_1_barrel', 'shotgun_2_barrel', 'thrower']
        self.weapon = self.weapons[self.id]
        self.pointer = self.game.renderer.get_texture(join('Sources', 'weapons', 'pointer.png'), (50, 50))
        self.target_pos = [
            (self.render_settings.H_WIDTH - (self.frames[0].get_width() // 2 - 202), self.render_settings.HEIGHT - (self.frames[0].get_height() + 120)),
            (self.render_settings.H_WIDTH - (self.frames[0].get_width() // 2 - 133), self.render_settings.HEIGHT - (self.frames[0].get_height() + 10)),
            (self.render_settings.H_WIDTH - (self.frames[0].get_width() // 2 - 134), self.render_settings.HEIGHT - (self.frames[0].get_height() + 15)),
            (self.render_settings.H_WIDTH - (self.frames[0].get_width() // 2 - 135), self.render_settings.HEIGHT - (self.frames[0].get_height() + 120))
        ]
        self.pointer_pos = self.target_pos[self.id]
        # self.restriction = len(self.weapons) - 2
        self.restriction = 0
        self.rshift_pressed = False
        self.b_pressed = False

    def weapon_change(self):
        key = pg.key.get_pressed()
        if key[pg.K_b] and not self.reloading and not self.b_pressed:
            self.id = (self.id + 1) % (len(self.weapons) - self.restriction)
            self.weapon = self.weapons[self.id]
            self.damage = self.damages[self.id]
            self.path = join('Sources', 'weapons', self.weapon, '1.png')
            self.scale = 4 if self.id !=1 else 0.3
            self.image = pg.image.load(self.path).convert_alpha()
            self.frames = self.get_frames(self.path.rsplit('\\', 1)[0])
            self.frames_count = len(self.frames)
            self.weapon_pos = (self.render_settings.H_WIDTH - self.frames[0].get_width() // 2, self.render_settings.HEIGHT - self.frames[0].get_height())
            self.pointer_pos = self.target_pos[self.id]
            self.b_pressed = True
        if not key[pg.K_b]:
            self.b_pressed = False

    def get_frames(self, path):
        frames = deque()
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                frame = pg.image.load(os.path.join(path, file)).convert_alpha()
                frame = pg.transform.smoothscale(frame, (self.image.get_width() * self.scale, self.image.get_height() * self.scale))
                frames.append(frame)
        return frames
    
    def toggle_target(self):
        key = pg.key.get_pressed()
        if key[pg.K_RSHIFT] and not self.rshift_pressed:
            self.target = not self.target
            self.rshift_pressed = True
        if not key[pg.K_RSHIFT]:
            self.rshift_pressed = False
    
    def animate_shot(self):
        if self.reloading:
            self.game.player.fired = False
            if self.animation_flag:
                self.frames.rotate(-1)
                self.image = self.frames[0]
                self.reloading_progress += 1
                if self.frames_count == self.reloading_progress:
                    self.reloading = False
                    self.reloading_progress = 0
                    self.game.sound.shotgun_shell_drop.play()
    
    def draw(self):
        self.game.SCREEN.blit(self.frames[0], self.weapon_pos)
        if not self.reloading and self.target:
            self.game.SCREEN.blit(self.pointer, self.pointer_pos)
    
    def update(self):
        self.check_animation()
        self.weapon_change()
        self.animate_shot()
        self.toggle_target()
