import pygame
from pygame.time import Clock

from asyncio import get_event_loop, gather, sleep
from uuid import uuid4

from system.objects import Bird
from system.objects import Background


# -- Main class --
class Application:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_size = pygame.Vector2(screen_width, screen_height)

        self.run = True
        self.objects = {}

        self.clock = Clock()
        self.dt = 0

    # -- Main code --
    def main(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.screen_size)

        title = "Flappy bird"
        version = "1.0"
        icon = "icon.png"

        pygame.display.set_caption(f"{title} v{version}")
        pygame.display.set_icon(pygame.image.load(f"src/resources/{icon}"))

        self.register(Background(self.screen_size))

        bird = self.register(Bird())
        self.objects[bird].translation = pygame.Vector2(0, 200)
        self.objects[bird].size = pygame.Vector2(60, 60)

        event_loop = get_event_loop()
        event_loop.run_until_complete(gather(self.events_task(), self.update_task()))

        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    # -- Update --
    def update(self):
        self.screen.fill((0, 0, 0))

        for object_ref in self.objects:
            object = self.objects[object_ref]
            object.update(self.screen)
            object.render(self.screen)

        pygame.display.flip()

    # -- Register object to application --
    def register(self, object):
        id = uuid4()
        self.objects[id] = object
        return id

    # -- Poll events task --
    async def events_task(self):
        while self.run:
            self.events()
            await sleep(1 / 1000) # Poll rate

    # -- Update task --
    async def update_task(self):
        while self.run:
            self.dt = self.clock.tick(60) / 1000.0
            self.update()
            await sleep(1 / 60) # Frame rate

