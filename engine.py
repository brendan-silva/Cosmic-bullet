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
        self.Bullethit=2

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
        if pressed_keys[K_UP] and not self.transform.pos[1] > 422:
            self.vy += 1
        if pressed_keys[K_DOWN] and not self.transform.pos[1] < -422:
            self.vy -= 1
        if pressed_keys[K_LEFT] and not self.transform.pos[0] > 314:
            self.vx -= 1
        if pressed_keys[K_RIGHT] and not self.transform.pos[0] < -314:
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

    def checkifhit(self,Bull):
        if self.hitcooldown <= 0:
            if math.pow(self.transform.pos.x-Bull.transform.pos.x,2)+math.pow(self.transform.pos.y-Bull.transform.pos.y,2) <= math.pow(self.Bullethit+Bull.Bullethit,2):
                self.hp -= 1
                self.hitcooldown = 1
                self.sprite.image = pygame.image.load(
                    "Cosmic-bullet/Sprites/Player hit.png"
                )
                if self.hp<=0:
                    self.dead=True


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
            self.Bullethit = self.sprite.rect.width * 0.5
        else:
            self.Bullethit = self.sprite.rect.height * 0.5
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
            self.Bullethit = self.sprite.rect.width * 0.5
        else:
            self.Bullethit = self.sprite.rect.height * 0.5
        self.dead = False

    def update(self, dt):
        self.transform.pos += self.v * dt
        self.v += self.a * dt
        if abs(self.transform.pos.x)>500:
            self.dead = True
        elif abs(self.transform.pos.y)>500:
            self.dead = True


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
            self.Bullethit = self.sprite.rect.width * 0.5
        else:
            self.Bullethit = self.sprite.rect.height * 0.5
        self.hitcooldown = 0
        self.dead = False

    def update(self, dt):
        if self.hitcooldown >= 0:
            self.hitcooldown -= dt
        self.transform.pos += self.v * dt
        self.v += self.a * dt
        for x in self.shotdata:
            x.update(dt, self.transform)
    
    def checkifhit(self,Object):
        if math.pow(self.transform.pos.x-Object.transform.pos.x,2)+math.pow(self.transform.pos.y-Object.transform.pos.y,2) <= math.pow(self.Bullethit+Object.Bullethit,2):
            if isinstance(Object,Player_laser):
                if self.hitcooldown == 0.25:
                    self.hp-= Object.dmg*0.2
                elif self.hitcooldown <=0 :
                    self.hp-= Object.dmg
                    self.hitcooldown = 0.25
            else:
                self.hp -= Object.dmg
                Object.dead=True
            if self.hp<=0:
                self.dead=True

class background(GameObject):
    def __init__(self,x,y,path,scroll=0):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(path)
        self.sprite.rect = self.sprite.image.get_rect()
        self.transform = Transform2D(x-self.sprite.rect.width/2,y-self.sprite.rect.height/2,0)
        self.dead = False
        self.scroll = scroll
    def update(self,dt):
        if self.scroll > 0:
            if self.transform.pos[1] <= 0:
                self.transform.pos += (0,432)
            self.transform.pos -= (0,self.scroll)

class sidebar(GameObject):
    def __init__(self,x,y,path,scroll=0):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(path)
        self.sprite.rect = self.sprite.image.get_rect()
        self.transform = Transform2D(x-self.sprite.rect.width/2,y-self.sprite.rect.height/2,0)
        self.dead = False
    def update(self,dt):
        pass     
                
class UI(GameObject):
    pass
    
class image(UI):
    def __init__(self,x,y,path,rotV=0,rot=0):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(path)
        self.sprite.rect = self.sprite.image.get_rect()
        self.transform = Transform2D(x,y,0)
        self.dead = False
        self.rot = rot
        self.rotV = rotV
    def update(self,dt):
        self.transform.rotation += self.rotV

class textobject(UI):
    def __init__(self,x,y,text,colour,size=72):
        pygame.font.init()
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
        pass
    def changetext(self,text,recenter=False):
        self.sprite.image = pygame.font.Font.render(self.font,text,False,self.colour)
        self.sprite.rect = self.sprite.image.get_rect()
        if recenter:
            self.sprite.rect.center = self.center

class button(UI):
    def __init__(self,x,y,scene,text="",quitbutton=False):
        self.sprite = pygame.sprite.Sprite()
        self.transform = Transform2D(x,y,0)
        self.enabled = pygame.image.load("Cosmic-bullet\Sprites\Button(1B).png")
        self.disabled = pygame.image.load("Cosmic-bullet\Sprites\Button(2B).png")
        self.type = textobject(0,0,text,DARKBLUE)
        self.text = text
        self.update_sprite(self.enabled,DARKBLUE)
        self.sprite.rect = self.sprite.image.get_rect()
        self.dead = False
        self.scene = scene
        self.quitbutton = quitbutton
    def update_sprite(self,image,colour):
        self.type = textobject(0,0,self.text,colour)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.sprite.rect = self.sprite.image.get_rect()
        coords = (self.sprite.rect.center[0]-self.type.sprite.rect.width/2,self.sprite.rect.center[1]-self.type.sprite.rect.height/2)
        self.sprite.image.blit(self.type.sprite.image,coords)
    def update(self,dt):
        global mousedown
        if self.sprite.rect.collidepoint((pygame.mouse.get_pos()[0]-WIDTH/2+self.sprite.rect.width/2,pygame.mouse.get_pos()[1]-HEIGHT/2+self.sprite.rect.height/2)):
            self.update_sprite(self.disabled,LIGHTBLUE)
            if mousedown == True:
                if self.quitbutton:
                    pygame.quit()
                global scene_change
                scene_change = self.scene
        else:
            self.update_sprite(self.enabled,DARKBLUE)
            
class statusbar(UI):
    def __init__(self,x,y,maxval=200,baseval=0,folder="defaultbar"):
        self.transform = Transform2D(x,y,0)
        self.sprite = pygame.sprite.Sprite()
        self.root = folder
        self.image = pygame.surface.Surface((273,96))
        self.icon = pygame.transform.scale_by(pygame.image.load("Cosmic-bullet\Sprites\\"+self.root+"\Icon.png"),3)
        self.bg = pygame.transform.scale_by(pygame.image.load("Cosmic-bullet\Sprites\\"+self.root+"\BG.png"),3)
        self.bar = pygame.transform.scale_by(pygame.image.load("Cosmic-bullet\Sprites\\"+self.root+"\Bar.png"),3)
        self.image.blits([(self.bg,(84,18)),(self.bar,(87,21)),(self.icon,(0,0))]) 
        self.sprite.image = self.image
        self.sprite.rect = self.sprite.image.get_rect()
        self.val = baseval
        self.max = maxval
        self.dead = False
    def update(self,dt):
        if self.val < self.max:
            self.val += 1
        self.bar = pygame.transform.scale(self.bar,(math.ceil(180*(self.val/self.max)),54))
        self.image.fill((164,111,43))
        self.image.blits([(self.bg,(84,18)),(self.bar,(87,21)),(self.icon,(0,0))])

    #objects: list[GameObject]

    #def __init__(self, *objects):
    #    self.objects = list(objects)

    #def spawn(self, game_object):
    #    self.objects.append(game_object)


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


def render(game_object: GameObject, screen: pygame.Surface,):
    """Render a game object to any surface"""
    if not game_object.sprite is None:
        world_pos = game_object.transform
        screen_pos = world_pos_to_screen_pos(world_pos.pos)
        sprite = game_object.sprite
        rect = rect_from_hitbox_and_pos(screen_pos, sprite.rect)
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
        self.player = None
        self.i=0
        while self.i < len(self.objects):
            if isinstance(self.objects[self.i], Player):
                self.player = self.objects[self.i]
            self.i += 1
        del self.i


    def spawn(self, game_object):
        self.objects.append(game_object)
        

def spawn(game_object: GameObject):
    """Spawn a game object in the active scene"""
    loaded_scene.spawn(game_object)



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
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
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
        object_matrix = [[],[],[],[],[],[],[]]
        for game_object in game_objects_with_sprites:
            if isinstance(game_object,background):
                object_matrix[0].append(game_object)
            elif isinstance(game_object,enemy):
                object_matrix[1].append(game_object)
            elif isinstance(game_object,Player):
                object_matrix[2].append(game_object)
            elif isinstance(game_object,Bullet):
                object_matrix[3].append(game_object)
            elif isinstance(game_object,Player_bullet):
                object_matrix[4].append(game_object)
            elif isinstance(game_object,sidebar):
                object_matrix[5].append(game_object)
            elif isinstance(game_object,UI):
                object_matrix[6].append(game_object)
        for array in object_matrix:
            for item in array:
                render(item, screen)
            
        i = 0
        for b in loaded_scene.objects:
            if isinstance(b, Bullet):
                loaded_scene.player.checkifhit(b)
        for e in loaded_scene.objects:
            if isinstance(e,enemy):
                for pb in loaded_scene.objects:
                    if isinstance(pb, Player_bullet):
                        e.checkifhit(pb)
        while i < len(loaded_scene.objects):
            if loaded_scene.objects[i].dead or (
                Playerlaseroff and isinstance(loaded_scene.objects[i], Player_laser)
            ):
                del loaded_scene.objects[i]
            else:
                i += 1
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
