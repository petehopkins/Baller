import pygame
from brick import *

class Bricks():
    def __init__(self, eventManager, availableWidth, availableHeight, gap = 2):
        self.eventManager = eventManager
        self.__pile = pygame.sprite.Group()
        self.createWall(eventManager, availableWidth, availableHeight, gap)

    def getPile(self):
        return self.__pile

    def createWall(self, eventManager, availableWidth, availableHeight, gap):
        brick = Brick(eventManager, [0,0])

        availableHeight -= 200 #allocate space at bottom for paddle
        
        ballparkWide = availableWidth // brick.getWidth()
        ballparkHigh = availableHeight // brick.getHeight()

        whitespaceWide = gap + (gap * ballparkWide)
        whitespaceHigh = gap + (gap * ballparkHigh)

        bricksWide = (availableWidth - whitespaceWide) // brick.getWidth()
        bricksHigh = (availableHeight - whitespaceHigh) // brick.getHeight()

        borderSpace = (availableWidth - (bricksWide * brick.getWidth()) - whitespaceWide) // 2
        leftBorder = borderSpace + gap
        rightBorder = availableWidth - borderSpace - gap

        for x in range(0, bricksWide):
            for y in range(0, bricksHigh):
                position = [leftBorder + gap + ((brick.getWidth() + gap) * x), gap + ((brick.getHeight() + gap) * y)]
                brick = Brick(self.eventManager, position)
                self.__pile.add(brick)

