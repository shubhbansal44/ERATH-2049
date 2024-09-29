from objects import *
from os.path import join


class Weapons(Animated_Objects):
    def __init__(self, game, path=join('Sources', 'weapons', 'shotgun', '0.png'), scale=0.3, animation_time=120):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.frames = deque([
            pg.transform.smoothscale(frame, (self.image.get_width() * scale, self.image.get_height() * scale))
            for frame in self.frames])
        self.weapon_pos = (H_WIDTH - self.frames[0].get_width() // 2, HEIGHT - self.frames[0].get_height())
        self.reloading = False
        self.frames_count = len(self.frames)
        self.reloading_progress = 0
        self.damage = 50

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

    def update(self):
        self.check_animation()
        self.animate_shot()