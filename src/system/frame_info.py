from pygame import Surface, Vector2
from pygame.time import Clock
from pygame.rect import Rect


class FrameInfo:
    def __init__(self, screen: Surface):
        self.screen = screen

        self.run = True
        self.game_state = "pre_game"

        self.player = None
        self.points = 0
        self.dead = False

        self.frame_index = 0

        self.clock = Clock()
        self.dt = 0
        self.fps = []
        self.max_fps = 60
        self.avg_fps = 0

    def get_screen_size(self) -> Vector2:
        return Vector2(self.screen.get_size())

    def update(self):
        if self.max_fps <= 0:
            self.dt = self.clock.tick() / 1000
        else:
            self.dt = self.clock.tick(self.max_fps) / 1000

        current_fps = self.clock.get_fps()

        self.fps.append(current_fps)
        if len(self.fps) > 60:
            self.fps.pop(0)

        self.avg_fps = sum(self.fps) / len(self.fps)

        self.frame_index += 1