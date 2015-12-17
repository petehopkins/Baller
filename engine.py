import pygame
from eventManager import *

class Engine():
    class Colors():
        WHITE = pygame.Color(255, 255, 255, 255)
        WHITE_TRANSLUCENT = pygame.Color(255, 255, 255, 64)
        LIGHT_GREY = pygame.Color(192, 192, 192, 255)
        DARK_BLUE = pygame.Color(0, 0, 96, 255)
        BRIGHT_RED = pygame.Color(255, 0, 0, 255)
        LAVENDER = pygame.Color(210, 166, 255, 255)
        GREY = pygame.Color(128, 128, 128, 255)
        BLACK = pygame.Color(0, 0, 0, 255)

    class Stats():
        BALLS_REMAINING = "Balls Remaining"
        SCORE = "Score"

    class Options():
        def __init__(self):
            self.name = "Baller" #"Defeat the oppressive war machine of the evil Quadratic invaders!"
            self.backstory = '''
    From the depths of Outer Space comes the vile army of the extraterrestrial race known only as the Quadrilaterians.

    Freshly resupplied from the war-torn planet of Buttercracker IV, the Quadrilaterians are hellbent on conquest and will not stop until they have crushed our military, overthrown our government, quelled all rebellions, completely subjugated our planet and have captured all of our cheese and the means of production for such.

    It is up to you, our Champion, to defeat the oppressive war machine of the evil Quadratic invaders!

    Your planet needs you!
            '''

            # clock
            self.tickSpeed = 60

            # sound properties
            self.soundNumberOfChannels = 8
            self.soundAmbientChannelNumber = 0
            self.soundPlayAmbient = True
            self.soundPlayBrickHit = True
            self.soundPlayBrickDestroyed = True
            self.soundPlayBallBounce = True
            self.soundVolumeAmbient = 1
            self.soundVolumeBrickHit = 1
            self.soundVolumeBrickDestroyed = 1
            self.soundVolumeBallBounce = 1

            # window properties
            self.windowWidth = 800
            self.windowHeight = 600
            self.windowSize = (self.windowWidth, self.windowHeight)
            self.windowFillColor = Engine.Colors.WHITE

            # Game Stats
            self.ballsRemaining = 3
            self.score = 0

            # difficulty
            self.availableDifficulties = [("Easy", 0), ("Normal", 1), ("Hard", 2), ("Brutal", 3)]
            self.defaultDifficultyValue = 1
            self.difficultyValue = self.defaultDifficultyValue
            self.difficulty = {
                0: {
                    "paddleWidth": 150,
                    "brickHitsRemaining": 0,
                    "ballRadius": 25,
                    "ballSpeed": 2,
                    "backgroundImage": "resources/images/easy.png"
                    },
                1: {
                    "paddleWidth": 100,
                    "brickHitsRemaining": 1,
                    "ballRadius": 12.5,
                    "ballSpeed": 4,
                    "backgroundImage": "resources/images/normal.png"
                },
                2: {
                    "paddleWidth": 50,
                    "brickHitsRemaining": 2,
                    "ballRadius": 6.75,
                    "ballSpeed": 8,
                    "backgroundImage": "resources/images/hard.png"
                },
                3: {
                    "paddleWidth": 10,
                    "brickHitsRemaining": 3,
                    "ballRadius": 3.375,
                    "ballSpeed": 16,
                    "backgroundImage": "resources/images/brutal.png"
                }}

            # level properties
            self.__infoZoneHeight = 75
            self.__paddleAreaHeight = 200
            self.levelZoneInfo = Engine.GUI.RectWithEdges(pygame.Rect(0, self.windowHeight - self.__infoZoneHeight, self.windowWidth, self.__infoZoneHeight)) #{"x": 0, "y": self.windowHeight - self.__infoZoneHeight, "width": self.windowWidth, "height": self.__infoZoneHeight}
            self.levelZoneGamePlay = {"x": 0, "y": 0, "width": self.windowWidth, "height": self.windowHeight - self.levelZoneInfo.rect.height}
            self.levelZonePaddleArea = {"x": 0, "y": self.levelZoneGamePlay["height"] - self.__paddleAreaHeight, "width": self.windowWidth, "height": self.__paddleAreaHeight}
            self.levelBackgroundImage = self.difficulty[self.difficultyValue]["backgroundImage"]
            self.levelSoundAmbient = "resources/sounds/fantomenk_560407_a_tiny_spaceships_final_mission.ogg"
            self.levelCompleteSoundAmbient = "resources/sounds/mike_koenig_215222688_10_second_applause.ogg"

            # Main Layer properties
            self.backgroundImage = "resources/images/backdrop.png"
            self.soundAmbient = "resources/sounds/fantomenk_532501_cold_war_game_theme_song.ogg"

            # Mouse / Keyboard(?) sensitivity
            sensitivities = []
            for s in range(10, 0, -1):
                text = "Every {0} ticks"
                sensitivities.append((text.format(s), s))

            sensitivities[0] = ("MIN (not recommended)", len(sensitivities))
            sensitivities[len(sensitivities) - 1] = ("MAX (recommended)", 1)

            self.availableSensitivities = sensitivities
            self.defaultSensitivityValue = 1
            self.sensitivityValue = self.defaultSensitivityValue

            # brick properties
            self.brickWidthHeightRatio = {"width": 2, "height": 1} # only ever used in this class to determine width and height
            self.brickSize = 25 # only ever used in this class to determine width and height

            self.brickWidth = self.brickSize * self.brickWidthHeightRatio["width"]
            self.brickHeight = self.brickSize * self.brickWidthHeightRatio["height"]
            self.brickBorderWidth = 2
            self.brickHitsRemaining = self.difficulty[self.difficultyValue]["brickHitsRemaining"]
            self.soundBrickHit = "resources/sounds/vladimir_719669812_neck_snap.ogg"
            self.soundBrickDestroyed = "resources/sounds/mike_koenig_1123041125_crumbling.ogg"

            # ball properties
            self.ballSpeed = self.difficulty[self.difficultyValue]["ballSpeed"]
            self.ballRadius = self.difficulty[self.difficultyValue]["ballRadius"]
            self.ballVectorInitial = -45
            self.ballGyreDirection = 180
            self.ballColor = Engine.Colors.BRIGHT_RED
            self.ballInitialPosition = ((self.levelZonePaddleArea["x"] + self.levelZonePaddleArea["width"]) / 2, self.levelZonePaddleArea["y"] + (self.ballRadius * 3))
            self.soundBallBounce = "resources/sounds/mark_diangelo_79054334_blop.ogg"

            # paddle properties
            self.paddleWidth = self.difficulty[self.difficultyValue]["paddleWidth"]
            self.paddleHeight = 25
            self.paddleLeftBound = self.ballRadius
            self.paddleRightBound = self.paddleLeftBound
            self.paddleColor = Engine.Colors.DARK_BLUE
            self.paddleX = ((self.levelZonePaddleArea["x"] + self.levelZonePaddleArea["width"]) / 2) - (self.paddleWidth / 2)
            self.paddleY = (self.levelZonePaddleArea["y"] + self.levelZonePaddleArea["height"]) - (self.paddleHeight + (self.ballRadius / 2))

            # brick wall properties
            self.brickWallMinimumOffset = (self.ballRadius * 2)
            self.brickWallWidth = self.levelZoneGamePlay["width"] - (self.brickWallMinimumOffset * 2)
            self.brickWallHeight = self.levelZoneGamePlay["height"] - self.__paddleAreaHeight - self.brickWallMinimumOffset
            self.brickWallMortarGap = 2

            # Base GUI widget properties
            self.widgetFont = None
            self.widgetPadding = 40
            self.widgetFontSize = 56
            self.widgetCollisionZoneRatioCenter = 1 / 10
            self.widgetCollisionZoneRatioNear = 2 / 3

            # Label GUI Widget properties
            self.labelWidgetTextColor = Engine.Colors.BLACK
            self.labelWidgetBackgroundColor = Engine.Colors.WHITE

            # StatTracker GUI Widget Properties
            self.statTrackerTextFontSize = 24
            self.statTrackerTextPadding = 8
            self.statTrackerValueTextSpacing = 4

            # Slider GUI widget
            self.sliderFontSize = 24
            self.sliderWidth = 200
            self.sliderHeight = 72
            self.sliderBarHeight = 10
            self.sliderBarOffsetX = 0
            self.sliderBarOffsetY = 15
            self.sliderSlideWidth = 10
            self.sliderSlideHeight = 40
            self.sliderTextOffsetY = 8
            self.sliderDragPaddingX = 100
            self.sliderWidgetTextColor = Engine.Colors.BLACK
            self.sliderWidgetFillColor = Engine.Colors.LIGHT_GREY
            self.sliderWidgetBackgroundColor =  Engine.Colors.WHITE

    class GUI():
        def __init__(self):
            pass

        class RectWithEdges():
            def __init__(self, rect):
                self.rect = rect

            def leftEdge(self, x = None):
                if x != None:
                    self.rect.x = x # set x

                return self.rect.x

            def rightEdge(self, x = None):
                if x != None:
                    self.rect.x = (x - self.rect.width) # set x

                return self.rect.x + self.rect.width

            def topEdge(self, y = None):
                if y != None:
                    self.rect.y = y # set y

                return self.rect.y

            def bottomEdge(self, y = None):
                if y != None:
                    self.rect.y = (y - self.rect.height) # set y

                return self.rect.y + self.rect.height

        class Widget(pygame.sprite.Sprite, RectWithEdges):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)

                self.eventManager = EventManager()
                self.isCollidable = False
                self.focused = False
                self.dirty = True
                self.options = self.eventManager.game.options #alias

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

            def get_rect(self):
                return self.rect

            def centerZone(self): # allow for a wider zone, if desired
                rect = self.image.get_rect() # get a new rect based on the image
                rect.y = self.rect.y

                rect.width = self.rect.width * self.options.widgetCollisionZoneRatioCenter

                if self.width % 2 == 0: #even width
                    rect.x = self.rect.x + ((self.rect.width / 2) - (rect.width / 2))

                else: # odd width
                    rect.x = self.rect.x + ((self.rect.width + 1) / 2) - (rect.width / 2)

                return rect

            def leftNearZone(self):
                centerZone = self.centerZone() # get the center zone
                rect = self.image.get_rect() # get a new rect based on the image

                rect.y = self.rect.y

                rect.width = (centerZone.x - self.rect.x) * self.options.widgetCollisionZoneRatioNear
                rect.x = (centerZone.x - rect.width)

                return rect

            def leftFarZone(self):
                leftNearZone = self.leftNearZone() # get the leftNear zone
                rect = self.image.get_rect() # get a new rect based on the image

                rect.x = self.rect.x
                rect.y = self.rect.y

                rect.width = (leftNearZone.x - rect.x)

                return rect

            def rightNearZone(self):
                centerZone = self.centerZone() # get the center zone
                rect = self.image.get_rect() # get a new rect based on the image

                rect.x = centerZone.x + centerZone.width
                rect.y = self.rect.y

                rect.width = (self.rightEdge() - (centerZone.x + centerZone.width)) * self.options.widgetCollisionZoneRatioNear

                return rect

            def rightFarZone(self):
                rightNearZone = self.rightNearZone() # get the rightNear zone
                rect = self.image.get_rect() # get a new rect based on the image

                rect.y = self.rect.y
                rect.x = rightNearZone.x + rightNearZone.width
                rect.width = self.rightEdge() - rect.x

                return rect

            def setFocus(self, val):
                self.focused = val
                self.dirty = True

            def kill(self):
                self.eventManager.removeListeners(self)
                pygame.sprite.Sprite.kill(self)

            def addListeners(self):
                pass #print("Abstract Method: addListeners; not implemented.")

            def notify(self, event):
                print("Abstract Method: notify; not implemented. Triggering event:", event.name)

    class Layer():
        def __init__(self, fillColor = None, mouseVisible = True):
            self.eventManager = EventManager()

            self.activate = self.addListeners
            self.deactivate = self.removeListeners

            self.widgets = pygame.sprite.Group()
            self.widgetValues = {}

            self.mouseVisible = mouseVisible

            self.background = pygame.Surface(self.eventManager.game.options.windowSize)
            self.setFillColor(fillColor)

            self.soundAmbient = None
            self.soundAmbientStartAt = 0
            self.soundVolumeAmbient = self.eventManager.game.options.soundVolumeAmbient

        def setFillColor(self, fillColor):
            self.fillColor = fillColor if fillColor != None else self.eventManager.game.Colors.WHITE

            self.background.fill(self.fillColor)
            self.background.set_alpha(self.fillColor.a)

        def setBackgroundImage(self, image):
            self.background = pygame.image.load(image).convert()

        def addWidget(self, widget):
            self.widgets.add(widget)

        def addListeners(self):
            for widget in self.widgets:
                widget.addListeners()

        def removeListeners(self):
            for widget in self.widgets:
                #if hasattr(widget, "text"):
                    #print("Removing listeners for", widget.text)
                self.eventManager.removeListeners(widget)

        def removeWidget(self, widget):
            if widget in self.widgets:
                self.eventManager.removeListeners(widget)
                self.widgets.remove(widget)

        def getWidgets(self, ofType = None):
            widgets = self.widgets

            if ofType != None:
                widgets = [widget for widget in self.widgets if type(widget) == ofType]

            return widgets

        def redraw(self, window):
            window.blit(self.background, self.background.get_rect())
            self.widgets.update()
            self.widgets.draw(window)

    class Level(Layer):
        def __init__(self, fillColor = None, mouseVisible = True):
            super().__init__(fillColor, mouseVisible)

            self.ballsRemaining = self.eventManager.game.options.ballsRemaining
            self.score = 0

        def addListeners(self):
            super().addListeners()

            event = Events.StatUpdateEvent()
            self.eventManager.addListener(event, self)

            event = Events.LowerVolumeEvent()
            self.eventManager.addListener(event, self)

        def removeListeners(self):
            super().removeListeners()

            self.eventManager.removeListeners(self)

        def notify(self, event):
            from brick import Brick # delayed import to prevent circular loading

            if isinstance(event, Events.LowerVolumeEvent):
                pygame.mixer.music.set_volume(0.2)

            if isinstance(event, Events.StatUpdateEvent):
                if event.stat == Engine.Stats.BALLS_REMAINING:
                    self.ballsRemaining += event.value

                    if self.ballsRemaining < 0:
                        event = Events.GameOverEvent()
                        self.eventManager.post(event)

                if event.stat == Engine.Stats.SCORE:
                    bricksRemaining = self.getWidgets(Brick)
                    if len(bricksRemaining) == 0:
                        event = Events.LevelCompleteEvent()
                        self.eventManager.post(event)

    class Ticker():
        def __init__(self, engine):
            self.eventManager = EventManager()
            self.engine = self.eventManager.game
            self.counter = 0
            self.countdown = False

            event = Events.TickEvent()
            self.eventManager.addListener(event, self)

            event = Events.NewGameEvent()
            self.eventManager.addListener(event, self)

            event = Events.UnpauseGameEvent()
            self.eventManager.addListener(event, self)

            event = Events.QuitEvent()
            self.eventManager.addListener(event, self)

        def notify(self, event):
            if isinstance(event, Events.QuitEvent):
                self.eventManager.running = False

            if isinstance(event, Events.TickEvent):
                self.engine.clock.tick(self.engine.options.tickSpeed)
                self.engine.redrawWindow() #redraw sprites
                self.eventManager.game.sleep() # CRITICAL: sleep for the minimum amount of time. DO NOT REMOVE THIS LINE
                pygame.display.update() #redraw screen

                if self.countdown:
                    self.counter -= 1
                    if self.counter == 0:
                        self.countdown = False

                        event = Events.LowerVolumeEvent()
                        self.eventManager.post(event)

            if isinstance(event, Events.NewGameEvent) or isinstance(event, Events.UnpauseGameEvent):
                self.counter = 240
                self.countdown = True

    def sleep(self, time = 0):
        pygame.time.wait(time)

    def applyOptions(self, newSensitivity, newDifficulty):
        from ball import Ball
        from paddle import Paddle
        from brick import Brick
        from widgets import SliderWidget

        # grab old difficulty
        oldDifficulty = self.options.difficultyValue

        # store new setting
        self.options.sensitivityValue = newSensitivity
        self.options.difficultyValue = newDifficulty

        # apply difficulty
        self.options.paddleWidth = self.options.difficulty[self.options.difficultyValue]["paddleWidth"]
        self.options.brickHitsRemaining = self.options.difficulty[self.options.difficultyValue]["brickHitsRemaining"]
        self.options.ballSpeed = self.options.difficulty[self.options.difficultyValue]["ballSpeed"]
        self.options.ballRadius = self.options.difficulty[self.options.difficultyValue]["ballRadius"]
        self.options.levelBackgroundImage = self.options.difficulty[self.options.difficultyValue]["backgroundImage"]

        # ball size has probably changed, update the bounds for the paddle
        self.options.paddleLeftBound = self.options.ballRadius / 2
        self.options.paddleRightBound = self.options.paddleLeftBound

        # update sounds, does nothing as of yet
        self.options.soundPlayAmbient = self.options.soundPlayAmbient
        self.options.soundPlayBrickHit = self.options.soundPlayBrickHit
        self.options.soundPlayBrickDestroyed = self.options.soundPlayBrickDestroyed
        self.options.soundPlayBallBounce = self.options.soundPlayBallBounce

        self.options.soundVolumeBallBounce = self.options.soundVolumeBallBounce
        self.options.soundVolumeBrickDestroyed = self.options.soundVolumeBrickDestroyed
        self.options.soundVolumeBrickHit = self.options.soundVolumeBrickHit
        self.options.soundVolumeAmbient = self.options.soundVolumeAmbient


        if self.screens:
            if "level" in self.screens.keys():
                screen = self.screens["level"]
                screen.setBackgroundImage(self.options.levelBackgroundImage)

                balls = screen.getWidgets(Ball)
                for ball in balls:
                    ball.speed = self.options.ballSpeed
                    ball.radius = self.options.ballRadius

                paddles = screen.getWidgets(Paddle)
                for paddle in paddles:
                    paddle.sensitivity = self.options.sensitivityValue
                    paddle.width = self.options.paddleWidth

                oldBrickHitsRemaining = self.options.difficulty[oldDifficulty]["brickHitsRemaining"]
                bricks = screen.getWidgets(Brick)
                for brick in bricks:
                    # update hitsRemaining as needed
                    differenceInHitsRemaining = oldBrickHitsRemaining - brick.hitsRemaining
                    if differenceInHitsRemaining == 0:
                        # hits remaining should be new max hits remaining
                        brick.hitsRemaining = self.options.brickHitsRemaining
                    elif brick.hitsRemaining < 0:
                        # brick should already be eliminated so...
                        pass
                    else:
                        # difference is non-zero and brick has hits remaining. adjust for new hits remaining.
                        brick.hitsRemaining = self.options.brickHitsRemaining - differenceInHitsRemaining

                    brick.animate()

            #ensure parity between both options screen and pause screen
            screens = ("options", "pause")
            for s in screens:
                if self.screens[s]:
                    screen = self.screens[s]

                    sliders = screen.getWidgets(SliderWidget)
                    for slider in sliders:
                        if slider.valueKey == "sensitivity":
                            slider.setValue(self.options.sensitivityValue)

                        if slider.valueKey == "difficulty":
                            slider.setValue(self.options.difficultyValue)

    def redrawWindow(self):
        screen = self.screens[self.activeScreen]
        screen.redraw(self.window)

    def end(self):
        self.eventManager.running = False
        pygame.display.quit()
        pygame.quit()

    def __init__(self, game):
        #Initial module setup

        #Instantiate the eventManager
        self.eventManager = EventManager(game)

        #make an instance of GUI and Options classes so the interpreter won't kvetch
        self.GUI = Engine.GUI()
        self.defaults = Engine.Options() # first instance is read-only
        self.options = Engine.Options() # second is changeable
        #self.GUI.Widget = Engine.GUI.Widget() #interpreter doesn't kvetch on not having an instance of Widget, so commenting out for now

        self.sprites = pygame.sprite.Group()
        self.screens = {}
        self.activeScreen = ""

        # ensure the sound mixer is available
        if pygame.mixer.get_init() == None:
            pygame.mixer.init()

        # set up sound channels
        pygame.mixer.set_num_channels(self.options.soundNumberOfChannels)
        self.soundAmbientChannel = pygame.mixer.Channel(self.options.soundAmbientChannelNumber)

        #Create a window and start a clock
        pygame.init()
        self.window = pygame.display.set_mode(self.options.windowSize, pygame.SRCALPHA, 32)
        pygame.display.set_caption(self.options.name)
        self.clock = pygame.time.Clock()
