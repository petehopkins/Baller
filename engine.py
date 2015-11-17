import pygame
from eventManager import *

class Engine():
    class Colors():
        WHITE = (255, 255, 255)
        LIGHT_GREY = (192, 192, 192)
        LAVENDER = (210, 166, 255)
        GREY = (128, 128, 128)
        BLACK = (0, 0, 0)

    class Options():
        def __init__(self):
            self.name = "Baller" #"Defeat the oppressive war machine of the evil Quadratic invaders!"
            self.backstory = '''
    From the depths of Outer Space comes the vile army of the extraterrestrial race known only as the Quadrilaterians.

    Freshly resupplied from the war-torn planet of Buttercracker IV, the Quadrilaterians are hellbent on conquest and will not stop until they have crushed our military, overthrown our government, quelled all rebellions, completely subjugated our planet and have captured all of our cheese and the means of production for such.

    It is up to you, our Champion, to defeat the oppressive war machine of the evil Quadratic invaders!

    Your planet needs you!
            '''
            self.windowWidth = 800
            self.windowHeight = 600
            self.tickSpeed = 60
            self.availableDifficulties = [("Easy", 0), ("Normal", 1), ("Hard", 2), ("Brutal", 3)]

    class GUI():
        def __init__(self):
            pass

        class Widget(pygame.sprite.Sprite):
            def __init__(self, eventManager, container = None):
                pygame.sprite.Sprite.__init__(self)

                self.eventManager = eventManager
                self.container = container
                self.focused = False
                self.dirty = True
                self.Options = self.eventManager.game.Options #alias

            def setPosition(self, x = None, y = None):
                if x or y:
                    self.dirty = True

                    if x:
                        self.rect.x = x

                    if y:
                        self.rect.y = y

                    self.update()

            def centerOn(self, surf):
                surfRect = surf.get_rect()
                onX = surfRect.x + (surfRect.width / 2) - (self.rect.width / 2)
                onY = surfRect.y + (surfRect.height / 2) - (self.rect.height / 2)
                self.setPosition(onX, onY)

            def setFocus(self, val):
                self.focused = val
                self.dirty = True

            def kill(self):
                self.container = None
                del self.container
                pygame.sprite.Sprite.kill(self)

            def removeListeners(self):
                listeners = self.eventManager.getListeners()
                if self in listeners.keys():
                    for event in listeners[self]:
                        e = Events.getEvent(event)
                        self.eventManager.removeListener(e, self)

            def notify(self, event):
                print("Abstract Class not implemented. Triggering event:", event.name)

    class Layer():
        def __init__(self):
            self.widgets = pygame.sprite.Group()
            self.sprites = pygame.sprite.Group()
            self.activate = self.addListeners
            self.deactivate = self.removeListeners

        def addWidget(self, widget):
            self.widgets.add(widget)#append

        def addWidgetListeners(self):
            for widget in self.widgets:
                widget.addListeners()

        def removeWidgetListeners(self):
            for widget in self.widgets:
                widget.removeListeners()

        def removeWidget(self, widget):
            if widget in self.widgets:
                widget.removeListeners()
                self.widgets.remove(widget)

        def addSprite(self, sprite):
            self.sprites.add(sprite)

        def addSpriteListeners(self):
            for sprite in self.sprites:
                sprite.addListeners()

        def removeSpriteListeners(self):
            for sprite in self.sprites:
                sprite.removeListeners()

        def removeSprite(self, sprite):
            self.sprites.remove(sprite)

        def getWidgets(self):
            return self.widgets

        def getSprites(self):
            return self.sprites

        def redrawWidgets(self, window):
##            for widget in self.widgets:
##                widget.update()
##                window.blit(widget.widget, widget.rect) #widget.widget.get_rect(x = widget.rect.x, y = widget.rect.y)
            self.widgets.update()
            self.widgets.draw(window)

        def redrawSprites(self, window):
            self.sprites.update()
            self.sprites.draw(window)

        def addListeners(self):
            self.addWidgetListeners()
            self.addSpriteListeners()

        def removeListeners(self):
            self.removeWidgetListeners()
            self.removeSpriteListeners()

    class Ticker():
        def __init__(self, eventManager, engine):
            self.eventManager = eventManager
            self.engine = engine

            event = Events.TickEvent()
            self.eventManager.addListener(event, self)

            event = Events.QuitEvent()
            self.eventManager.addListener(event, self)

        def notify(self, event):
            if isinstance(event, Events.QuitEvent):
                self.eventManager.running = False

            if isinstance(event, Events.TickEvent):
                self.engine.clock.tick(self.engine.tickSpeed)
                self.engine.redrawWindow() #redraw sprites
                pygame.display.update() #redraw screen

    def redrawWindow(self):
        screen = self.screens[self.activeScreen]
        self.window.fill(self.windowFillColor)
        screen.redrawWidgets(self.window)
        screen.redrawSprites(self.window)

    def end(self):
        self.eventManager.running = False
        pygame.display.quit()
        pygame.quit()

    def __init__(self):
        #Initial module setup
        #make an instance of GUI and Options classes so the interpreter won't kvetch
        self.GUI = Engine.GUI()
        self.Options = Engine.Options()
        #self.GUI.Widget = Engine.GUI.Widget()

        self.name = "Baller" #"Defeat the oppressive war machine of the evil Quadratic invaders!"
        self.backstory = '''
From the depths of Outer Space comes the vile army of the extraterrestrial race known only as the Quadrilaterians.

Freshly resupplied from the war-torn planet of Buttercracker IV, the Quadrilaterians are hellbent on conquest and will not stop until they have crushed our military, overthrown our government, quelled all rebellions, completely subjugated our planet and have captured all of our cheese and the means of production for such.

It is up to you, our Champion, to defeat the oppressive war machine of the evil Quadratic invaders!

Your planet needs you!
        '''
        self.sprites = pygame.sprite.Group()
        self.windowWidth = self.Options.windowWidth
        self.windowHeight = self.Options.windowHeight
        self.windowSize = (self.windowWidth, self.windowHeight)
        self.windowFillColor = self.Colors.WHITE
        self.tickSpeed = self.Options.tickSpeed
        self.screens = {}
        self.activeScreen = ""

        #Create a window and start a clock
        pygame.init()
        self.window = pygame.display.set_mode(self.windowSize)
        pygame.display.set_caption(self.name)
        self.clock = pygame.time.Clock()
