from abc import ABCMeta, abstractmethod
from pygame import Vector2
from pygame import Rect
from pygame.locals import *
import pygame
import math 
Playermove = Vector2(0, 0)
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

    def __add__(self, other):
        return Transform2D(
            self.pos.x + other.pos.x,
            self.pos.y + other.pos.y,
            self.rotation + other.rotation,
        )


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
        self.sprite.image = pygame.image.load("Cosmic-bullet\Sprites\Player.png")
        self.sprite.rect = self.sprite.image.get_rect(center=(0, 0))
        self.diagonal_modifier = math.sqrt(2) / 2
        self.shotcooldown = 0
        self.bulletimg = pygame.image.load("Cosmic-bullet\Sprites\Player Bullet 1.png")
        self.Laserimg = pygame.image.load("Cosmic-bullet\Sprites\Large Player Laser.png")
        self.v = Vector2(0, 400)
        self.vy = 0
        self.vx = 0
        self.shottype = 0
        self.xhold = False
        self.hp = 3
        self.hitcooldown=0

    def update(self, dt):
        if self.hitcooldown >= 0:
            self.hitcooldown -= dt
            if self.hitcooldown <= 0:
                self.sprite.image = pygame.image.load("Cosmic-bullet\Sprites\Player.png")
        global Playermove
        self.v = Vector2(0, 400)
        self.vy = 0
        self.vx = 0
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LSHIFT]:
            self.v = self.v / 2
        if pressed_keys[K_UP]:
            self.vy += 1
        if pressed_keys[K_DOWN]:
            self.vy -= 1
        if pressed_keys[K_LEFT]:
            self.vx -= 1
        if pressed_keys[K_RIGHT]:
            self.vx += 1
        if not self.vy == 0:
            self.v = self.v.rotate(90 - self.vy * 90 + self.vx * self.vy * 45)
        elif not self.vx == 0:
            self.v = self.v.rotate(self.vx * 90)
        else:
            self.v = Vector2(0, 0) 
        Playermove = self.v
        self.transform.pos += self.v * dt
        if self.shotcooldown >= 0:
            self.shotcooldown -= dt
        if pressed_keys[K_z] and self.shotcooldown <= 0 and self.shottype == 0:
            for i in range(-3, 4):
                spawn(
                    Player_bullet(
                        self.transform.pos + Vector2(4, 20),
                        600,
                        5 * i,
                        self.bulletimg,
                        1
                    )
                )
            self.shotcooldown += 0.2
        if pressed_keys[K_z] and self.shotcooldown <= 0 and self.shottype == 1:
            for i in range(0,30):
                spawn(
                    Player_laser(
                    self.transform.pos + Vector2(0, 38+(32*i))-Playermove * dt,
                    00,
                    0,
                    self.Laserimg,
                    2
                    )
                )
            self.shotcooldown += 0.1
        if pressed_keys[K_x]:
            if not self.xhold:
                self.shottype += 1
                if self.shottype > 2:
                    self.shottype = 0
            self.xhold = True
        else:
            self.xhold=False
    def checkifhit(self,Bull:GameObject):
        distance=math.sqrt(abs(self.transform.pos.x-Bull.transform.pos.x)+abs(self.transform.pos.y-Bull.transform.pos.y))
        if distance <= math.sqrt(4+Bull.Bullethit):
            self.hp -= 1
            self.sprite.image = pygame.image.load("Cosmic-bullet\Sprites\Player hit.png")
            self.hitcooldown = 1

class Player_bullet(GameObject):
    def __init__(self, pos: Vector2, speed: float, ang: float, image: pygame.image,dmg:float=0):
        self.transform = Transform2D(pos.x, pos.y, ang)
        self.v = pygame.Vector2(0, speed)
        self.v = self.v.rotate(ang)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.sprite.rect = self.sprite.image.get_rect()
        self.dmg=dmg
        if self.sprite.rect.width>self.sprite.rect.height:
            self.Bullethit=self.sprite.rect.width*1.1
        else:
            self.Bullethit=self.sprite.rect.height*1.1

    def update(self, dt):
        self.transform.pos += self.v * dt
class Player_laser(Player_bullet):
    def update(self, dt):
        global Playermove
        self.transform.pos += self.v * dt + Playermove * dt

class Bullet(GameObject):
    def __init__(
        self,
        transformation: Transform2D,
        image: pygame.image,
        v: list[float, float],
        a: list[float, float],
    ):
        self.transform = transformation
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.v = pygame.Vector2(0, v[0])
        self.v = self.v.rotate(v[1])
        self.a = pygame.Vector2(0, a[0])
        self.a = self.a.rotate(a[1])
        self.sprite.rect = self.sprite.image.get_rect()
        if self.sprite.rect.width<self.sprite.rect.height:
            self.Bullethit=self.sprite.rect.width*0.8
        else:
            self.Bullethit=self.sprite.rect.height*0.8

    def update(self, dt):
        self.transform.pos += self.v * dt
        self.v += self.a * dt


class shotdata:
    def __init__(
        self,
        transformation: Transform2D,
        image: pygame.image,
        v: list[float, float] = [0, 0],
        a: list[float, float] = [0, 0],
        BulletsPerBurst: int = 1,
        shottime: float = 1,
        timeoffset: float = 0,
        Burstchange: list[float, float, float, float] = [0, 0, 0, 0],
        incrementchange: list[float, float, float, float] = [0, 0, 0, 0],
        incrementcap: int = -1,
    ):
        self.transform = transformation
        self.image = image
        self.v = v
        self.a = a
        self.repeat = BulletsPerBurst
        self.shotrate = shottime
        self.repeatchange = Burstchange
        self.incrementchange = incrementchange
        self.shotcooldown = timeoffset
        self.i = 0
        self.incrementcap = incrementcap


    def update(self, dt, Transform2D: Transform2D):
        if self.shotcooldown >= 0:
            self.shotcooldown -= dt
        if self.shotcooldown <= 0:
            for x in range(0, self.repeat):
                spawn(
                    Bullet(
                        Transform2D + self.transform,
                        self.image,
                        [
                            self.v[0]
                            + x * self.repeatchange[0]
                            + self.i * self.incrementchange[0],
                            self.v[1]
                            + x * self.repeatchange[1]
                            + self.i * self.incrementchange[1],
                        ],
                        [
                            self.a[0]
                            + x * self.repeatchange[2]
                            + self.i * self.incrementchange[2],
                            self.a[1]
                            + x * self.repeatchange[3]
                            + self.i * self.incrementchange[3],
                        ],
                    )
                )
            self.shotcooldown += self.shotrate
            self.i += 1
            if self.i == self.incrementcap:
                self.i = 0


class enemy(GameObject):
    def __init__(
        self,
        transformation: Transform2D,
        image: pygame.image,
        v: list[float, float] = [0, 0],
        a: list[float, float] = [0, 0],
        hp: float = 1,
        shotdata: list[shotdata] = None,
    ):
        self.transform = transformation
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.v = pygame.Vector2(0, v[0])
        self.v = self.v.rotate(v[1])
        self.a = pygame.Vector2(0, a[0])
        self.a = self.a.rotate(a[1])
        self.sprite.rect = self.sprite.image.get_rect()
        self.shotdata = shotdata
        self.hp = hp
        if self.sprite.rect.width>self.sprite.rect.height:
            self.Bullethit=self.sprite.rect.width*1.0
        else:
            self.Bullethit=self.sprite.rect.height*1.0
        self.hitcooldown=0

    def update(self, dt):
        if self.hitcooldown >= 0:
            self.hitcooldown -= dt
        self.transform.pos += self.v * dt
        self.v += self.a * dt
        for x in self.shotdata:
            x.update(dt, self.transform)
    def checkifhit(self,Bull:GameObject):
        distance=math.sqrt(abs(self.transform.pos.x-Bull.transform.pos.x)+abs(self.transform.pos.y-Bull.transform.pos.y))
        if distance <= math.sqrt(self.Bullethit+Bull.Bullethit):
            if isinstance(Bull,Player_laser):
                if self.hitcooldown == 0.25:
                    self.hp-= Bull.dmg*0.2
                elif self.hitcooldown <=0 :
                    self.hp-= Bull.dmg
                    self.hitcooldown = 0.25
            else:
                self.hp -= Bull.dmg
            if self.hp<=0:
                self.sprite.image=pygame.image.load("Cosmic-bullet\Sprites\Player.png")



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

        rect = Rect(screen_pos.x - width / 2, screen_pos.y - height / 2, width, height)
        screen.blit(
            pygame.transform.rotate(
                game_object.sprite.image, -game_object.transform.rotation
            ),
            rect,
        )


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
        for game_object in loaded_scene.objects:
            if isinstance(game_object,Player):
                if game_object.hitcooldown<=0:
                    for game_object2 in loaded_scene.objects:
                        if isinstance(game_object2,Bullet):
                            if game_object.hitcooldown<=0:
                                game_object.checkifhit(game_object2)
                    if game_object.hp<=0:
                        game_loop = False
        for game_object in loaded_scene.objects:
            if isinstance(game_object,enemy):
                for game_object2 in loaded_scene.objects:
                    if isinstance(game_object2,Player_bullet):
                        game_object.checkifhit(game_object2)
        pygame.display.flip()
        screen.fill((0, 0, 0))
        delta_time = clock.tick(fps) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
