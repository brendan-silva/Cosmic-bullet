from abc import ABCMeta, abstractmethod
from pygame import Vector2, Rect
from pygame.sprite import Sprite
from pygame.locals import *
import pygame
from typing_extensions import Self
import math
import copy
Playermove = Vector2(0, 0)
Playerlaseroff = True
WIDTH = 1536
HEIGHT = 864
WHITE = (255, 255, 255)
DARKBLUE = (35,33,87)
LIGHTBLUE = (79,90,154)

scene_lib = {}
scene_change = None
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
    deload: bool = False

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

    def hit(self, other: Self):
        pass

    # def delete(self):
    #     """
    #     Delete a game object from the current scene.
    #
    #     This method does not happen right away.
    #     """
    #     self.deload = True


class Player(GameObject):
    def __init__(self):
        self.transform = Transform2D(0, 0, 0)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("Cosmic-bullet/Sprites/Player.png")
        self.sprite.rect = self.sprite.image.get_rect(center=(0, 0))
        self.diagonal_modifier = math.sqrt(2) / 2
        self.shotcooldown = 0
        self.bulletimg = pygame.image.load("Cosmic-bullet/Sprites/Player Bullet 1.png")
        self.Laserimg = pygame.image.load(
            "Cosmic-bullet/Sprites/Large Player Laser.png"
        )
        self.v = Vector2(0, 400)
        self.vy = 0
        self.vx = 0
        self.shottype = 0
        self.xhold = False
        self.hp = 3
        self.hitcooldown = 0
        self.dead = False

    def update(self, dt):
        global Playerlaseroff
        global Playermove
        if self.hitcooldown >= 0:
            self.hitcooldown -= dt
            if self.hitcooldown <= 0:
                self.sprite.image = pygame.image.load(
                    "Cosmic-bullet/Sprites/Player.png"
                )
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
                        1,
                    )
                )
            self.shotcooldown += 0.2
        if pressed_keys[K_z] and self.shotcooldown <= 0 and self.shottype == 1:
            if Playerlaseroff:
                for i in range(0, 30):
                    spawn(
                        Player_laser(
                            self.transform.pos
                            + Vector2(0, 38 + (32 * i))
                            - Playermove * dt,
                            00,
                            0,
                            self.Laserimg,
                            10,
                        )
                    )
            Playerlaseroff = False
        else:
            Playerlaseroff = True
        if pressed_keys[K_x]:
            if not self.xhold:
                self.shottype += 1
                if self.shottype > 2:
                    self.shottype = 0
            self.xhold = True
        else:
            self.xhold = False

    def hit(self, other: Self):
        if isinstance(other, Bullet):
            # GameObject.delete(other)
            if self.hitcooldown <= 0:
                self.hp -= 1
                self.hitcooldown = 1
                self.sprite.image = pygame.image.load(
                    "Cosmic-bullet/Sprites/Player hit.png"
                )


class Player_bullet(GameObject):
    def __init__(
        self,
        pos: Vector2,
        speed: float,
        ang: float,
        image: pygame.image,
        dmg: float = 0,
    ):
        self.transform = Transform2D(pos.x, pos.y, ang)
        self.v = pygame.Vector2(0, speed)
        self.v = self.v.rotate(ang)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.sprite.rect = self.sprite.image.get_rect()
        self.dmg = dmg
        if self.sprite.rect.width > self.sprite.rect.height:
            self.Bullethit = self.sprite.rect.width * 1.1
        else:
            self.Bullethit = self.sprite.rect.height * 1.1
        self.dead = False

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
        if self.sprite.rect.width < self.sprite.rect.height:
            self.Bullethit = self.sprite.rect.width * 0.8
        else:
            self.Bullethit = self.sprite.rect.height * 0.8
        self.dead = False

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
class wavedata(GameObject):
    def __init__(
        self,
        transformation: Transform2D,
        image: pygame.image,
        v: list[float, float] = [0, 0],
        a: list[float, float] = [0, 0],
        enemysPerBurst: int = 1,
        shottime: float = 1,
        timeoffset: float = 0,
        Burstchange: list[float, float, float, float] = [0, 0, 0, 0],
        incrementchange: list[float, float, float, float] = [0, 0, 0, 0],
        incrementcap: int = 1,
        shotdata:list[shotdata]=None,
        hp:float=1
    ):
        self.sprite=None
        self.transform = transformation
        self.image = image
        self.v = v
        self.a = a
        self.repeat =enemysPerBurst
        self.shotrate = shottime
        self.repeatchange = Burstchange
        self.incrementchange = incrementchange
        self.shotcooldown = timeoffset
        self.i = 0
        self.incrementcap = incrementcap
        self.dead=False
        self.shotdata=shotdata
        self.hp=hp
        self.aaaa=[]


    def update(self, dt,):
        if self.shotcooldown >= 0:
            self.shotcooldown -= dt
        if self.shotcooldown <= 0:
            for x in range(0, self.repeat):
                self.aaaa=[]
                for y in self.shotdata:
                    self.aaaa.append(copy.copy(y))
                spawn(
                    enemy(
                        self.transform+Transform2D(0,0,0),
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
                        self.hp,
                        self.aaaa
                    )
                )
            self.shotcooldown += self.shotrate
            self.i += 1
            if self.i == self.incrementcap:
                self.dead=True

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
        if self.sprite.rect.width > self.sprite.rect.height:
            self.Bullethit = self.sprite.rect.width * 1.0
        else:
            self.Bullethit = self.sprite.rect.height * 1.0
        self.hitcooldown = 0
        self.dead = False

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
                Bull.dead=True
            if self.hp<=0:
                self.dead=True

class textobject(GameObject):
    def __init__(self,x,y,text,colour,size=72):
        self.font = pygame.font.Font(None, size)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.font.Font.render(self.font,text,False,colour)
        self.sprite.rect = self.sprite.image.get_rect()
        self.center = self.sprite.rect.center
        self.transform = Transform2D(x,y,0)
        self.dead = False
        self.text = text
        self.colour = colour
    def update(self,dt):
        if dt >= 0:
            self.changetext("newtext")
    def changetext(self,text,recenter=False):
        self.sprite.image = pygame.font.Font.render(self.font,text,False,self.colour)
        self.sprite.rect = self.sprite.image.get_rect()
        if recenter:
            self.sprite.rect.center = self.center

class button(GameObject):
    def __init__(self,x,y,scene,text=""):
        self.sprite = pygame.sprite.Sprite()
        self.transform = Transform2D(x,y,0)
        self.enabled = pygame.image.load("Cosmic-bullet\Sprites\Button(1).png")
        self.disabled = pygame.image.load("Cosmic-bullet\Sprites\Button(2).png")
        self.type = textobject(0,0,text,DARKBLUE)
        self.text = text
        self.update_sprite(self.enabled,DARKBLUE)
        self.sprite.rect = self.sprite.image.get_rect()
        self.dead = False
        self.scene = scene
    def update_sprite(self,image,colour):
        self.type = textobject(0,0,self.text,colour)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.sprite.image.blit(self.type.sprite.image,self.type.sprite.rect)
        self.sprite.rect = self.sprite.image.get_rect()
    def update(self,dt):
        global mousedown
        if self.sprite.rect.collidepoint((pygame.mouse.get_pos()[0]-WIDTH/2+self.sprite.rect.width/2,pygame.mouse.get_pos()[1]-HEIGHT/2+self.sprite.rect.height/2)):
            self.update_sprite(self.disabled,LIGHTBLUE)
            if mousedown == True:
                pass
        else:
            self.update_sprite(self.enabled,DARKBLUE)

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


def rect_from_hitbox_and_pos(pos: Vector2, hitbox: Rect) -> Rect:
    width = hitbox.width
    height = hitbox.height
    return Rect(pos.x - width / 2, pos.y - height / 2, width, height)


def render(game_object: GameObject, screen: pygame.Surface, debug: bool = False):
    """Render a game object to any surface"""
    if not game_object.sprite is None:
        world_pos = game_object.transform
        screen_pos = world_pos_to_screen_pos(world_pos.pos)

        sprite = game_object.sprite

        rect = rect_from_hitbox_and_pos(screen_pos, sprite.rect)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), rect, width=2)

        screen.blit(
            pygame.transform.rotate(
                game_object.sprite.image, -game_object.transform.rotation
            ),
            rect,
        )
class Scene:
    objects: list[GameObject]

    def __init__(self, *objects):
        self.objects = list(objects)

    def spawn(self, game_object):
        self.objects.append(game_object)

def spawn(game_object: GameObject):
    """Spawn a game object in the active scene"""
    loaded_scene.spawn(game_object)


def collison_decection(game_objects: GameObject):
    for index, game_object in enumerate(game_objects):
        # Need to figure out a way to check if the bullet has collided with anything without terrible performance
        if game_object.sprite.rect is not None and not isinstance(game_object, Bullet):
            # get all objects except current
            objects = game_objects[:index] + game_objects[index + 1:]

            # gets all the rects calculated from there position and hitbox
            rects = list(
                map(
                    lambda obj: rect_from_hitbox_and_pos(
                        obj.transform.pos, obj.sprite.rect
                    ),
                    objects,
                )
            )

            # Check collisions
            collided = rect_from_hitbox_and_pos(
                game_object.transform.pos, game_object.sprite.rect
            ).collidelistall(rects)

            # Get original index before removing current element
            collided = map(
                lambda index_collided: (
                    index_collided + 1 if index_collided >= index else index_collided
                ),
                collided,
            )

            # get objects form the collisions
            collided_objects = [game_objects[i] for i in collided]

            # Call collsion callback
            for other_object in collided_objects:
                game_object.hit(other_object)


def main(loading: str, lib: dict):
    global loaded_scene
    global scene_lib
    global scene_change
    scene_lib = lib
    loaded_scene = scene_lib[loading]
    delta_time: float = 0
    fps = 60
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game_loop = True
    global mousedown
    mousedown = False

    while game_loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_loop = False
            if event.type == MOUSEBUTTONDOWN:
                mousedown = True
                
        for game_object in loaded_scene.objects:
            # if game_object.deload:
            # #     del game_object
            # else:
            game_object.update(delta_time)

        game_objects_with_sprites = list(
            filter(
                lambda game_obj: game_object.sprite is not None, loaded_scene.objects
            )
        )

        for game_object in game_objects_with_sprites:
            render(game_object, screen, True)

        collison_decection(game_objects_with_sprites)

        if isinstance(game_object, enemy):
            for game_object2 in loaded_scene.objects:
                if isinstance(game_object2, Player_bullet):
                    game_object.checkifhit(game_object2)

        i = 0
        while i < len(loaded_scene.objects):
            if loaded_scene.objects[i].dead or (
                Playerlaseroff and isinstance(loaded_scene.objects[i], Player_laser)
            ):
                del loaded_scene.objects[i]
            else:
                i += 1
        # test
        end = 0
        for game_object in loaded_scene.objects:
            if isinstance(game_object, enemy):
                end += 1
        if end == 0:
            scene_change = "stage_2"
        # test
        if not (scene_change == None):
            loaded_scene = scene_lib[scene_change]
            scene_change = None
        pygame.display.flip()
        screen.fill((0, 0, 0))
        delta_time = clock.tick(fps) / 1000
        mousedown = False

    pygame.quit()


if __name__ == "__main__":
    main()
