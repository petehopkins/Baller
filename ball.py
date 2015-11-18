import pygame
from engine import Engine
from eventManager import Events
from Bricks import *

class Ball(Engine.GUI.Widget):
    def __init__(self, eventManager, stage):
        super().__init__(eventManager, None)

        self.stage = stage
        self.eventManager = eventManager
        #making rectangular
        self.width = 25
        self.height = 25
        self.xDirection = 1
        self.yDirection = 1
        self.dx = 150
        self.dy = 150
        self.speed = 5
        self.color = (255,0,0)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 150

    def checkForCollision():
        #check for boundary
        #check for paddle
        #check for bricks
            #if brick:
                #brick.collide()

        #if collision:
            #self.bounce()
    def move(self):
        self.dx = self.xDirection * self.speed
        self.dy = self.yDirection * self.speed
        
        self.rect.x += self.dx
        self.rect.y += self.dy

        #check for boundary collisions

        self.checkForCollisions()

    #if boundaries are hit    
    #def bounce():
        if self.rect.x > (800 - self.width) or self.rect.x < 0:
            self.xDirection *= -1
        
        if self.rect.y < 0 or self.rect.y > (600 - self.height):
            self.yDirection *= -1
           
    #if paddle/brick is hit        
##    def collision():
##        if paddle:
##            if hit = True
##            self.dy *= -1
##            
        spridgets = self.stage.getWidgets()
        if self in spridgets:
            spridgets.remove(self)
        
        collides = self.groupcollide(self, spridgets)
        for c in collides:
            
                    
        for brick in bricks
            if self.isInPlay = True
                #refer back to brick side/height 
                #if (leftBorder(self.height in brick?) or rightBorder hit) = True
                self.dx *= -1
                self.collide() #call collide function or collision event
                #refer back to brick top/bottom/width
                #if (self.width?) = True
                self.dy *= -1
                self.collide() #call collide function or collision event?
                #add score?
            if self.isInPlay = False
                pass

    def addListeners(self,):
        event = Events.TickEvent()
        self.eventManager.addListener(event, self)
            
    def notify(self, event):
        if isinstance(event, Events.TickEvent):
            #reposition ball
            self.move()

    self.eventManager.post(eventName) #Collide?

    #for draw - define surface (rectangle) image property self.image self.rect


