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
Playerlasercool = 0
Playerhp=3
PlayerEXcharge = 100

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
        self.transform = Transform2D(0, 0, 0)
        self.sprite = None
        self.dead = False

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
        self.sprite.image = pygame.image.load("Sprites/Player.png")
        self.sprite.rect = self.sprite.image.get_rect(center=(0, 0))
        self.diagonal_modifier = math.sqrt(2) / 2
        self.shotcooldown = 0
        self.bulletimg = pygame.image.load("Sprites/PlayerBullet.png")
        self.Laserimg = pygame.image.load("Sprites/PlayerLaser.png")
        self.Laserstartimg=pygame.image.load("Sprites/PlayerLaserStart.png")
        self.missileimg =pygame.image.load("Sprites/PlayerMissile.png")
        self.explosionimg =pygame.image.load("Sprites/PlayerExplosion.png")
        self.bulletimgEX = pygame.image.load("Sprites/PlayerBulletEX.png")
        self.LaserimgEX = pygame.image.load("Sprites/PlayerLaserEX.png")
        self.LaserstartimgEX=pygame.image.load("Sprites/PlayerLaserStartEX.png")
        self.missileimgEX =pygame.image.load("Sprites/PlayerMissileEX.png")
        self.explosionimgEX =pygame.image.load("Sprites/PlayerExplosionEX.png")
        self.v = Vector2(0, 400)
        self.vy = 0
        self.vx = 0
        self.shottype = 0
        self.shot_on= True
        self.zhold = False
        self.xhold = False
        self.chold = False
        self.hitcooldown = 0
        self.dead = False
        self.Bullethit=2
        self.EXchargeON=False

    def update(self, dt):
        global Playerlasercool
        global Playerlaseroff
        global Playermove
        global PlayerEXcharge
        if self.EXchargeON:
            PlayerEXcharge-=dt*5
        if PlayerEXcharge<0:
                self.EXchargeON =False
        if self.hitcooldown >= 0:
            self.hitcooldown -= dt
            if self.hitcooldown <= 0:
                self.sprite.image = pygame.image.load(
                    "Sprites/Player.png"
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
        
        #shot types
        if self.shot_on and self.shotcooldown <= 0 :
            if not self.EXchargeON:
                #dps roof of 60
                if self.shottype == 0:
                    for i in range(-3, 5):
                        spawn(
                            Player_bullet(
                                self.transform.pos + Vector2(4, 20),
                                600,
                                (5 * i) - 2.5,
                                self.bulletimg,
                                1.50,
                            )
                        )
                    self.shotcooldown += 0.2
                #dps floor of 50
                if self.shottype == 1:
                    if Playerlaseroff:
                        for i in range(0, 30):
                            if i==0:
                                spawn(
                                    Player_laser(
                                        self.transform.pos
                                        + Vector2(0, 38 + (32 * i))
                                        - Playermove * dt,
                                        00,
                                        0,
                                        self.Laserstartimg,
                                        10,
                                    )
                                )
                            else:
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
                #dps floor of 40
                if self.shottype == 2:
                    spawn(
                        Player_missile(
                            self.transform.pos + Vector2(0, 20),
                            300,
                            0,
                            self.missileimg,
                            self.explosionimg,
                            6,
                            2,
                        )
                    )
                    self.shotcooldown += 0.2
            #EXshot types
            else:
                #dps roof of 120
                if self.shottype == 0:
                    for i in range(-1, 3):
                        spawn(
                            Player_bulletEX(
                                self.transform.pos + Vector2(4, 20),
                                600,
                                (10 * i) - 5,
                                self.bulletimgEX,
                                self.bulletimg,
                                6,
                            )
                        )
                    self.shotcooldown += 0.2
                #dps floor of 100
                if self.shottype == 1:
                    if Playerlaseroff:
                        for i in range(0, 30):
                            if i==0:
                                spawn(
                                    Player_laser(
                                        self.transform.pos
                                        + Vector2(0, 38 + (32 * i))
                                        - Playermove * dt,
                                        00,
                                        0,
                                        self.LaserstartimgEX,
                                        20,
                                    )
                                )
                            else:
                                spawn(
                                    Player_laser(
                                        self.transform.pos
                                        + Vector2(0, 38 + (32 * i))
                                        - Playermove * dt,
                                        00,
                                        0,
                                        self.LaserimgEX,
                                        20,
                                    )
                                )
                    Playerlaseroff = False
                else:
                    Playerlaseroff = True
                #dps floor of 80
                if self.shottype == 2:
                    spawn(
                        Player_missile(
                            self.transform.pos + Vector2(0, 20),
                            300,
                            0,
                            self.missileimgEX,
                            self.explosionimgEX,
                            24,
                            8,
                        )
                    )
                    self.shotcooldown += 0.4
        if pressed_keys[K_z]:
            if not self.zhold:
                self.shottype += 1
                if self.shottype > 2:
                    self.shottype = 0
            self.zhold = True
        else:
            self.zhold = False
        if pressed_keys[K_x]:
            if not self.xhold and (PlayerEXcharge>25 or not self.EXchargeON):
                self.EXchargeON =not self.EXchargeON
                Playerlaseroff = True
            self.xhold = True
        else:
            self.xhold = False
        if PlayerEXcharge<0:
                self.EXchargeON =False
                Playerlaseroff = True
        if pressed_keys[K_c]:
            if not self.chold:
                self.shot_on =not self.shot_on
            self.chold = True
        else:
            self.chold = False


    def checkifhit(self,Bull):
        global Playerhp
        if self.hitcooldown <= 0:
            if math.pow(self.transform.pos.x-Bull.transform.pos.x,2)+math.pow(self.transform.pos.y-Bull.transform.pos.y,2) <= math.pow(self.Bullethit+Bull.Bullethit,2):
                Playerhp -= 1
                self.hitcooldown = 1
                self.sprite.image = pygame.image.load(
                    "Sprites/Player hit.png"
                )
                if Playerhp<=0:
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
            self.Bullethit = self.sprite.rect.width *0.8
        else:
            self.Bullethit = self.sprite.rect.height *0.8
        self.dead = False

    def update(self, dt):
        self.transform.pos += self.v * dt
        if abs(self.transform.pos.x)>500:
            self.dead = True
        elif abs(self.transform.pos.y)>500:
            self.dead = True
    
    def hitenemy(self, other):
        other.hp -= self.dmg 
        self.dead = True

class Player_bulletEX(Player_bullet):
    def __init__(
        self,
        pos: Vector2,
        speed: float,
        ang: float,
        image: pygame.image,
        bulletimage: pygame.image,
        dmg: float = 0,
    ):
        super().__init__(pos,speed,ang,image,dmg)
        self.time=0
        self.bulletimage=bulletimage
    def update(self, dt):
        Player_bullet.update(self,dt)
        self.time+=dt
        if self.time>=0.3:
            for i in range(4):
                spawn(Player_bullet(
                    self.transform.pos+Vector2(0,0),
                    600,
                    self.transform.rotation-15+i*10,
                    self.bulletimage,
                    self.dmg/4
                    ))
            self.dead = True

class Player_explosion(Player_bullet):
    def __init__(
        self,
        pos: Vector2,
        image: pygame.image,
        dmg: float = 0,
    ):
        super().__init__(pos,0,0,image,dmg)
        self.maxsize=self.sprite.rect.width*3
        self.sprite.rect.width=1
        self.sprite.rect.height=1
        self.Bullethit = self.sprite.rect.width *0.9
        self.enemieshit = []
        self.imgPure=self.sprite.image
        self.time=0.5
        self.sprite.image=pygame.transform.scale(self.imgPure,(self.sprite.rect.width,self.sprite.rect.height))
    def update(self, dt):
        self.time+=dt
        if self.time>3.5:
            self.dead = True
        self.sprite.rect.width=self.maxsize*(1-1/(self.time*2))
        self.sprite.rect.height=self.maxsize*(1-1/(self.time*2))
        self.sprite.image=pygame.transform.scale(self.imgPure,(self.sprite.rect.width,self.sprite.rect.height))
    def hitenemy(self, other):
        if not other in self.enemieshit:
            other.hp -= self.dmg 
            self.enemieshit.append(other)

class Player_missile(Player_bullet):
    def __init__(
        self,
        pos: Vector2,
        speed: float,
        ang: float,
        image: pygame.image,
        explosionimage:pygame.image=None,
        dmg: float = 0,
        explosiondmg: float = 0
    ):
        super().__init__(pos,speed,ang,image,dmg)
        self.explosionimage=explosionimage
        self.explosiondmg=explosiondmg
        self.aim=Vector2(0,1000)
    def update(self, dt):
        loaded_scene
        self.aim=Vector2(1000,1000)
        Player_bullet.update(self,dt)
        for e in loaded_scene.objects:
            if isinstance(e,enemy):
                if Vector2.magnitude_squared(self.transform.pos-e.transform.pos)<self.aim.magnitude_squared():
                    self.aim=e.transform.pos-self.transform.pos
            if not self.aim==Vector2(1000,1000):
                self.v+=(self.aim.normalize()*dt*10)-(self.v.normalize()*dt*5)
            self.transform.rotation=-self.v.angle_to(Vector2(0,1))
    def hitenemy(self, other):
        Player_bullet.hitenemy(self, other)
        spawn(Player_explosion(self.transform.pos+Vector2(0,0),self.explosionimage,self.explosiondmg))

class Player_laser(Player_bullet):
    def update(self, dt):
        global Playermove
        self.transform.pos += self.v * dt + Playermove * dt
    
    def hitenemy(self, other):
        global Playerlasercool
        if Playerlasercool == 0.25:
            other.hp -= self.dmg/10
        elif Playerlasercool<= 0:
            Playerlasercool=0.25
            other.hp -= self.dmg

        Playerlasercool=0.20

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
        if abs(self.transform.pos.x)>500:
            self.dead = True
        elif abs(self.transform.pos.y)>500:
            self.dead = True
    
    def checkifhit(self,Object):
        if math.pow(self.transform.pos.x-Object.transform.pos.x,2)+math.pow(self.transform.pos.y-Object.transform.pos.y,2) <= math.pow(self.Bullethit+Object.Bullethit,2):
            Object.hitenemy(self)
            if self.hp<=0:
                self.dead=True

class bossenemy(enemy):
    def __init__(
        self,
        transformation: Transform2D,
        image: pygame.image,
        nextStage:str,
        hpAll:list[float]=[0],
        timerAll:list[float]=[0],
        shotdataAll:list[list[shotdata]]=[None]
        ):
        super().__init__(transformation,image,[0,0],[0,0],hpAll[0],shotdataAll[0])
        self.hpAll=hpAll
        self.timerAll=timerAll
        self.timer=timerAll[0]
        self.shotdataAll=shotdataAll
        self.bossPhase=0
        self.nextStage=nextStage
    def update(self, dt):
        global scene_change

        self.timer -= dt
        
        if self.timer <= 0:
            self.bossPhase+=1
            self.dead=False
            if len(self.hpAll)>self.bossPhase:
                self.hp=self.hpAll[self.bossPhase]
                self.timer=self.timerAll[self.bossPhase]
                self.shotdata=self.shotdataAll[self.bossPhase]
            else:
                scene_change=self.nextStage
        self.movement(dt)
        for x in self.shotdata:
            x.update(dt, self.transform)
    def movement(self, dt):
        self.dead=False
    def checkifhit(self,Object):
        global scene_change
        enemy.checkifhit(self,Object)
        if self.dead:
            self.bossPhase+=1
            self.dead=False
            if len(self.hpAll)>self.bossPhase:
                self.hp=self.hpAll[self.bossPhase]
                self.timer=self.timerAll[self.bossPhase]
                self.shotdata=self.shotdataAll[self.bossPhase]
            else:
                scene_change=self.nextStage

class bossSpawner(GameObject):
    def __init__(self,
        bossEnemy:bossenemy,
        spawnTime:float=0,
        spawnDelay:float=0,
    ):
        self.bossenemy=bossEnemy
        self.spawntime=spawnTime
        self.spawndelay=spawnDelay
        self.dead = False
        self.noenemy = False
        self.sprite=None
    def update(self,dt):
        global loaded_scene
        self.noenemy = True
        if self.spawntime<0:
            for i in loaded_scene.objects:
                if isinstance(i,enemy):
                    self.noenemy = False
            if self.noenemy:
                if self.spawndelay<0:
                    spawn(self.bossenemy)
                    self.dead = True
                else:
                    self.spawndelay-=dt
        else:
            self.spawntime-=dt

class image(GameObject):
    def __init__(self,x,y,path,rot=0):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(path)
        self.sprite.rect = self.sprite.image.get_rect()
        self.transform = Transform2D(x,y,0)
        self.dead = False
    def update(self,dt):
        self.transform.rotation = rot*math.sin(dt)

class textobject(GameObject):
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


class Bar(GameObject):
    def __init__(self, colour, current_value, max_value, length, width, x, y):
        super().__init__()
        self.transform = Transform2D(x, y, 0)
        self.colour = colour
        self.current_value = current_value
        self.max_value = max_value
        self.length = length
        self.width = width
        self.sprite = Sprite()
        self.sprite.image = pygame.Surface([length, width])
        self.sprite.image.fill(self.colour)
        self.sprite.rect = self.sprite.image.get_rect()

    def update(self, dt):
        pressed_keys = pygame.key.get_pressed()

        length = self.length * (self.current_value/self.max_value)
        self.sprite.image = pygame.transform.scale(self.sprite.image, (length, self.width));

    def set_value(self, amount):
        self.current_value = amount
        if self.callback is not None:
            self.callback(str(self.current_value))

    def increase(self, amount):
        self.current_value += amount
        if self.callback is not None:
            self.callback(str(self.current_value))

    def decrease(self, amount):
        self.current_value -= amount
        if self.callback is not None:
            self.callback(str(self.current_value))

    def register_callback(self, callback):
        self.callback = callback


class BarWithText(GameObject):
    bar: Bar
    text: textobject

    def __init__(self, colour, text_colour, current_value, max_value, length, width, bar_x, bar_y, text_x, text_y, text_size):
        super().__init__()
        self.bar = Bar(colour, current_value, max_value, length, width, bar_x, bar_y)
        self.text = textobject(text_x, text_y, str(current_value), text_colour, text_size)
        self.bar.register_callback(self.text.changetext)
        self.first = True

    def update(self, dt):
        if self.first:
            spawn(self.bar)
            spawn(self.text)
            self.first = False
        self.bar.update(dt)
        self.text.update(dt)

    def set_value(self, amount):
        self.bar.set_value(amount)

    def increase(self, amount):
        self.bar.increase(amount)

    def decrease(self, amount):
        self.bar.decrease(amount)


class button(GameObject):
    def __init__(self,x,y,scene,text="",quitbutton=False):
        self.sprite = pygame.sprite.Sprite()
        self.transform = Transform2D(x,y,0)
        self.enabled = pygame.image.load("Sprites\Button(1).png")
        self.disabled = pygame.image.load("Sprites\Button(2).png")
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
                game_object.sprite.image,
                -game_object.transform.rotation
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
        for game_object in game_objects_with_sprites:
            render(game_object, screen)
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
