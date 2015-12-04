import pygame
from engine import *
from eventManager import Events

class Paddle(Engine.GUI.Widget):
    def __init__(self, eventManager):

        super().__init__(eventManager)

        self.width = self.options.paddleWidth
        self.height = self.options.paddleHeight

        self.minx = self.options.levelZonePaddleArea["x"] + self.options.paddleLeftBound
        self.maxx = (self.options.levelZonePaddleArea["x"] + self.options.levelZonePaddleArea["width"]) - (self.width + self.options.paddleRightBound)

        self.x = self.options.paddleX

        self.color = self.options.paddleColor

        self.sensitivity = self.options.sensitivityValue
        self.tickCounter = 0

        self.isCollidable = True

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.options.paddleY

    def addListeners(self):
        event = Events.TickEvent()
        self.eventManager.addListener(event, self)

        event = Events.PaddleMoveEvent()
        self.eventManager.addListener(event, self)

    def notify(self, event):
        if isinstance(event, Events.TickEvent):
            self.tickCounter += 1 # increment counter
            self.tickCounter %= self.sensitivity # and reset when it reaches the sensitivity value to keep the numbers sane

        if isinstance(event, Events.PaddleMoveEvent):
            if self.tickCounter == 0: # ok to move now
                self.move(event.pos[0])

    def update(self):
        self.minx = self.options.levelZonePaddleArea["x"] + self.options.paddleLeftBound
        self.maxx = (self.options.levelZonePaddleArea["x"] + self.options.levelZonePaddleArea["width"]) - (self.width + self.options.paddleRightBound)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.options.paddleY

    def getPosition(self):
        return (self.rect.x, self.rect.y)

    def move(self, x):
        if x < self.minx:
            x = self.minx

        if x > self.maxx:
            x =self.maxx

        self.x = x

    def collide(self, zone = None, rect = None):
        collision = False

        if zone == None:
            zone = self.rect

        if rect != None:
            collision = (rect.x <= zone.x <= rect.x + rect.width or zone.x <= rect.x <= zone.x + zone.width) and \
                        (rect.y <= zone.y <= rect.y + rect.height or zone.y <= rect.y <= zone.y + zone.height)

        return collision

    def redirect(self, ball):
        oldVector = ball.vector

        # figure out where collision occurred
        if self.collide(self.centerZone(), ball.centerZone()):
            ball.vector = 270 # towards top of screen

        elif self.collide(self.leftNearZone(), ball.rect):
            ball.vector = 225 # towards topleft of screen

        elif self.collide(self.rightNearZone(), ball.rect):
            ball.vector = 315 # towards topright of screen

        elif self.collide(self.leftFarZone(), ball.rect):
            ball.vector = 210 # towards lefttop of screen

        elif self.collide(self.rightFarZone(), ball.rect):
            ball.vector = 330 # towards righttop of screen

##        ls = [self.rect, self.leftFarZone(), self.leftNearZone(), self.centerZone(), self.rightNearZone(), self.rightFarZone()]
##        for rect in ls:
##            print("x x+w w y y+h h: ", rect.x, rect.x + rect.width, rect.width, rect.y, rect.y + rect.height, rect.height)

