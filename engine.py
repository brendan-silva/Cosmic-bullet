from abc import ABCMeta, abstractmethod
from pygame import Vector2
from pygame import Rect
from pygame.locals import *
import pygame

WIDTH = 1536
HEIGHT = 864
WHITE = (255, 255, 255)

loaded_scene = None


class Transform2D:
    pos: Vector2
    rotation: float

    def __init__(self, x: float, y: float, theta: float):
        self.pos = Vector2(x, y)
        self.rotation = theta


class GameObject(metaclass=ABCMeta):
    transform: Transform2D
    sprite: pygame.sprite.Sprite

    def __init__(self):
        self.transform = Transform2D()

    @abstractmethod
    def update(self, dt: float):
        pass


class Scene:
    objects: list[GameObject]

    def __init__(self, *objects):
        self.objects = list(objects)

    def spawn(self, game_object):
        self.objects.append(game_object)


def world_pos_to_screen_pos(pos: Vector2) -> Vector2:
    new_pos = Vector2(-pos.x, -pos.y)
    new_pos.x += WIDTH / 2
    new_pos.y += HEIGHT / 2
    return new_pos


def render(game_object: GameObject, screen: pygame.Surface):
    if game_object.sprite is not None:
        world_pos = game_object.transform
        screen_pos = world_pos_to_screen_pos(world_pos.pos)

        sprite = game_object.sprite
        width = sprite.rect.width
        height = sprite.rect.height

        rect = Rect(screen_pos.x + width / 2, screen_pos.y + height / 2, width, height)
        pygame.draw.rect(screen, WHITE, rect)


def spawn(game_object: GameObject):
    loaded_scene.spawn(game_object)


def main(loading: Scene):
    global loaded_scene
    loaded_scene = loading
    delta_time: float = 0
    fps = 60
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                break
        for game_object in loaded_scene.objects:
            game_object.update(delta_time)

        for game_object in loaded_scene.objects:
            render(game_object, screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))

        delta_time = clock.tick(fps) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
