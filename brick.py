# Class: Brick
# Represents a single brick as displayed on screen.
# Used as a target for the Ball to break

# Requires pygame
import pygame

class Brick(pygame.sprite.Sprite):
    def init(self, eventManager, position, fill = None, border = None):
        from Game import Engine

        super().init()
        
        self.eventManager = eventManager
        
        self.borderWidth = 2
        self.hitsRemaining = 1
        self.x = position[0]
        self.y = position[1]
        self.size = 25
        self.whRatio = {"width": 2, "height": 1}
        self.width = size * whRatio["width"]
        self.height = size * whRatio["height"]
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

        self.brick = pygame.Surface((self.width, self.height))
        self.brickRect = self.brick.get_rect()
        self.brickRect.x = self.x
        self.brickRect.y = self.y
        self.brick.fill(self.border)
        
        self.inner = pygame.Surface((self.width - (self.borderWidth * 2), self.height - (self.borderWidth * 2)))
        self.innerRect = self.inner.get_rect()
        self.innerRect.x = (self.brickRect.width / 2) - (self.innerRect.width / 2)
        self.innerRect.y = (self.brickRect.height / 2) - (self.innerRect.height / 2)
        self.inner.fill(self.fill)

        self.brick.blit(self.inner, self.innerRect)
    
    def notify(self, event):
        if isinstance(event, CollisionEvent):
            if event.obj == self:
                self.collide()

    def update(self):
        pass

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def removeFromPlay(self):
        self.isInPlay = False #set flag

    def animate(self):
        if self.hitsRemaining <= 0:
            self.removeFromPlay() #no hits remaining, get rid of this one

    def collide(self):
        self.hitsRemaining -= 1 #decrement hits
        self.animate() #and animate the hit

    def stack(self, window):
        if self.isInPlay:
           window.blit(self.brick, self.rect) #draw border
