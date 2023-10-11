
#separate DrawingPygame and DrawingPyplot from the other modules later, to package those without any external dependencies


import pygame
from Physics import PointMass2, PointMass3, World2
pygame.init()

def drawCircle(x,y, r, col, simWin):
    pygame.draw.circle(simWin, col, (x,y), r)
    
def refreshWindow(simWin):
    col = (20,20,20)
    pygame.display.flip()
    simWin.fill(col)

def RUNSIM2(world:World2, settings):
    window=pygame.display.set_mode([settings["width"], settings["height"]])
    # the game loop
    running = True
    while running:
        for event in pygame.event.get():
            #all simulation events and keyboard inputs goes here

            if(event.type == pygame.QUIT):
                #this triggers the X on the window
                running = False

            elif(event.type == pygame.KEYDOWN):
                #keypresses goes here
                if pygame.K_q:
                    running = False


        #sim goes here

        for p in world.pointsList:
            drawCircle(p.x, p.y, p.radius, (200,200,200), window)
        world.update(settings)
        refreshWindow(window)

        #/sim goes here

    pygame.quit()

