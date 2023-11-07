from pygame import Surface, Vector2
from pygame.image import load
from pygame.transform import scale


class Sprite:
    def __init__(self, image_path: str):
        self.translation = Vector2()
        self.rotation = 0

        self.image = load(f"src/resources/{image_path}")

        self.size = Vector2(self.image.get_width(), self.image.get_height())

    def update(self, screen: Surface):
        pass

    def render(self, screen: Surface, render_target: Surface = None):
        if render_target == None:
            screen.blit(scale(self.image, self.size), self.translation)
        else:
            screen.blit(scale(render_target, self.size), self.translation)


class AnimatableSprite:
    def __init__(self, image_path: str):
        self.translation = Vector2()
        self.rotation = 0

        self.image = load(f"src/resources/{image_path}")

        self.size = Vector2(self.image.get_width(), self.image.get_height())

    def update(self, screen: Surface):
        pass

    def render(self, screen: Surface, render_target: Surface = None):
        if render_target == None:
            screen.blit(scale(self.image, self.size), self.translation)
        else:
            screen.blit(scale(render_target, self.size), self.translation)