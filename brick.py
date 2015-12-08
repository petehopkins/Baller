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

        self.isCollidable = True

        self.width = self.options.brickWidth
        self.height = self.options.brickHeight
        self.borderWidth = self.options.brickBorderWidth
        self.hitsRemaining = self.options.brickHitsRemaining

        self.isInPlay = True

        self.fill = fill if fill != None else Engine.Colors.GREY
        self.border = border if border != None else Engine.Colors.BLACK

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.inner = pygame.Surface((self.width - (self.borderWidth * 2), self.height - (self.borderWidth * 2)))
        self.innerRect = self.inner.get_rect()
        self.innerRect.x = (self.rect.width / 2) - (self.innerRect.width / 2)
        self.innerRect.y = (self.rect.height / 2) - (self.innerRect.height / 2)

        self.animate()
        self.redrawBrick()

    @staticmethod
    def createWall(eventManager, options):
        pile = pygame.sprite.Group()

        ballparkWide = options.brickWallWidth // options.brickWidth
        ballparkHigh = options.brickWallHeight // options.brickHeight

        whitespaceWide = options.brickWallMortarGap + (options.brickWallMortarGap * ballparkWide)
        whitespaceHigh = options.brickWallMortarGap + (options.brickWallMortarGap * ballparkHigh)

        bricksWide = int(options.brickWallWidth - whitespaceWide) // options.brickWidth
        bricksHigh = int(options.brickWallHeight - whitespaceHigh) // options.brickHeight

        borderSpace = (options.brickWallWidth - (bricksWide * options.brickWidth) - whitespaceWide) // 2
        leftBorder = options.brickWallMinimumOffset + borderSpace + options.brickWallMortarGap
        rightBorder = options.brickWallWidth - borderSpace - options.brickWallMortarGap
        topBorder = options.brickWallMinimumOffset

        for x in range(0, bricksWide):
            for y in range(0, bricksHigh):
                position = [leftBorder + options.brickWallMortarGap + ((options.brickWidth + options.brickWallMortarGap) * x), topBorder + options.brickWallMortarGap + ((options.brickHeight + options.brickWallMortarGap) * y)]
                brick = Brick(eventManager, position)
                pile.add(brick)

        return pile.sprites()

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

        event = Events.StatUpdateEvent(stat = Engine.Stats.SCORE, value = 1)
        self.eventManager.post(event)

        self.kill()

    def redrawBrick(self):
        self.image.fill(self.border)
        self.inner.fill(self.fill)
        self.image.blit(self.inner, self.innerRect)

    def animate(self):
        if self.hitsRemaining == 3:
            self.fill = Engine.Colors.DARK_BLUE

        elif self.hitsRemaining == 2:
            self.fill = Engine.Colors.LAVENDER

        elif self.hitsRemaining == 1:
            self.fill = Engine.Colors.LIGHT_GREY

        elif self.hitsRemaining == 0:
            self.fill = Engine.Colors.GREY
        else:
            self.fill = Engine.Colors.BLACK
            self.removeFromPlay() #no hits remaining, get rid of this one

        self.redrawBrick()

    def collide(self):
        self.hitsRemaining -= 1 #decrement hits
        self.animate() #and animate the hit
