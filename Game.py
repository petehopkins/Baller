#Game class
# The main class which will provide the framework for the rest of the
# game objects to run in.
# Includes the main event loop, clock, window settings, etc.

# Requires pygame

import pygame

class Game():
    name = "Baller: Defeat the oppressive war machine of the evil Quadratic invaders!"
    stageWidth = 800
    stageHeight = 600
    stageSize = (stageWidth, stageHeight)
    stageFillColor = (255, 255, 255)
    tickSpeed = 60
    
    @staticmethod
    def end():
        pygame.display.quit()
        pygame.quit()
    
    pygame.init()
    stage = pygame.display.set_mode(stageSize)
    pygame.display.set_caption(name)
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        
        #pass the variable "stage" to your object's initializer to have access to the screen/window/stage thingy for drawing on it
        #also, put calls to animate things in this loop
        
        pygame.display.flip()
        clock.tick(tickSpeed)
        
Game()
Game.end()
