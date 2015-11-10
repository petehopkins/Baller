# Class: Brick
# Represents a single brick as displayed on screen.
# Used as a target for the Ball to break

# Requires pygame
import pygame
from engine import Engine
from eventManager import Events

class Brick(Engine.GUI.Widget):
    def __init__(self, eventManager, position, fill = None, border = None, container = None):
        super().__init__(eventManager, container)

        self.eventManager = eventManager

        self.borderWidth = 2
        self.hitsRemaining = 1
        self.x = position[0]
        self.y = position[1]
        self.size = 25
        self.whRatio = {"width": 2, "height": 1}
        self.width = self.size * self.whRatio["width"]
        self.height = self.size * self.whRatio["height"]
        self.hitsRemaining = 1
        self.isInPlay = True

        if fill != None:
            self.fill = fill
        else:
            self.fill = Engine.Colors.LAVENDER

        if border != None:
            self.border = border
        else:
            self.border = Engine.Colors.BLACK

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.inner = pygame.Surface((self.width - (self.borderWidth * 2), self.height - (self.borderWidth * 2)))
        self.innerRect = self.inner.get_rect()
        self.innerRect.x = (self.rect.width / 2) - (self.innerRect.width / 2)
        self.innerRect.y = (self.rect.height / 2) - (self.innerRect.height / 2)

        self.redrawBrick()

    def notify(self, event):
        if isinstance(event, Events.CollisionEvent):
            if event.obj == self:
                self.collide()

    def addListeners(self):
        event = Events.CollisionEvent()
        self.eventManager.addListener(event, self)


    def update(self):
        pass

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def removeFromPlay(self):
        self.isInPlay = False #set flag

    def redrawBrick(self):
        self.image.fill(self.border)
        self.inner.fill(self.fill)
        self.image.blit(self.inner, self.innerRect)

    def animate(self):
        if self.hitsRemaining == 1:
            self.fill = Engine.Colors.LAVENDER
        elif self.hitsRemaining == 0:
            self.fill = Engine.Colors.GREY
        else:
            self.fill = Engine.Colors.BLACK
            self.removeFromPlay() #no hits remaining, get rid of this one

        self.redrawBrick()

    def collide(self):
        self.hitsRemaining -= 1 #decrement hits
        self.animate() #and animate the hit
