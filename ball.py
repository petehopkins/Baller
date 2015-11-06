class Ball():
    def __init__(self, eventManager):
        self.eventManager
        self.diameter = 25
        self.x = 150
        self.y = 150
        self.dx = 2
        self.dy = 2
        self.speed = 5

    def move(self):
        self.dx = self.x + self.speed
        self.dy = self.y + self.speed
        self.x = self.dx
        self.y = self.dy
        
    def bounce():
        if self.x > 800 - self.diameter or self.x < 0:
            self.dx * -1
        if self.y < 0:
            self.dy * -1
        #lose life
        if self.y > (paddle location)
            self.lives -= 1
            
        for paddle in paddle
            self.dx * -1
            self.dy * -1
            
    def collision():
        for brick in brick
            self.dx * -1
            self.dy * -1
            #add score?
            #link to destroy brick

    pygame.draw.circle(screen, black, [x, y], diameter)
