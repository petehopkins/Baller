import pygame
from brick import *

class Bricks():
    def __init__(self, eventManager, window, gap = 2):
        self.eventManager = eventManager
        self.__pile = pygame.sprite.Group()
        self.createWall(eventManager, window, gap)

    def getPile(self):
        return self.__pile

    def createWall(self, eventManager, window, gap):
        brick = Brick(eventManager, [0,0])
        availableWidth = window.get_width()
        availableHeight = window.get_height() - 200 #allocate 200px on bottom for paddle and maneuvering space

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

