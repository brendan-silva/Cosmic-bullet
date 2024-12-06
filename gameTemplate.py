import pygame
from pygame.locals import *
from math import *

size = 1536, 864
width, height = size
BLACK = (50,50,50)
WHITE = (255,255,255)
RED = (255,0,0)
screen = "home"

pygame.init()
screen = pygame.display.set_mode(size)
running = True

exitB = Button()#
newGameB = Button()#
###

while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    if screen = "home":
        if exitB.clicked():
            running = False
        elif newGameB.clicked():
            screen = "game"
            stage = "enemy"
            p = Player()#
            eT = 0
            ###
        else:
            ###

    #######    
    elif screen = "game":
        if stage = "enemy":
            if eT > n:
                stage = "boss"
                bT = 0
                ###
            else:
                eT += 1
                ###
        else:
            if bT = n:
                b = Boss()#
                ###
            if bT > n:
                if b.dead():
                    screen = "win"
                    homeB = Button()
                    ###
                else:
                    ###
            bT += 1
        if p.dead():
            screen = "death"
            restartB = Button()#
            homeB = Button()#
            ###
    #######
        
    elif screen = "death":
        if restartB.clicked():
            screen = "game"
            stage = "enemy"
            p = Player#
            eT = 0
            ###
        elif homeB.clicked():
            screen = "home"
            exitB = Button()#
            newGameB = Button()#
            ###
        else:
            ###
            
    elif screen = "win":
        if homeB.clicked():
            screen = "home"
            exitB = Button()#
            newGameB = Button()#
            ###
        else:
            ###
        
    pygame.display.update()

pygame.quit()
