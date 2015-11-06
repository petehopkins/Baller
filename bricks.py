import pygame
from brick import *

class Bricks():
    __pile = []

    def __init__(self, stage, gap = 2):
        self.__pile = pygame.sprite.Group()
        self.createWall(stage, gap)

    def getPile(self):
        return self.__pile

    def createWall(self, stage, gap):
        brick = Brick([0,0])
        availableWidth = stage.get_width()
        availableHeight = stage.get_height() - 200 #allocate 200px on bottom for paddle and manuevering space

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
                brick = Brick(position)
                self.__pile.add(brick)
        
        
    def redrawWall(self, stage):
        self.__pile.draw(stage)
