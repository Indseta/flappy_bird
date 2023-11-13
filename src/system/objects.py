from pygame import Vector2
from pygame.rect import Rect

from math import floor, ceil
from random import randint

from system.frame_info import FrameInfo
from system.sprite import Sprite


class Background(Sprite):
    def __init__(self, frame_info: FrameInfo):
        super().__init__(frame_info, "textures/sprites.png")

        self.screen_size = frame_info.get_screen_size()
        self.screen_size.y *= 1

        self.image = self.image.subsurface(0, 0, 144, 256).convert()

        self.aspect_ratio = self.image.get_width() / self.image.get_height()
        self.size = Vector2(self.screen_size.y * self.aspect_ratio, self.screen_size.y)

        self.num_tiles = ceil(self.screen_size.x / self.size.x)
        self.tile_step = floor(self.size.x)

    def update(self, frame_info: FrameInfo):
        pass

    def render(self, frame_info: FrameInfo):
        for i in range(self.num_tiles):
            self.translation.x = self.tile_step * i
            super().render(frame_info)


class Bird(Sprite):
    def __init__(self, frame_info: FrameInfo):
        super().__init__(frame_info, "textures/sprites.png")

        self.screen_size = frame_info.get_screen_size()

        self.size = Vector2(17, 12)
        self.size *= 3.5

        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 3000)

        self.animation_frames = [self.image.subsurface(3, 491, 17, 12).convert_alpha(), self.image.subsurface(31, 491, 17, 12).convert_alpha(), self.image.subsurface(59, 491, 17, 12).convert_alpha(), self.image.subsurface(31, 491, 17, 12).convert_alpha()]
        self.animation_interval = 8
        self.animation_step = 0

        self.translation = Vector2(self.screen_size.x / 3 - self.size.x / 2, self.screen_size.y / 2 - self.size.y / 2)

        self.b_jump = False
        self.b_has_jumped = False

    def update(self, frame_info: FrameInfo):
        if self.b_jump and not self.b_has_jumped:
            self.velocity.y = -700
            self.b_has_jumped = True

        self.velocity += self.acceleration * 0.5 * frame_info.dt
        self.translation += self.velocity * frame_info.dt
        self.velocity += self.acceleration * 0.5 * frame_info.dt

        if self.translation.y > self.screen_size.y - self.size.y:
            self.translation.y = self.screen_size.y - self.size.y

        super().update(frame_info)

    def pre_game_update(self, frame_info: FrameInfo):
        if self.b_jump and not self.b_has_jumped:
            frame_info.game_state = "in_game"
            frame_info.points = 0

            self.velocity.y = -700
            self.b_has_jumped = True

        self.translation += self.velocity * frame_info.dt

        if self.translation.y > self.screen_size.y - self.size.y:
            self.translation.y = self.screen_size.y - self.size.y

        super().update(frame_info)

    def render(self, frame_info: FrameInfo):
        if frame_info.frame_index % self.animation_interval == 0:
            self.animation_step += 1
        render_target = self.animation_frames[self.animation_step % len(self.animation_frames)]
        super().render(frame_info, render_target)


class Pipe(Sprite):
    def __init__(self, frame_info: FrameInfo):
        super().__init__(frame_info, "textures/sprites.png")

        self.screen_size = frame_info.get_screen_size()

        self.placement = Vector2(self.screen_size.x, randint(200, 520))
        self.translation = Vector2(self.placement.x, 0)

        self.velocity = Vector2(-180, 0)

        self.frame_index = 0

        self.size = Vector2(26, 160)
        self.size *= 3.5

        self.space = 180

        self.pipe_images = [self.image.subsurface(56, 323, 26, 160).convert_alpha(), self.image.subsurface(84, 323, 26, 160).convert_alpha()]

        self.b_assigned_point = False

    def update(self, frame_info: FrameInfo):
        self.placement += self.velocity * frame_info.dt

        if self.placement.x < -self.size.x:
            self.placement = Vector2(self.screen_size.x, randint(200, 520))

        self.rect = [Rect(self.placement.x, self.placement.y - self.size.y - self.space / 2, self.size.x, self.size.y), Rect(self.placement.x, self.placement.y + self.space / 2, self.size.x, self.size.y)]

        if Rect.colliderect(frame_info.player.rect, self.rect[0]) or Rect.colliderect(frame_info.player.rect, self.rect[1]):
            frame_info.dead = True

        if self.placement.x <= frame_info.player.translation.x:
            if not self.b_assigned_point:
                frame_info.points += 1
                self.b_assigned_point = True
        else:
            self.b_assigned_point = False

    def render(self, frame_info: FrameInfo):
        self.translation = Vector2(self.placement.x, self.placement.y - self.size.y - self.space / 2)
        super().render(frame_info, self.pipe_images[0])
        self.translation = Vector2(self.placement.x, self.placement.y + self.space / 2)
        super().render(frame_info, self.pipe_images[1])