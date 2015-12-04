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
        super().__init__()
        self.eventManager = EventManager(self)
        self.ticker = Engine.Ticker(self.eventManager, self)

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
        screen = Engine.Layer(mouseVisible = False)

        wall = Brick.createWall(self.eventManager, self.options)
        screen.addWidget(wall)

        ball = Ball(self.eventManager, screen)
        screen.addWidget(ball)

        paddle = Paddle(self.eventManager)
        screen.addWidget(paddle)

        return screen

    def makeOptions(self):
        screen = Engine.Layer()

        title = Label(self.eventManager, "Options", self.Colors.BLACK)
        title.centerOn(self.window)
        title.setPosition(y = 100)
        screen.addWidget(title)

        sensitivityLabel = Label(self.eventManager, "Sensitivity", self.Colors.BLACK)
        sensitivityLabel.setPosition(50, 200)
        screen.addWidget(sensitivityLabel)

        sensitivity = SliderWidget(self.eventManager, "sensitivity", self.options.availableSensitivities, self.options.sensitivityValue)
        sensitivity.setPosition(530, sensitivityLabel.rect.y + 20)
        screen.addWidget(sensitivity)

        difficultyLabel = Label(self.eventManager, "Difficulty", self.Colors.BLACK)
        difficultyLabel.setPosition(50, 300)
        screen.addWidget(difficultyLabel)

        difficulty = SliderWidget(self.eventManager, "difficulty", self.options.availableDifficulties, self.options.difficultyValue)
        difficulty.setPosition(530, difficultyLabel.rect.y + 20)
        screen.addWidget(difficulty)

        saveButton = Button(self.eventManager, "Apply", buttonColor = self.Colors.LIGHT_GREY, onClickAction = self.postApplyOptionsEvent)
        saveButton.setPosition(50, 500)
        screen.addWidget(saveButton)

        defaultsButton = Button(self.eventManager, "Defaults", buttonColor = self.Colors.LIGHT_GREY, onClickAction = self.postResetValuesToDefaultsEvent)
        defaultsButton.centerOn(self.window)
        defaultsButton.setPosition(y = 500)
        screen.addWidget(defaultsButton)

        cancelButton = Button(self.eventManager, "Cancel", buttonColor = self.Colors.LIGHT_GREY, onClickAction = self.postCancelOptionsEvent)
        cancelButton.setPosition(575, 500)
        screen.addWidget(cancelButton)

        return screen

    def makePause(self):
        screen = self.makeOptions()
        screen.fillColor = self.Colors.WHITE_TRANSLUCENT
        return screen

    def makeStart(self):
        screen = Engine.Layer()

        title = Label(self.eventManager, self.options.name, self.Colors.LAVENDER)
        title.centerOn(self.window)
        title.setPosition(y = 200)
        screen.addWidget(title)

        startButton = Button(self.eventManager, "Start", buttonColor = Engine.Colors.GREY, onClickAction = self.postNewGameEvent)
        startButton.setPosition(50, 500)
        screen.addWidget(startButton)

        optionsButton = Button(self.eventManager, "Options", onClickAction = self.postShowOptionsEvent)
        optionsButton.centerOn(self.window)
        optionsButton.setPosition(y = 500)
        screen.addWidget(optionsButton)

        quitButton = Button(self.eventManager, "Quit", onClickAction = self.postQuitEvent)
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

        self.window.fill(screen.fillColor)
        screen.redrawWidgets(self.window)

        self.screens[self.activeScreen].activate()

    def notify(self, event):
        if isinstance(event, Events.NewGameEvent):
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

    @staticmethod
    def launch():
        game = Game()

        game.screens["start"] = game.makeStart()
        game.screens["options"] = game.makeOptions()
        game.screens["pause"] = game.makePause()
        game.screens["level"] = game.makeLevel()

        game.activeScreen = "start"

        game.showScreen(game.activeScreen)
        game.eventManager.processEvents()
        game.end()

Game.launch()
