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

        self.ticker = Engine.Ticker(self)

        event = Events.ActivateScreenEvent()
        self.eventManager.addListener(event, self)

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

        event = Events.GameOverEvent()
        self.eventManager.addListener(event, self)

    def postNewGameEvent(self):
        event = Events.NewGameEvent()
        self.eventManager.post(event)

    def postShowOptionsEvent(self):
        event = Events.ShowOptionsEvent()
        self.eventManager.post(event)

    def postQuitEvent(self):
        event = Events.QuitEvent()
        self.eventManager.post(event)

    def postApplyOptionsEvent(self):
        event = Events.ApplyOptionsEvent()
        self.eventManager.post(event)

    def postResetValuesToDefaultsEvent(self):
        event = Events.ResetValuesToDefaultsEvent()
        self.eventManager.post(event)

    def postCancelOptionsEvent(self):
        event = Events.CancelOptionsEvent()
        self.eventManager.post(event)

    def makeLevel(self):
        screen = Engine.Level(mouseVisible = False)

        wall = Brick.createWall(self.options)
        screen.addWidget(wall)

        ball = Ball(screen)
        screen.addWidget(ball)

        paddle = Paddle()
        screen.addWidget(paddle)

        ballTracker = StatTracker(self.Stats.BALLS_REMAINING, self.options.ballsRemaining)
        ballTracker.leftEdge(self.options.levelZoneInfo.leftEdge())
        ballTracker.bottomEdge(self.options.levelZoneInfo.bottomEdge())
        screen.addWidget(ballTracker)

        scoreTracker = StatTracker(self.Stats.SCORE, self.options.score)
        scoreTracker.rightEdge(self.options.levelZoneInfo.rightEdge() - 25)
        scoreTracker.bottomEdge(self.options.levelZoneInfo.bottomEdge())
        screen.addWidget(scoreTracker)

        return screen

    def makeOptions(self):
        screen = Engine.Layer()

        title = Label("Options", self.Colors.BLACK)
        title.centerOn(self.window)
        title.setPosition(y = 100)
        screen.addWidget(title)

        sensitivityLabel = Label("Sensitivity", self.Colors.BLACK)
        sensitivityLabel.setPosition(50, 200)
        screen.addWidget(sensitivityLabel)

        sensitivity = SliderWidget("sensitivity", self.options.availableSensitivities, self.options.sensitivityValue)
        sensitivity.setPosition(530, sensitivityLabel.rect.y + 20)
        screen.addWidget(sensitivity)

        difficultyLabel = Label("Difficulty", self.Colors.BLACK)
        difficultyLabel.setPosition(50, 300)
        screen.addWidget(difficultyLabel)

        difficulty = SliderWidget("difficulty", self.options.availableDifficulties, self.options.difficultyValue)
        difficulty.setPosition(530, difficultyLabel.rect.y + 20)
        screen.addWidget(difficulty)

        saveButton = Button("Apply", buttonColor = self.Colors.LIGHT_GREY, onClickAction = self.postApplyOptionsEvent)
        saveButton.setPosition(50, 500)
        screen.addWidget(saveButton)

        defaultsButton = Button("Defaults", buttonColor = self.Colors.LIGHT_GREY, onClickAction = self.postResetValuesToDefaultsEvent)
        defaultsButton.centerOn(self.window)
        defaultsButton.setPosition(y = 500)
        screen.addWidget(defaultsButton)

        cancelButton = Button("Cancel", buttonColor = self.Colors.LIGHT_GREY, onClickAction = self.postCancelOptionsEvent)
        cancelButton.setPosition(575, 500)
        screen.addWidget(cancelButton)

        return screen

    def makePause(self):
        screen = self.makeOptions()
        screen.setFillColor(self.Colors.WHITE_TRANSLUCENT)
        return screen

    def makeStart(self):
        screen = Engine.Layer()

        title = Label(self.options.name, self.Colors.LAVENDER)
        title.centerOn(self.window)
        title.setPosition(y = 200)
        screen.addWidget(title)

        startButton = Button("Start", buttonColor = Engine.Colors.GREY, onClickAction = self.postNewGameEvent)
        startButton.setPosition(50, 500)
        screen.addWidget(startButton)

        optionsButton = Button("Options", onClickAction = self.postShowOptionsEvent)
        optionsButton.centerOn(self.window)
        optionsButton.setPosition(y = 500)
        screen.addWidget(optionsButton)

        quitButton = Button("Quit", onClickAction = self.postQuitEvent)
        quitButton.setPosition(625, 500)
        screen.addWidget(quitButton)

        return screen

    def makeGameOver(self):
        screen = Engine.Layer()
        screen.setFillColor(self.Colors.WHITE_TRANSLUCENT)

        gameOver = Label("Game Over")
        gameOver.centerOn(self.window)
        screen.addWidget(gameOver)

        mainButton = Button("Main Menu", buttonColor = Engine.Colors.GREY, onClickAction = self.postNewGameEvent)
        mainButton.setPosition(50, 500)
        screen.addWidget(mainButton)

        quitButton = Button("Quit", onClickAction = self.postQuitEvent)
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
                self.showScreen("level")
            else:
                self.showScreen("start")

        if isinstance(event, Events.PauseGameEvent):
            if self.activeScreen == "level":
                self.showScreen("pause")

        if isinstance(event, Events.GameOverEvent):
            self.showScreen("game_over")

    @staticmethod
    def launch():
        game = Game()

        game.screens["start"] = game.makeStart()
        game.screens["options"] = game.makeOptions()
        game.screens["pause"] = game.makePause()
        game.screens["game_over"] = game.makeGameOver()

        game.activeScreen = "start"

        game.showScreen(game.activeScreen)
        game.eventManager.processEvents()
        game.end()

Game.launch()
