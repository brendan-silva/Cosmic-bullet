from abc import ABCMeta, abstractmethod
from pygame import Vector2, Rect
from pygame.sprite import Sprite
from pygame.locals import *
import pygame
from typing_extensions import Self
import math
import copy
import random
running = True
Playermove = Vector2(0, 0)
Playerlaseroff = True
Playerlasercool = 0
Playerhp=10
Playerscrap=1
PlayerEXcharge = 50
EXchargeON = False
Score=0
file = open("PersonalBest.txt","r")
PB = math.ceil(float(file.read()))
file.close()
killbullet=False
itemimage=[[pygame.image.load("Sprites\items\itemEnergy1.png"),
            pygame.image.load("Sprites\items\itemEnergy10.png"),
            pygame.image.load("Sprites\items\itemEnergy100.png")
            ],[
            pygame.image.load("Sprites\items\itemScrap1.png"),
            pygame.image.load("Sprites\items\itemScrap10.png"),
            pygame.image.load("Sprites\items\itemScrap100.png")
            ],[
            pygame.image.load("Sprites\items\itemStar1.png"),
            pygame.image.load("Sprites\items\itemStar10.png"),
            pygame.image.load("Sprites\items\itemStar100.png"),
            ]]
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
    have to be overridden.

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
        self.transform = Transform2D(0, (-1*HEIGHT/4), 0)
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
        global EXchargeON
        EXchargeON = self.EXchargeON
        if self.EXchargeON:
            PlayerEXcharge-=dt*25
        elif PlayerEXcharge < 125:
            PlayerEXcharge+=dt*5
        if PlayerEXcharge<1:
            self.EXchargeON =False
        if self.hitcooldown >= 0:
            self.hitcooldown -= dt
            if self.hitcooldown <= 0:
                self.sprite.image = pygame.image.load(
                    "Sprites/Player.png"
                )
        Playerlasercool-=dt
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
        
        #shot types
        if self.shot_on and self.shotcooldown <= 0 :
            if not self.EXchargeON:
                #dps roof of 70
                if self.shottype == 0:
                    for i in range(-3, 5):
                        spawn(
                            Player_bullet(
                                self.transform.pos + Vector2(4, 20),
                                600,
                                (5 * i) - 2.5,
                                self.bulletimg,
                                1.75,
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
                #dps roof of 140
                if self.shottype == 0:
                    for i in range(-1, 3):
                        spawn(
                            Player_bulletEX(
                                self.transform.pos + Vector2(4, 20),
                                600,
                                (10 * i) - 5,
                                self.bulletimgEX,
                                self.bulletimg,
                                7,
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
        if PlayerEXcharge<=1:
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
        global killbullet
        if self.hitcooldown <= 0:
            if math.pow(self.transform.pos.x-Bull.transform.pos.x,2)+math.pow(self.transform.pos.y-Bull.transform.pos.y,2) <= math.pow(self.Bullethit+Bull.Bullethit,2):
                Playerhp -= 1
                self.hitcooldown = 1
                killbullet=True
                self.sprite.image = pygame.image.load(
                    "Sprites/Player hit.png"
                )
                if Playerhp<=0:
                    Score = 0
                    self.dead=True
                    if loaded_scene != 'death':
                        global scene_change
                        scene_change = 'death'

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
        self.EX=loaded_scene.player.EXchargeON

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
        if self.time>=0.5:
            for i in range(4):
                spawn(Player_bullet(
                    self.transform.pos+Vector2(0,0),
                    600,
                    self.transform.rotation-15+i*10,
                    self.bulletimage,
                    self.dmg/4
                    ))
            self.dead = True
    def hitenemy(self, other):
        Player_bullet.hitenemy(self, other)
        itemgroupspawn(self.transform.pos,[2,0,0],10)

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
        if self.time>1.5:
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
        if self.EX:
                itemgroupspawn(self.transform.pos,[0,3,0],10)

class Player_laser(Player_bullet):
    def update(self, dt):
        self.transform.pos += self.v * dt + Playermove * dt
    
    def hitenemy(self, other):
        global Playerlasercool
        if Playerlasercool == 0.20:
            other.hp -= self.dmg/10
            if loaded_scene.player.EXchargeON:
                itemgroupspawn(self.transform.pos,[0,0,1],10)
        elif Playerlasercool<= 0:
            Playerlasercool=0.20
            other.hp -= self.dmg
            if self.EX:
                itemgroupspawn(self.transform.pos,[0,0,10],10)
            


class item(GameObject):
    #type(0=Energy,1=Scrap,2=Star)
    def __init__(
        self,
        pos: Vector2,
        image: pygame.image,
        potency: int = 1,
        itemtype:int=0
    ):
        self.transform = Transform2D(pos.x, pos.y, 0)
        self.v = pygame.Vector2(0, -150)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.sprite.rect = self.sprite.image.get_rect()
        self.potency = potency
        self.itemtype = itemtype
        self.itemget = (self.sprite.rect.width *1.4)**2
        self.followplayer=False
        self.dead = False
    def update(self, dt):
        global loaded_scene
        global Playerscrap
        global PlayerEXcharge
        global Score
        if self.followplayer:
            self.transform.pos+=pygame.Vector2.normalize(loaded_scene.player.transform.pos-self.transform.pos)*dt*400
            if pygame.Vector2.magnitude_squared(loaded_scene.player.transform.pos-self.transform.pos)<self.itemget:
                if self.itemtype==0:
                    if PlayerEXcharge < 250:
                        if self.potency > (250 - PlayerEXcharge):
                            Score+=self.potency - (250 - PlayerEXcharge)
                            PlayerEXcharge = 250
                        else:
                            PlayerEXcharge+=self.potency
                    else:
                        Score+=self.potency*2**(Score/2000)
                elif self.itemtype==1:
                    Playerscrap+=self.potency
                else:
                    Score+=self.potency
                self.dead = True
        else:
            self.transform.pos+=self.v*dt
            if pygame.Vector2.magnitude_squared(loaded_scene.player.transform.pos-self.transform.pos)<100**2 or loaded_scene.player.transform.pos.y >216:
                self.followplayer = True

def itemgroupspawn(pos: Vector2,itemvalues:list[int]=[0,0,0],area:float=0):
    #type(0=Energy,1=Scrap,2=Star)
    itemtype=0
    itemscale=2
    while itemvalues!=[0,0,0]:
        while itemvalues[itemtype]<10**itemscale:
            if itemscale == 0:
                itemscale=2
                itemtype+=1
            else:
                itemscale-=1
        spawn(item(pos+pygame.Vector2.rotate(pygame.Vector2(0,random.randrange(0 ,area)),random.randrange(0,360)),
                itemimage[itemtype][itemscale],
                10**itemscale,itemtype))
        itemvalues[itemtype]-=10**itemscale

class Bullet(GameObject):
    def __init__(
        self,
        transformation: Transform2D,
        image: pygame.image,
        v: list[float, float],
        a: list[float, float],
    ):
        self.transform = transformation
        if a[0]*2>v[0]:
            self.transform.rotation=a[1]
        else:
            self.transform.rotation=v[1]
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
        hp:float=1,
        itemdata:list[int,int,int,float]=[0,0,0,0]
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
        self.itemdata=itemdata


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
                        self.aaaa,
                        self.itemdata
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
        itemdata:list[int,int,int,float]=[0,0,0,0]
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
        self.itemdata=itemdata
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
                itemgroupspawn(self.transform.pos,self.itemdata[0:3],self.itemdata[3])
                self.itemdata=[0,0,0,0]

class bossenemy(enemy):
    def __init__(
        self,
        transformation: Transform2D,
        image: pygame.image,
        nextStage:str,
        hpAll:list[float]=[0],
        timerAll:list[float]=[0],
        shotdataAll:list[list[shotdata]]=[None],
        itemdataAll:list[list[int,int,int,float]]=[[0,0,0,0]]
        ):
        super().__init__(transformation,image,[0,0],[0,0],hpAll[0],shotdataAll[0],itemdataAll[0])
        self.hpAll=hpAll
        self.timerAll=timerAll
        self.timer=timerAll[0]
        self.shotdataAll=shotdataAll
        self.itemdataAll=itemdataAll
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
        global PB
        global killbullet
        enemy.checkifhit(self,Object)
        if self.dead:
            self.bossPhase+=1
            self.dead=False
            killbullet=True
            if len(self.hpAll)>self.bossPhase:
                self.hp=self.hpAll[self.bossPhase]
                self.timer=self.timerAll[self.bossPhase]
                self.shotdata=self.shotdataAll[self.bossPhase]
                self.itemdata=self.itemdataAll[self.bossPhase]
            else:
                if Score > PB:
                    PB = math.ceil(Score)
                file = open("PersonalBest.txt","r")
                if PB > float(file.read()):
                    file.close()
                    file = open("PersonalBest.txt","w")
                    file.write(str(PB))
                print(PB)
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
    def __init__(self,x,y,path="Sprites\sidebar.png"):
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
    def __init__(self,x,y,path,rot=0):
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load(path)
        self.sprite.rect = self.sprite.image.get_rect()
        self.transform = Transform2D(x,y,0)
        self.dead = False
    def update(self,dt):
        self.transform.rotation = rot*(dt)
        
class textobject(UI):
    def __init__(self,x,y,text,colour,size=72,scoretxt=(0,False)):
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
        self.score = scoretxt
    def update(self,dt):
        if self.score[1]:
            if self.score[0] == 0:
                self.text = str(Score)
            else:
                self.text = self.text[0:self.score[0]]
                self.text += str(math.ceil(Score))    
        self.changetext(self.text,False)
    def changetext(self,text,recenter=False):
        self.sprite.image = pygame.font.Font.render(self.font,text,False,self.colour)
        self.sprite.rect = self.sprite.image.get_rect()
        if recenter:
            self.sprite.rect.center = self.center

#Cole
class Bar(UI):
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

#Kirin
class statusbar(UI):
    def __init__(self,x,y,folder="defaultbar",maxval=200,baseval=0):
        self.transform = Transform2D(x,y,0)
        self.sprite = pygame.sprite.Sprite()
        self.root = folder
        self.image = pygame.surface.Surface((273,96))
        self.icon = pygame.transform.scale_by(pygame.image.load("Sprites\\"+self.root+"\Icon.png"),3)
        self.bg = pygame.transform.scale_by(pygame.image.load("Sprites\\"+self.root+"\BG.png"),3)
        self.bar = pygame.transform.scale_by(pygame.image.load("Sprites\\"+self.root+"\Bar.png"),3)
        self.image.blits([(self.bg,(84,18)),(self.bar,(87,21)),(self.icon,(0,0))]) 
        self.sprite.image = self.image
        self.sprite.rect = self.sprite.image.get_rect()
        self.val = baseval
        self.max = maxval
        self.dead = False
        self.hastext = False
    def update(self,dt):
        self.bar = pygame.transform.scale(self.bar,(math.ceil(180*(self.val/self.max)),54))
        self.image.fill((164,111,43))
        if self.val > 1:
            self.image.blits([(self.bg,(84,18)),(self.bar,(87,21)),(self.icon,(0,0))])
        else:
            self.image.blits([(self.bg,(84,18)),(self.icon,(0,0))])
        self.sprite.image = self.image
        self.sprite.rect = self.sprite.image.get_rect()

class scrap_bar(statusbar):
    def __init__(self,x,y):
        super().__init__(x,y,folder="Scrapbar")
        self.max = 25 * Playerhp**2 + 75
        self.val = Playerscrap
        self.text = textobject(x,y,str(Playerhp),(255, 132, 0),90)
        self.text2 = textobject(x,y,str(Playerhp),(128, 66, 0),108)
        self.text.center = (48,48)
        self.text2.center = (47,48)
        self.image.blit(self.text.sprite.image,self.text.sprite.rect)
    def update(self,dt):
        global Playerhp
        global Playerscrap
        self.max = 25 * Playerhp**2 + 75
        for i in range(5):
            if self.val < Playerscrap:
                self.val += 1
        if self.val >= self.max:
            Playerscrap -= self.max-1
            self.val = 1
            Playerhp += 1
            self.max = 25 * Playerhp**2 + 75
        self.text.changetext(str(Playerhp),True)
        self.text2.changetext(str(Playerhp),True)
        super().update(dt)
        self.image.blit(self.text2.sprite.image,self.text2.sprite.rect)
        self.image.blit(self.text.sprite.image,self.text.sprite.rect)

class energy_bar(statusbar):
    def __init__(self,x,y):
        super().__init__(x,y,folder="Energybar")
        self.max = 250
        self.val = PlayerEXcharge
    def update(self,dt):
        if EXchargeON:
            self.icon = pygame.transform.scale_by(pygame.image.load("Sprites\Energybar\Icon_A.png"),3)
        else:
            if PlayerEXcharge >= 200:
                self.icon = pygame.transform.scale_by(pygame.image.load("Sprites\Energybar\Icon_B.png"),3)
            elif PlayerEXcharge >= 50:
                self.icon = pygame.transform.scale_by(pygame.image.load("Sprites\Energybar\Icon_C.png"),3)
            else:
                self.icon = pygame.transform.scale_by(pygame.image.load("Sprites\Energybar\Icon_D.png"),3)
        #self.val = PlayerEXcharge
        for i in range(5):
            if self.val < PlayerEXcharge:
                self.val += 1
            elif self.val > PlayerEXcharge and self.val > 1:
                self.val -= 1
        super().update(dt)

class button(UI):
    def __init__(self,x,y,scene,text="",quitbutton=False,superquit=False):
        self.sprite = pygame.sprite.Sprite()
        self.transform = Transform2D(x,y,0)
        self.enabled = pygame.image.load("Sprites\Button(1B).png")
        self.disabled = pygame.image.load("Sprites\Button(2B).png")
        self.type = textobject(0,0,text,DARKBLUE)
        self.text = text
        self.update_sprite(self.enabled,DARKBLUE)
        self.sprite.rect = self.sprite.image.get_rect()
        self.dead = False
        self.scene = scene
        self.quitbutton = quitbutton
        self.superquit = superquit
    def update_sprite(self,image,colour):
        self.type = textobject(0,0,self.text,colour)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = image
        self.sprite.rect = self.sprite.image.get_rect()
        coords = (self.sprite.rect.center[0]-self.type.sprite.rect.width/2,self.sprite.rect.center[1]-self.type.sprite.rect.height/2)
        self.sprite.image.blit(self.type.sprite.image,coords)
    def update(self,dt):
        global mousedown
        if self.sprite.rect.collidepoint((self.transform.pos[0]+pygame.mouse.get_pos()[0]-WIDTH/2+self.sprite.rect.width/2,self.transform.pos[1]+pygame.mouse.get_pos()[1]-HEIGHT/2+self.sprite.rect.height/2)):
            self.update_sprite(self.disabled,LIGHTBLUE)
            if mousedown == True:
                if self.quitbutton:
                    global running
                    global game_loop
                    if self.superquit:
                        global PB
                        if Score > PB:
                            PB = math.ceil(Score)
                        file = open("PersonalBest.txt","r")
                        if PB > float(file.read()):
                            file.close()
                            file = open("PersonalBest.txt","w")
                            file.write(str(PB))
                        file.close()
                        running = False
                    game_loop = False
                if self.scene != "":
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
    global running
    global game_loop
    global killbullet
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
    global Score
    global PB
    if Score > PB:
        PB = math.ceil(Score)
    Score = 0

    while game_loop:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                game_loop = False
                running = False
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
        object_matrix = [[],[],[],[],[],[],[],[]]
        for game_object in game_objects_with_sprites:
            if isinstance(game_object,background):
                object_matrix[0].append(game_object)
            elif isinstance(game_object,enemy):
                object_matrix[1].append(game_object)
            elif isinstance(game_object,Player):
                object_matrix[2].append(game_object)
            elif isinstance(game_object,Player_bullet):
                object_matrix[3].append(game_object)
            elif isinstance(game_object,item):
                object_matrix[4].append(game_object)
            elif isinstance(game_object,Bullet):
                object_matrix[5].append(game_object)
            elif isinstance(game_object,sidebar):
                object_matrix[6].append(game_object)
            elif isinstance(game_object,UI):
                object_matrix[7].append(game_object)
        for array in object_matrix:
            for thing in array:
                render(thing, screen)
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
            if loaded_scene.objects[i].dead or (Playerlaseroff and isinstance(loaded_scene.objects[i], Player_laser)) or (killbullet and isinstance(loaded_scene.objects[i],Bullet)):
                del loaded_scene.objects[i]
            else:
                i += 1
        killbullet=False
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
