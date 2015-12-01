import pygame
from engine import *
from eventManager import Events

class Paddle(Engine.GUI.Widget):
    def __init__(self, eventManager):

        super().__init__(eventManager)

        self.width = self.options.paddleWidth
        self.height = self.options.paddleHeight

        self.minx = self.options.paddleLeftBound
        self.maxx = self.options.windowWidth - self.options.paddleRightBound - self.width

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
            collision = rect.x <= zone.x <= rect.x + rect.width and \
                        rect.y <= zone.y <= rect.y + rect.height

        return collision

    def redirect(self, ball):
        # figure out where collision occurred
        if self.centerZone().colliderect(ball.centerZone()):
            ball.vector = 270 # towards top of screen
            print("center")
        elif self.leftNearZone().colliderect(ball.rect):
            ball.vector = 225 # towards topleft of screen
            print("left near")
        elif self.rightNearZone().colliderect(ball.rect):
            ball.vector = 315 # towards topright of screen
            print("right near")
        elif self.leftFarZone().colliderect(ball.rect):
            ball.vector = 210 # towards lefttop of screen
            print("left far")
        elif self.rightFarZone().colliderect(ball.rect):
            ball.vector = 330 # towards righttop of screen
            print("right far")
        print(ball.vector)

