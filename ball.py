import pygame
from engine import Engine
from eventManager import Events

class Ball(Engine.GUI.Widget):
    def __init__(self, eventManager, container = None):
        super().__init__(eventManager, container)
        
        self.eventManager
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

    def move(self):
        self.dx = self.xDirection * self.speed
        self.dy = self.yDirection * self.speed
        
        self.rect.x += self.dx
        self.rect.y += self.dy

    #if boundaries are hit    
    #def bounce():
        if self.rect.x > (800 - self.width) or self.rect.x < 0:
            self.xDirection *= -1
        
        if self.rect.y < 0 or self.rect.y > (600 - self.height):
            self.yDirection *= -1

        #lose life
##        if self.y > (paddle location)
##            return self.lose_life
            
    #if paddle/brick is hit        
##    def collision():
##        if paddle:
##            if hit = True
##            self.dy *= -1
##            
##        for brick in bricks
##            if (hit side) = True
##            self.dx *= -1
##            if (hit top/bottom) = True
##            self.dy *= -1
            #add score?
            #link to destroy brick

    def addListeners(self,):
        event = Events.TickEvent()
        self.eventManager.addListener(event, self)
            
    def notify(self, event):
        if isinstance(event, Events.TickEvent):
            #reposition ball
            self.move()
    #call self.eventManager.post(eventType) to throw an event

    #for draw - define surface (rectangle) image property self.image self.rect
    


