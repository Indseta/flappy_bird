from pygame import Surface, Vector2
from pygame.image import load as load_image
from pygame.transform import scale, rotate
from pygame.rect import Rect

from json import load as load_json

from system.frame_info import FrameInfo


with open("resources/details.json", "r") as f:
    details = load_json(f)

resources = details["system"]["resources"]


class Sprite:
    def __init__(self, frame_info: FrameInfo, image_path: str):
        self.translation = Vector2(0, 0)
        self.rotation = 0

        self.image = load_image(f"{resources}/{image_path}").convert_alpha()

        self.size = Vector2(self.image.get_width(), self.image.get_height())

        self.rect = Rect(self.translation.x, self.translation.y, self.size.x, self.size.y)

    def update(self, frame_info: FrameInfo):
        self.rect = Rect(self.translation.x, self.translation.y, self.size.x, self.size.y)

    def render(self, frame_info: FrameInfo, render_target: Surface = None):
        if render_target == None:
            rotated_image = rotate(self.image, self.rotation)
            frame_info.screen.blit(scale(rotated_image, self.size), self.translation)
        else:
            rotated_image = rotate(render_target, self.rotation)
            frame_info.screen.blit(scale(rotated_image, self.size), self.translation)
