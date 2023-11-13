import pygame

from json import load as load_json
from math import floor
from uuid import UUID, uuid4

from system.frame_info import FrameInfo
from system.objects import Background
from system.objects import Bird
from system.objects import Pipe


# -- Main class --
class Application:
    def __init__(self, screen_width: int, screen_height: int):
        pygame.init()

        self.screen = pygame.display.set_mode((screen_width, screen_height))

        with open("resources/details.json", "r") as f:
            details = load_json(f)

        self.resources = details["system"]["resources"]

        pygame.display.set_caption(f"{details["title"]} v{details["version"]}")
        pygame.display.set_icon(pygame.image.load(f"{self.resources}/{details["system"]["icon"]}"))

        self.frame_info = FrameInfo(self.screen)
        self.frame_info.max_fps = 80

        self.objects = {}

    # -- Main --
    def main(self):
        self.screen_size = self.frame_info.get_screen_size()

        self.background = Background(self.frame_info)

        self.bird = Bird(self.frame_info)

        self.num_pipes = 2

        for i in range(self.num_pipes):
            pipe = self.register(Pipe(self.frame_info))
            self.objects[pipe].placement.x = self.screen_size.x + i * (self.screen_size.x + self.objects[pipe].size.x) / self.num_pipes

        self.fps_text_object = pygame.font.Font(f"{self.resources}/fonts/ProggyClean.ttf", 18)
        self.points_text_object = pygame.font.Font(None, 42)

        while self.frame_info.run:
            if self.frame_info.game_state == "pre_game":
                self.pre_game_update()
            elif self.frame_info.game_state == "in_game":
                self.update()

            self.events()

        pygame.quit()

    # -- Update --
    def update(self):
        self.frame_info.update()
        self.frame_info.player = self.bird

        self.background.update(self.frame_info)
        self.background.render(self.frame_info)

        self.bird.update(self.frame_info)
        self.bird.render(self.frame_info)

        for object_ref in self.objects:
            object = self.objects[object_ref]

            object.update(self.frame_info)
            object.render(self.frame_info)

        # HUD
        self.screen.blit(self.fps_text_object.render(str(floor(self.frame_info.avg_fps)), True, pygame.Color(100, 100, 100)), (4, 4))
        self.screen.blit(self.points_text_object.render(str(self.frame_info.points), True, pygame.Color(255, 255, 255)), (250, 200))

        # Death
        if self.frame_info.dead:
            self.on_death()
            self.frame_info.dead = False

        pygame.display.flip()

    # -- Pre game/Menu update --
    def pre_game_update(self):
        self.frame_info.update()
        self.frame_info.player = self.bird

        self.background.update(self.frame_info)
        self.background.render(self.frame_info)

        self.bird.pre_game_update(self.frame_info)
        self.bird.render(self.frame_info)

        # HUD
        self.screen.blit(self.fps_text_object.render(str(floor(self.frame_info.avg_fps)), True, pygame.Color(100, 100, 100)), (4, 4))
        self.screen.blit(self.points_text_object.render(str(self.frame_info.points), True, pygame.Color(255, 255, 255)), (250, 200))

        pygame.display.flip()

    # -- Poll events --
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.frame_info.run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.bird.b_jump = True
        else:
            self.bird.b_jump = False
            self.bird.b_has_jumped = False

    # -- Register object --
    def register(self, object) -> UUID:
        id = uuid4()
        self.objects[id] = object
        return id

    # -- Death event --
    def on_death(self):
        self.frame_info.game_state = "pre_game"
        self.bird.translation = pygame.Vector2(self.screen_size.x / 3 - self.bird.size.x / 2, self.screen_size.y / 2 - self.bird.size.y / 2)
        self.bird.velocity = pygame.Vector2(0, 0)
        self.objects.clear()
        for i in range(self.num_pipes):
            pipe = self.register(Pipe(self.frame_info))
            self.objects[pipe].placement.x = self.screen_size.x + i * (self.screen_size.x + self.objects[pipe].size.x) / self.num_pipes