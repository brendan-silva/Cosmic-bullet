from abc import ABCMeta, abstractmethod
from pygame import Vector2
from pygame import Rect
from pygame.locals import *
import pygame
from math import *
WIDTH = 1536
HEIGHT = 864
WHITE = (255, 255, 255)

loaded_scene = None


class Transform2D:
    """
    Represents a position in any coordinate system.

    Attributes
    ----------
    pos: Vector2
        The x and y component of the position
    rotation: float
        The rotational component of the position
    """
    pos: Vector2
    rotation: float

    def __init__(self, x: float, y: float, theta: float):
        self.pos = Vector2(x, y)
        self.rotation = theta


class GameObject(metaclass=ABCMeta):
    """
    Represents any object in a game.

    This class is a meta class meant to be inherited. This class represents a
    generic game object. All methods on the class are abstract meaning they
    have to be overrode.

    Attributes
    ----------
    transform : Transform2D
        The position of the game object in world coordinates
    sprite: Sprite
        The pygame sprite for the game object
    """
    transform: Transform2D
    sprite: pygame.sprite.Sprite

    def __init__(self):
        """
        Construct a new instance of the game object class.

        A constructor for the game object class. This constructor should be used
        by all subclasses or it's functionally duplicated in the subclasses
        constructor.
        """
        self.transform = Transform2D()

    @abstractmethod
    def update(self, dt: float):
        """
        Call once a frame to allow game object to take actions.

        This abstract method must be overrode by all subclasses. This is method
        should be used to respond to user events, e.g. key presses or mouse
        clicks.

        Parameters
        ----------
        self : self
            The game object this method is being called upon.
        dt : float
            The delta time since the last time this method was called.
        """
        pass

class Player(GameObject):
    def __init__(self):
        self.transform = Transform2D(0, 0, 0)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("Sprites\Player.png")
        self.sprite.rect = self.sprite.image.get_rect(center=(0,0))
        self.diagonal_modifier= sqrt(2)/2
        self.shotcooldown=0
        self.bulletimg = pygame.image.load("Sprites\Player Bullet 1.png")
        self.cent=pygame.Vector2(self.sprite.rect.width-self.bulletimg.get_rect().width-4,(self.sprite.rect.height/3)-self.bulletimg.get_rect().height)

    def update(self, dt):
        VELOCITY = 400
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LSHIFT]:
            VELOCITY = 200
        if  self.shotcooldown >=0:
            self.shotcooldown-=dt
        if pressed_keys[K_z]and self.shotcooldown <=0:
            for i in range(-5,6):
                spawn(Player_bullet(self.transform.pos-self.cent,600,5*i,self.bulletimg))
            self.shotcooldown+=0.2
        if pressed_keys[K_UP]and pressed_keys[K_DOWN]:
            if  not (pressed_keys[K_LEFT] and pressed_keys[K_RIGHT]):
                if pressed_keys[K_LEFT]:
                    self.transform.pos.x += VELOCITY * dt
                elif pressed_keys[K_RIGHT]:
                    self.transform.pos.x -= VELOCITY * dt
        elif pressed_keys[K_UP]:
            if  not (pressed_keys[K_LEFT] and pressed_keys[K_RIGHT]):
                if pressed_keys[K_LEFT]:
                    self.transform.pos.x += VELOCITY * dt *self.diagonal_modifier
                    self.transform.pos.y += VELOCITY * dt *self.diagonal_modifier
                elif pressed_keys[K_RIGHT]:
                    self.transform.pos.x -= VELOCITY * dt *self.diagonal_modifier
                    self.transform.pos.y += VELOCITY * dt *self.diagonal_modifier
                else:
                    self.transform.pos.y += VELOCITY * dt 
            else:
                self.transform.pos.y += VELOCITY * dt 
        elif pressed_keys[K_DOWN]:
            if  not (pressed_keys[K_LEFT] and pressed_keys[K_RIGHT]):
                if pressed_keys[K_LEFT]:
                    self.transform.pos.x += VELOCITY * dt *self.diagonal_modifier
                    self.transform.pos.y -= VELOCITY * dt *self.diagonal_modifier
                elif pressed_keys[K_RIGHT]:
                    self.transform.pos.x -= VELOCITY * dt *self.diagonal_modifier
                    self.transform.pos.y -= VELOCITY * dt *self.diagonal_modifier
                else:
                    self.transform.pos.y -= VELOCITY * dt 
            else:
                self.transform.pos.y -= VELOCITY * dt
        else:
            if  not (pressed_keys[K_LEFT] and pressed_keys[K_RIGHT]):
                if pressed_keys[K_LEFT]:
                    self.transform.pos.x += VELOCITY * dt
                elif pressed_keys[K_RIGHT]:
                    self.transform.pos.x -= VELOCITY * dt

class Player_bullet(GameObject):
    def __init__(self,pos:Vector2,speed:float,ang:float,image:pygame.image):
        self.transform = Transform2D(pos.x,pos.y,ang)
        self.v = pygame.Vector2(0, speed)
        self.v = self.v.rotate(ang)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.sprite.rect = self.sprite.image.get_rect()
    
    def update(self, dt):
        self.transform.pos+=self.v*dt

class Bullet(GameObject):
    def __init__(self, transformation: Transform2D,image: pygame.image,v:list[float,float],a:list[float,float]):
        self.transform = transformation
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.v = pygame.Vector2(0, v[0])
        self.v = self.v.rotate(v[1])
        self.a = pygame.Vector2(0, a[0])
        self.a = self.a.rotate(a[1])
        self.sprite.rect = self.sprite.image.get_rect()

    def update(self, dt):
        self.transform.pos += self.v *dt
        self.v += self.a *dt

class Scene:
    objects: list[GameObject]

    def __init__(self, *objects):
        self.objects = list(objects)

    def spawn(self, game_object):
        self.objects.append(game_object)


def world_pos_to_screen_pos(pos: Vector2) -> Vector2:
    """Convert a vector in world coordinates to pixel coordinates"""
    new_pos = Vector2(-pos.x, -pos.y)
    new_pos.x += WIDTH / 2
    new_pos.y += HEIGHT / 2
    return new_pos


def render(game_object: GameObject, screen: pygame.Surface):
    """Render a game object to any surface"""
    if game_object.sprite is not None:
        world_pos = game_object.transform
        screen_pos = world_pos_to_screen_pos(world_pos.pos)

        sprite = game_object.sprite
        width = sprite.rect.width
        height = sprite.rect.height


        rect = Rect(screen_pos.x + width / 2, screen_pos.y + height / 2, width, height)
        screen.blit(pygame.transform.rotate(game_object.sprite.image,-game_object.transform.rotation),rect)


def spawn(game_object: GameObject):
    """Spawn a game object in the active scene"""
    loaded_scene.spawn(game_object)


def main(loading: Scene):
    global loaded_scene
    loaded_scene = loading
    delta_time: float = 0
    fps = 60
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game_loop = True

    while game_loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_loop = False
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
