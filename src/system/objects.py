from pygame import Surface, Vector2

from math import floor, ceil

from system.sprite import Sprite


class Bird(Sprite):
    def __init__(self):
        super().__init__("textures/sprites.png")

        self.velocity = Vector2()
        self.gravity = 9.81
        self.move_speed = 2

        self.animation_frames = [self.image.subsurface(3, 489, 16, 16), self.image.subsurface(31, 489, 16, 16), self.image.subsurface(59, 489, 16, 16), self.image.subsurface(31, 489, 16, 16)]
        self.animation_interval = 7
        self.animation_step = 0

        self.frame_index = 0

    def update(self, screen: Surface):
        self.translation.x += self.move_speed

        self.frame_index += 1

        super().update(screen)

    def render(self, screen: Surface):
        if self.frame_index % self.animation_interval == 0:
            self.animation_step += 1
        super().render(screen, self.animation_frames[self.animation_step % len(self.animation_frames)])


class Background(Sprite):
    def __init__(self, screen_size: Vector2):
        super().__init__("textures/sprites.png")
        self.screen_size = screen_size
        self.screen_size.y *= 1.2

        self.image = self.image.subsurface(0, 0, 143, 255)

        self.aspect_ratio = self.image.get_width() / self.image.get_height()
        self.size = Vector2(self.screen_size.y * self.aspect_ratio, self.screen_size.y)

        self.num_tiles = ceil(self.screen_size.x / self.size.x)
        self.tile_step = floor(self.size.x)

    def update(self, screen: Surface):
        super().update(screen)

    def render(self, screen: Surface):
        for i in range(self.num_tiles):
            self.translation.x = self.tile_step * i
            super().render(screen)