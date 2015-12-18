import pygame, math
from engine import Engine
from eventManager import Events
from brick import *
from paddle import *

class Ball(Engine.GUI.Widget):
    def __init__(self, level):
        super().__init__()

        self.level = level
        self.eventManager = EventManager()

        self.radius = self.options.ballRadius
        self.vector = self.options.ballVectorInitial
        self.gyreDirection = self.options.ballGyreDirection
        self.speed = self.options.ballSpeed
        self.color = self.options.ballColor

        self.pauseForTicks = 0
        self.repositionWhilePausedAfterTicks = 0

        # puting these here as these may be needed
        self.width = self.options.ballRadius * 2
        self.height = self.width

        self.x = self.options.ballInitialPosition[0]
        self.y = self.options.ballInitialPosition[1]

        # making a square ball for now
        self.image = pygame.Surface((self.options.ballRadius * 2, self.options.ballRadius * 2))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x =  - self.radius
        self.rect.y = self.options.ballInitialPosition[1] - self.radius

        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

        self.soundBallBounce = pygame.mixer.Sound(self.options.soundBallBounce)
        self.soundVolumeBallBounce = self.options.soundVolumeBallBounce

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
            if self.pauseForTicks > 0:
                self.pauseForTicks -= 1
                if self.pauseForTicks == self.repositionWhilePausedAfterTicks:
                    self.move(0)
            else:
                # reposition ball and check for collisions
                self.move(self.speed)
                self.checkForCollisions()

    def handleOverlap(self, xOverlap, yOverlap, isPaddle):
        # figure out which overlap is further into the brick with an edge case of equally
        overlap = 0
        normalAxis = 180 # default to top/bottom collisions

        if not isPaddle:
            # sanity check for overlap as it should never be greater than the speed of the ball
            # this is invalid for paddle collisions as the paddle moves independently of the ball at it's own rate
            if xOverlap > self.speed:
                xOverlap = 0 # ignore overlap

            if yOverlap > self.speed:
                yOverlap = 0 # ignore overlap
        else:
            xOverlap = 0 # it's the paddle, so we only care about the yOverlap if it exists

        if yOverlap > xOverlap: # collision likely came from top/bottom
            overlap = yOverlap

        elif xOverlap > yOverlap: # collsions likely came from left/right
            overlap = xOverlap
            normalAxis = 360 # change normal axis to vertical

        else: # edge case of equal, so which one doesn't matter
            overlap = xOverlap

        self.move(overlap * -1, assureMovement = True) # move ball back along vector to the last edge passed

        return normalAxis

    def bounce(self, bounces, normalAxis, collidableObjects, isPaddle = False, spin = None):
        # recheck position and move ball outside of (or to the edge of) the collision zone to prevent multiple bounces on the same object per hit
        # otherwise vectors can get messed up as the ball bounces off the object going into it and then again (and again and again, etc.)
        # while exiting the collision zone

        normals = []

        # play sound
        if self.options.soundPlayBallBounce:
            self.soundBallBounce.play()

        if self.leftEdge() < self.options.levelZoneGamePlay["x"]:
            self.x = self.options.levelZoneGamePlay["x"] # left edge is past window, clamp to left edge of window

        if self.rightEdge() > self.options.levelZoneGamePlay["x"] + self.options.levelZoneGamePlay["width"]:
            self.x = (self.options.levelZoneGamePlay["x"] + self.options.levelZoneGamePlay["width"]) - self.rect.width # right edge is past window, clamp to right edge of window

        if self.topEdge() < self.options.levelZoneGamePlay["y"]:
            self.y = self.options.levelZoneGamePlay["y"] # top edge is past window, clamp to top edge of window

        if self.bottomEdge() > self.options.levelZoneGamePlay["y"] + self.options.levelZoneGamePlay["height"]:
            self.y = (self.options.levelZoneGamePlay["y"] + self.options.levelZoneGamePlay["height"]) - self.rect.height # bottom edge is past window, clamp to bottom edge of window

        # now do the same for the bricks and the paddle (both of which are collidable objects)
        for co in collidableObjects:
            if co.rect.collidepoint(self.rect.topleft):
                # topleft is within the collidable object
                xOverlap = abs(co.rightEdge() - self.leftEdge())
                yOverlap = abs(co.bottomEdge() - self.topEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap, isPaddle))

            if co.rect.collidepoint(self.rect.topright):
                # topright is within the collidable object
                xOverlap = abs(co.leftEdge() - self.rightEdge())
                yOverlap = abs(co.bottomEdge() - self.topEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap, isPaddle))

            if co.rect.collidepoint(self.rect.bottomright):
                # bottomright is within the collidable object
                xOverlap = abs(co.leftEdge() - self.rightEdge())
                yOverlap = abs(co.topEdge() - self.bottomEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap, isPaddle))

            if co.rect.collidepoint(self.rect.bottomleft):
                # bottomleft is within the collidable object
                xOverlap = abs(co.rightEdge() - self.leftEdge())
                yOverlap = abs(co.topEdge() - self.bottomEdge())
                normals.append(self.handleOverlap(xOverlap, yOverlap, isPaddle))

            co.collide() # may as well notify the object of a collision here so we don't have to loop through twice

        # finally, change vector, angle of incidence = angle of reflection, may need to change rotation (counter/clockwise) on paddle hit or ball spin
        if len(normals) > 0: # multiple bounces passed in, bounce once prioritizing vertical travel
            normalAxis = max(normals)

        # angle of incidence... yadda yadda...
        reflectionVector = (normalAxis - self.vector)

        # change gyre direction if needed
        reflectionVector -= self.gyreDirection #(0 or 180)

        # keep the angles sane (i.e., between 0 and 359)
        reflectionVector %= 360

        # update to new vector
        self.vector = reflectionVector

    def checkForCollisions(self):
        # intialize variables here to count brick/paddle bounces as python does not support variable hoisting
        bounces = 0
        collidableObjects = pygame.sprite.Group()

        # check for boundary collisions
        if self.topEdge() <= self.options.levelZoneGamePlay["y"]:
            self.bounce(1, 180, collidableObjects)

        if self.rightEdge() >= self.options.levelZoneGamePlay["x"] + self.options.levelZoneGamePlay["width"]:
            self.bounce(1, 360, collidableObjects)

        if self.bottomEdge() >= self.options.levelZoneGamePlay["y"] + self.options.levelZoneGamePlay["height"]: # bottom was hit, lose a ball
            # reset to intial position and vector
            self.x = self.options.ballInitialPosition[0]
            self.y = self.options.ballInitialPosition[1]
            self.vector = self.options.ballVectorInitial
            self.pauseForTicks = 60

            event = Events.StatUpdateEvent(stat = Engine.Stats.BALLS_REMAINING, value = -1)
            self.eventManager.post(event)

        if self.leftEdge() <= self.options.levelZoneGamePlay["x"]:
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
            for paddle in collidableObjects: # should only be one, but this allows for multiple paddles later if we want to do that sort of thing
                self.bottomEdge(paddle.topEdge()) # always set the bottom edge of the ball to the top edge of the paddle
                paddle.redirect(self) # set the new vector
                if self.options.soundPlayBallBounce:
                    self.soundBallBounce.play() # and play sound

    def move(self, distance, assureMovement = None):
        if assureMovement == None:
            assureMovement = self.options.difficulty == 0

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

        # this will keep track of x,y seperately and account for fractional pixel movement
        self.x += dx
        self.y += dy

        # assigning a fractional value to a pygame.Rect will apparently truncate the fraction, hence the need for separate storage above
        self.rect.x = self.x
        self.rect.y = self.y
