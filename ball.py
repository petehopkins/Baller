import pygame, math
from engine import Engine
from eventManager import Events
from bricks import *
from paddle import *

class Ball(Engine.GUI.Widget):
    def __init__(self, eventManager, level):
        super().__init__(eventManager, None)

        self.level = level
        self.eventManager = eventManager

        self.radius = self.options.ballRadius
        self.vector = self.options.ballVectorInitial
        self.gyreDirection = self.options.ballGyreDirection
        self.speed = self.options.ballSpeed
        self.color = self.options.ballColor

        # puting these here as these may be needed
        self.width = self.options.ballRadius * 2
        self.height = self.width

        #making a square ball for now
        self.image = pygame.Surface((self.options.ballRadius * 2, self.options.ballRadius * 2))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = self.options.ballInitialPosition[0] - self.radius
        self.rect.y = self.options.ballInitialPosition[1] - self.radius

        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

    def update(self):
        x = self.rect.x
        y = self.rect.y

        self.width = self.options.ballRadius * 2
        self.height = self.width

        self.image = pygame.Surface((self.options.ballRadius * 2, self.options.ballRadius * 2))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def addListeners(self,):
        event = Events.TickEvent()
        self.eventManager.addListener(event, self)

    def notify(self, event):
        if isinstance(event, Events.TickEvent):
            # reposition ball and check for collisions
            self.move(self.speed)
            self.checkForCollisions()

    def handleOverlap(self, xOverlap, yOverlap):
        #figure out which overlap is further into the brick with an edge case of equally
        overlap = 0
        normalAxis = 180 # default to top/bottom collisions

        # sanity check for overlap as it should never be greater than the speed of the ball
        if xOverlap > self.speed:
            xOverlap = 0 # ignore overlap

        if yOverlap > self.speed:
            yOverlap =0 # ignore overlap

        if yOverlap > xOverlap: # collision likely came from top/bottom
            overlap = yOverlap

        elif xOverlap > yOverlap: # collsions likely came from left.right
            overlap = xOverlap
            normalAxis = 360

        else: # edge case of equal, so which one doesn't matter
            overlap = xOverlap

        self.move(overlap * -1, assureMovement = True) # move ball back along vector to the last edge passed

        return normalAxis

    def bounce(self, bounces, normalAxis, bricks, spin = None):
        # recheck position and move ball outside of (or to the edge of) the collision zone to prevent multiple bounces on the same object per hit
        # otherwise vectors can get messed up as the ball bounces off the object going into it and then again (and again and again, etc.)
        # while exiting the collision zone

        normals = []

        if self.leftEdge() < 0:
            self.rect.x = 0 # left edge is past window, clamp to left edge of window

        if self.rightEdge() > self.options.windowWidth:
            self.rect.x = self.options.windowWidth - self.rect.width # right edge is past window, clamp to right edge of window

        if self.topEdge() < 0:
            self.rect.y = 0 # top edge is past window, clamp to top edge of window

        if self.bottomEdge() > self.options.windowHeight:
             self.rect.y = self.options.windowHeight - self.rect.height # bottom edge is past window, clamp to bottom edge of window

        # now do the same for the bricks and the paddle (which would be in bricks as it is a collidable object)
        for brick in bricks:
            if brick.rect.collidepoint(self.rect.topleft):
                # topleft is within the brick
                xOverlap = abs(brick.rightEdge() - self.leftEdge())
                yOverlap = abs(brick.bottomEdge() - self.topEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap))

            if brick.rect.collidepoint(self.rect.topright):
                # topright is within the brick
                xOverlap = abs(brick.leftEdge() - self.rightEdge())
                yOverlap = abs(brick.bottomEdge() - self.topEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap))

            if brick.rect.collidepoint(self.rect.bottomright):
                # bottomright is within the brick
                xOverlap = abs(brick.leftEdge() - self.rightEdge())
                yOverlap = abs(brick.topEdge() - self.bottomEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap))

            if brick.rect.collidepoint(self.rect.bottomleft):
                # bottomleft is within the brick
                xOverlap = abs(brick.rightEdge() - self.leftEdge())
                yOverlap = abs(brick.topEdge() - self.bottomEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap))

            brick.collide() # may as well notify the object of a collision here so we don't have to loop through twice

        #finally, change vector, angle of incidence = angle of reflection, may need to change rotation (counter/clockwise) on paddle hit or ball spin
        if len(normals) > 0: # multiple bounces passed in, bounce once prioritizing vertical travel
            normalAxis = max(normals)

        #angle of incidence... yadda yadda...
        reflectionVector = (normalAxis - self.vector)

        #change gyre direction if needed
        reflectionVector -= self.gyreDirection #(0 or 180)

        #keep the angles sane (i.e., between 0 and 359)
        reflectionVector %= 360

        #update to new vector
        self.vector = reflectionVector

    def checkForCollisions(self):
        #start counting bounces
        bounces = 0
        collidableObjects = pygame.sprite.Group()

        #check for boundary collisions
        if self.topEdge() <= 0:
            self.bounce(1, 180, collidableObjects)

        if self.rightEdge() >= self.options.windowWidth:
            self.bounce(1, 360, collidableObjects)

        if self.bottomEdge() >= self.options.windowHeight: #once algorithm is abstracted / finalized, lose a ball instead
            self.bounce(1, 180, collidableObjects)

        if self.leftEdge() <= 0:
            self.bounce(1, 360, collidableObjects)

        #check for bricks
        collidableObjects.add(self.level.getWidgets(Brick))
        collidableObjects = pygame.sprite.groupcollide(collidableObjects, self.group, False, False) #redfine collidableObjects to include only those Bricks that were collided with
        bounces += len(collidableObjects)

        if bounces > 0:
            self.bounce(bounces, 180, collidableObjects)

        # redfine as a new group to remove all sprites from this group and redefine it as a actual group as groupcollide returns a dict
        collidableObjects = pygame.sprite.Group()

        # reset bounces
        bounces = 0

        # check for paddle
        collidableObjects.add(self.level.getWidgets(Paddle))
        collidableObjects = pygame.sprite.groupcollide(collidableObjects, self.group, False, False) #redfine collidableObjects to include only those Paddles that were collided with
        bounces += len(collidableObjects)

        if bounces > 0:
            self.bounce(bounces, 180, collidableObjects) # pass in to handle basic collision and overlaps
            for paddle in collidableObjects:
                paddle.redirect(self)

    def move(self, distance, assureMovement = False):
        vector = math.radians(self.vector)

        dx = distance * math.cos(vector)
        dy = distance * math.sin(vector)

        if assureMovement:
            if 0 < abs(dx) < 1:
                sign = dx / abs(dx)
                dx = 1 * sign

            if 0 < abs(dy) < 1:
                sign = dy / abs(dy)
                dy = 1 * sign

        self.rect.x += dx
        self.rect.y += dy
