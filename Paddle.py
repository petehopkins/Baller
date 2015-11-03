import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, window):
        pygame.sprite.Sprite.__init__(self)
        self.limitLeft = 20
        self.limitRight = window.get_width() - self.limitLeft
        self.width = 75
        self.height = 25
        self.color = (0, 0 , 96)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

    def getPosition(self):
        return (self.rect.x, self.rect.y)
    
    def move(self, x):
        self.rect.x = x

    def drawPaddle(self, window):
        window.blit(self)

