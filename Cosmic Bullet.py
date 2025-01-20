from engine import *
from pygame import Rect
from pygame.locals import *
import pygame
import engine

def stage_1() -> Scene:
    new_scene = Scene(
        Player(),
        wavedata(
            Transform2D(0, 200, 0),
            pygame.image.load("Sprites\Enemy.png"),
            [10, 180],
            [0, 0],
            1,
            0.5,
            2,
            [0,0,0,0],
            [0,72,0,0],
            5,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Sprites\Enemy Bullet 1.png"),
                    [100, 0],
                    [0, 0],
                    1,
                    0.1,
                    0,
                    [0, 0, 0, 0],
                    [0, 11, 0, 0],
                )
            ],
            100,
            [111,111,111,100]
        ),
        #BarWithText((255, 0, 0), (255, 255, 255), 100, 100, 300, 30, 550, 400, 450, 400, 72),
        bossSpawner(
        bossenemy(
            Transform2D(0, 200, 0),
            pygame.image.load("Sprites\Boss Enemy.png"),
            'victory',
            [2000,2000],
            [60,60],
            [
                [
                    shotdata(
                        Transform2D(0, 0, 0),
                        pygame.image.load("Sprites\Enemy Bullet 1.png"),
                        [10, 0],
                        [100, 0],
                        12,
                        0.1,
                        0,
                        [0, 30, 0, 0],
                        [0, 0, 0, 141],
                    )
                ],
                [
                    shotdata(
                        Transform2D(0, 0, 0),
                        pygame.image.load("Sprites\Enemy Bullet 1.png"),
                        [10, 0],
                        [100, 0],
                        12,
                        0.05,
                        0,
                        [0, 30, 0, 0],
                        [0, 0, 0, 141],
                    )
                ],
            ],
            [[25,25,25,100],[25,25,25,100]]
        ),
        1,
        1,
        ),
        background(324,1296,"Sprites\Background.png",10),
        sidebar(-324,432),
        sidebar(768,432),
        scrap_bar(-555,108),
        energy_bar(-555,-108),
        textobject(555,0,"Score: ",(255,255,0),72,(7,True)),
    )
    return new_scene

def stage_2() -> Scene:
    new_scene = Scene(
        Player(),
        wavedata(
            Transform2D(0, 300, 0),
            pygame.image.load("Sprites\Enemy.png"),
            [10, 180],
            [0, 0],
            1,
            0.5,
            2,
            [0,0,0,0],
            [0,72,0,0],
            5,
            [
                shotdata(
                    Transform2D(0, 0, 0),
                    pygame.image.load("Sprites\Enemy Bullet 1.png"),
                    [100, 0],
                    [0, 0],
                    1,
                    0.1,
                    0,
                    [0, 0, 0, 0],
                    [0, 11, 0, 0],
                )
            ],
            100,
            [25,25,25,100]
        ),
        sidebar(-324,432),
        sidebar(768,432),
        scrap_bar(-555,108),
        energy_bar(-555,-108)
    )
    return new_scene

def main_menu() -> Scene:
    new_scene = Scene(
        background(768,432,"Sprites\MainBG.png"),
        image(0,150,"Sprites\Logo.png"),
        button(250,-250,"stage_1","Begin Game"),
        button(-250,-250,"","Quit",True,True),
        textobject(0,-120,"High Score: "+hs,(255,255,0))
        )
    return new_scene

def death() -> Scene:
    new_scene = Scene(
        background(768,432,"Sprites\MainBG.png"),
        textobject(0,0,"You Died!!!",(255,0,0)),
        button(250,-200,"","Return to Menu",True),
        button(-250,-200,"","Quit",True,True)
        )
    return new_scene

def victory() -> Scene:
    new_scene = Scene(
        background(768,432,"Sprites\MainBG.png"),
        textobject(0,100,"You beat the boss!",(0,255,0)),
        textobject(0,0,"Your score was: 0",(255,255,0),72,(16,True)),
        button(250,-200,"","Return to Menu",True),
        button(-250,-200,"","Quit",True,True)
        )
    return new_scene

hs = str(engine.PB)
while engine.running == True:
    main('main_menu',lib={'victory':victory(),'death':death(),'stage_1':stage_1(),'stage_2':stage_2(),'main_menu':main_menu()})
    hs = str(engine.PB)
