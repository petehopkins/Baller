# Class: Brick
# Represents a single brick as displayed on screen.
# Used as a target for the Ball to break

# Requires pygame
import pygame

class Brick(pygame.sprite.Sprite):
    __borderWidth = 2
    __hitsRemaining = 1
    __position = {"x": 0, "y": 0}
    __size = 25
    __whRatio = {"width": 2, "height": 1}
    __width = __size * __whRatio["width"]
    __height = __size * __whRatio["height"]
    __outerRect = pygame.Rect(__position["x"], __position["y"], __width, __height)
    __innerRect = pygame.Rect(__position["x"] + __borderWidth, __position["y"] + __borderWidth, __width - (__borderWidth * 2), __height - (__borderWidth * 2))
    __isInPlay = True

    def __init__(self, position, fill = None, border = None):
        from Game import Engine

        super().__init__()

        if fill != None:
            self.__fill = fill
        else:
            self.__fill = Engine.Colors.LAVENDER

        if border != None:
            self.__border = border
        else:
            self.__border = Engine.Colors.BLACK

        self.__position["x"] = position[0]
        self.__position["y"] = position[1]
        self.__outerRect = pygame.Rect(self.__position["x"], self.__position["y"], self.__width, self.__height)
        self.__innerRect = pygame.Rect(self.__position["x"] + self.__borderWidth, self.__position["y"] + self.__borderWidth, self.__width - (self.__borderWidth * 2), self.__height - (self.__borderWidth * 2))
        self.__hitsRemaining = 1

        self.rect = self.__outerRect
        self.image = pygame.Surface([self.__width, self.__height])
        self.image.fill(self.__border)

        self.brick = pygame.Surface((self.__innerRect.width, self.__innerRect.height))
        self.brick.fill(self.__fill)

        self.image.blit(self.brick, self.__innerRect)

    def update(self):
        pass

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def __removeFromPlay(self):
        self.__isInPlay = False #set flag

    def __animate(self):
        if self.__hitsRemaining <= 0:
            self.__removeFromPlay() #no hits remaining, get rid of this one

    def collide(self):
        self.__hitsRemaining -= 1 #decrement hits
        self.__animate() #and animate the hit

    def stack(self, stage):
        if self.__isInPlay:
           stage.blit(self, self.rect) #draw border
