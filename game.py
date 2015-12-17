#Game class
# The main class which will provide the framework for the rest of the
# game objects to run in.
# Includes the main event loop, clock, window settings, etc.

# Requires pygame

import pygame
from engine import *
from eventManager import *
from widgets import *
from ball import *
from brick import *
from paddle import *

class Game(Engine):
    def __init__(self):
        # pass a reference to the game to the Engine
        # this will allow easy access to other things in the Engine
        # that some widgets need (e.g., the Options class)
        super().__init__(self)

        # initialize the Ticker
        self.ticker = Engine.Ticker(self)

        # register event listeners
        event = Events.NewGameEvent()
        self.eventManager.addListener(event, self)

        event = Events.ShowOptionsEvent()
        self.eventManager.addListener(event, self)

        event = Events.ApplyOptionsEvent()
        self.eventManager.addListener(event, self)

        event = Events.ResetValuesToDefaultsEvent()
        self.eventManager.addListener(event, self)

        event = Events.CancelOptionsEvent()
        self.eventManager.addListener(event, self)

        event = Events.PauseGameEvent()
        self.eventManager.addListener(event, self)

        event = Events.UnpauseGameEvent()
        self.eventManager.addListener(event, self)

        event = Events.GameOverEvent()
        self.eventManager.addListener(event, self)

        event = Events.LevelCompleteEvent()
        self.eventManager.addListener(event, self)

        event = Events.ShowStartEvent()
        self.eventManager.addListener(event, self)

    def postEvent(self, event):
        # make a closure so we can abstract an event poster rather than having to write a seperate method to post each type of event
        def generateEventPoster():
            e = event()
            self.eventManager.post(e)
        return generateEventPoster

    def makeLevel(self):
        screen = Engine.Level(mouseVisible = False)
        screen.score = self.options.score
        screen.setBackgroundImage(self.options.levelBackgroundImage)
        screen.soundAmbient = self.options.levelSoundAmbient
        screen.soundAmbientStartAt = 103
        screen.soundVolumeAmbient = 0.75

        wall = Brick((400, 300)) # use for quick testing
        #wall = Brick.createWall(self.options)
        screen.addWidget(wall)

        ball = Ball(screen)
        screen.addWidget(ball)

        paddle = Paddle()
        screen.addWidget(paddle)

        ballTracker = StatTracker(self.Stats.BALLS_REMAINING, self.options.ballsRemaining, backgroundColor = self.Colors.WHITE_TRANSLUCENT, transparentBackground = False)
        ballTracker.leftEdge(self.options.levelZoneInfo.leftEdge())
        ballTracker.bottomEdge(self.options.levelZoneInfo.bottomEdge())
        screen.addWidget(ballTracker)

        scoreTracker = StatTracker(self.Stats.SCORE, screen.score)
        scoreTracker.rightEdge(self.options.levelZoneInfo.rightEdge() - 25)
        scoreTracker.bottomEdge(self.options.levelZoneInfo.bottomEdge())
        screen.addWidget(scoreTracker)

        return screen

    def makeLevelComplete(self):
        screen = Engine.Layer()
        screen.setFillColor(self.Colors.WHITE_TRANSLUCENT)
        screen.soundAmbient = self.options.levelCompleteSoundAmbient

        gameOver = Label("Level Complete")
        gameOver.centerOn(self.window)
        screen.addWidget(gameOver)

        action = self.postEvent(Events.NewGameEvent)
        continueButton = Button("Continue", buttonColor = Engine.Colors.GREY, onClickAction = action)
        continueButton.setPosition(50, 500)
        screen.addWidget(continueButton)

        action = self.postEvent(Events.ShowStartEvent)
        mainButton = Button("Main Menu", buttonColor = Engine.Colors.GREY, onClickAction = action)
        mainButton.centerOn(self.window)
        mainButton.setPosition(y = 500)
        screen.addWidget(mainButton)

        action = self.postEvent(Events.QuitEvent)
        quitButton = Button("Quit", buttonColor = Engine.Colors.GREY, onClickAction = action)
        quitButton.setPosition(625, 500)
        screen.addWidget(quitButton)

        return screen

    def makeOptions(self):
        screen = Engine.Layer()

        title = Label("Game Options", self.Colors.BLACK)
        title.setPosition(34, 27)
        screen.addWidget(title)

        sensitivityLabel = Label("Sensitivity", self.Colors.BLACK)
        sensitivityLabel.setPosition(50, 125)
        screen.addWidget(sensitivityLabel)

        sensitivity = SliderWidget("sensitivity", self.options.availableSensitivities, self.options.sensitivityValue)
        sensitivity.setPosition(530, sensitivityLabel.rect.y + 20)
        screen.addWidget(sensitivity)

        difficultyLabel = Label("Difficulty", self.Colors.BLACK)
        difficultyLabel.setPosition(50, 225)
        screen.addWidget(difficultyLabel)

        difficulty = SliderWidget("difficulty", self.options.availableDifficulties, self.options.difficultyValue)
        difficulty.setPosition(530, difficultyLabel.rect.y + 20)
        screen.addWidget(difficulty)

        action = self.postEvent(Events.ApplyOptionsEvent)
        saveButton = Button("Apply", buttonColor = self.Colors.LIGHT_GREY, onClickAction = action)
        saveButton.setPosition(34, 500)
        screen.addWidget(saveButton)

        action = self.postEvent(Events.ResetValuesToDefaultsEvent)
        defaultsButton = Button("Defaults", buttonColor = self.Colors.LIGHT_GREY, onClickAction = action)
        defaultsButton.centerOn(self.window)
        defaultsButton.setPosition(y = 500)
        screen.addWidget(defaultsButton)

        action = self.postEvent(Events.CancelOptionsEvent)
        cancelButton = Button("Cancel", buttonColor = self.Colors.LIGHT_GREY, onClickAction = action)
        cancelButton.setPosition(591, 500)
        screen.addWidget(cancelButton)

        return screen

    def makePause(self):
        screen = self.makeOptions()

        screen.setFillColor(self.Colors.WHITE_TRANSLUCENT)

        action = self.postEvent(Events.ShowStartEvent)
        mainMenuButton = Button("Main Menu", buttonColor = self.Colors.LIGHT_GREY, onClickAction = action)
        mainMenuButton.setPosition(517, 27)
        screen.addWidget(mainMenuButton)

        return screen

    def makeStart(self):
        screen = Engine.Layer()
        screen.setBackgroundImage(self.options.backgroundImage)
        screen.soundAmbient = self.options.soundAmbient

        title = Label(self.options.name, self.Colors.DARK_BLUE, fontSize = 256)
        title.centerOn(self.window)
        title.setPosition(y = 200)
        screen.addWidget(title)

        action = self.postEvent(Events.NewGameEvent)
        startButton = Button("Start", buttonColor = Engine.Colors.GREY, onClickAction = action)
        startButton.setPosition(50, 500)
        screen.addWidget(startButton)

        action = self.postEvent(Events.ShowOptionsEvent)
        optionsButton = Button("Options", onClickAction = action)
        optionsButton.centerOn(self.window)
        optionsButton.setPosition(y = 500)
        screen.addWidget(optionsButton)

        action = self.postEvent(Events.QuitEvent)
        quitButton = Button("Quit", onClickAction = action)
        quitButton.setPosition(625, 500)
        screen.addWidget(quitButton)

        return screen

    def makeGameOver(self):
        screen = Engine.Layer()
        screen.setFillColor(self.Colors.WHITE_TRANSLUCENT)

        gameOver = Label("Game Over")
        gameOver.centerOn(self.window)
        screen.addWidget(gameOver)

        action = self.postEvent(Events.ShowStartEvent)
        mainButton = Button("Main Menu", buttonColor = Engine.Colors.GREY, onClickAction = action)
        mainButton.setPosition(50, 500)
        screen.addWidget(mainButton)

        action = self.postEvent(Events.QuitEvent)
        quitButton = Button("Quit", buttonColor = Engine.Colors.GREY, onClickAction = action)
        quitButton.setPosition(625, 500)
        screen.addWidget(quitButton)

        return screen

    def showScreen(self, screenName):
        screen = self.screens[self.activeScreen]
        screen.deactivate()
        self.sleep() # allow event processing to occur outside of the pygame engine

        self.activeScreen = screenName
        screen = self.screens[self.activeScreen]

        pygame.mouse.set_visible(screen.mouseVisible)

        self.screens[self.activeScreen].activate()

        if screen.soundAmbient != None:
            pygame.mixer.music.load(screen.soundAmbient)
            pygame.mixer.music.play(-1, start = screen.soundAmbientStartAt)
            pygame.mixer.music.set_volume(screen.soundVolumeAmbient)

    def getCurrentStatValue(self, stat):
        if stat == self.Stats.BALLS_REMAINING:
            value = self.options.ballsRemaining
        elif stat == self.Stats.SCORE:
            value = self.options.score
        else:
            value = 0
            print("Unknown stat:", stat, "passed to Game.getCurrentStatValue(). Returning 0.")

        if "level" in self.screens.keys():
            level = self.screens["level"]
            trackers = level.getWidgets(StatTracker)
            for tracker in trackers:
                if tracker.stat == stat:
                    value = tracker.value()

        return value

    def notify(self, event):
        if isinstance(event, Events.NewGameEvent):
            self.screens["level"] = self.makeLevel()
            self.showScreen("level")

        if isinstance(event, Events.ShowOptionsEvent):
            self.showScreen("options")

        if isinstance(event, Events.ApplyOptionsEvent):
            screen = self.screens[self.activeScreen]

            filterType = SliderWidget
            sliders = screen.getWidgets(filterType)
            for slider in sliders:
                screen.widgetValues[slider.valueKey] = slider.value

            self.applyOptions(screen.widgetValues["sensitivity"], screen.widgetValues["difficulty"])

            if self.activeScreen == "pause":
                event = Events.UnpauseGameEvent()
                self.eventManager.post(event)

                self.showScreen("level")

            else:
                self.showScreen("start")

        if isinstance(event, Events.ResetValuesToDefaultsEvent):
            widgets = self.screens[self.activeScreen].getWidgets()
            for widget in widgets:
                if hasattr(widget, "defaultValue"):
                    widget.setValue(widget.defaultValue)

        if isinstance(event, Events.CancelOptionsEvent):
            if self.activeScreen == "pause":
                event = Events.UnpauseGameEvent()
                self.eventManager.post(event)

                self.showScreen("level")

            else:
                self.showScreen("start")

        if isinstance(event, Events.PauseGameEvent):
            if self.activeScreen == "level":
                self.showScreen("pause")

        if isinstance(event, Events.GameOverEvent):
            # reset stats to defaults
            self.options.ballsRemaining = self.defaults.ballsRemaining
            self.options.score = self.defaults.score

            self.showScreen("game_over")

        if isinstance(event, Events.LevelCompleteEvent):
            self.options.ballsRemaining = self.getCurrentStatValue(self.Stats.BALLS_REMAINING)
            self.options.score = self.getCurrentStatValue(self.Stats.SCORE)
            self.showScreen("level_complete")

        if isinstance(event, Events.ShowStartEvent):
            # either it's the first run or user quit back to main, either way reset stats to defaults
            self.options.ballsRemaining = self.defaults.ballsRemaining
            self.options.score = self.defaults.score

            self.showScreen("start")

        if isinstance(event, Events.UnpauseGameEvent):
            level = self.screens["level"]
            level.checkIfLevelComplete()
            level.checkIfGameOver()

    @staticmethod
    def launch():
        game = Game()

        game.screens["start"] = game.makeStart()
        game.screens["options"] = game.makeOptions()
        game.screens["pause"] = game.makePause()
        game.screens["game_over"] = game.makeGameOver()
        game.screens["level_complete"] = game.makeLevelComplete()

        game.activeScreen = "start"

        game.showScreen(game.activeScreen)
        game.eventManager.processEvents()
        game.end()

Game.launch()
