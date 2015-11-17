#Game class
# The main class which will provide the framework for the rest of the
# game objects to run in.
# Includes the main event loop, clock, window settings, etc.

# Requires pygame

import pygame
from engine import *
from eventManager import *
from widgets import *
from bricks import *
from ball import *

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

        event = Events.SaveOptionsEvent()
        self.eventManager.addListener(event, self)

        event = Events.ResetValuesToDefaultsEvent()
        self.eventManager.addListener(event, self)

        event = Events.CancelOptionsEvent()
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

    def postSaveOptionsEvent(self):
        event = Events.SaveOptionsEvent()
        self.eventManager.post(event)

    def postResetValuesToDefaultsEvent(self):
        event = Events.ResetValuesToDefaultsEvent()
        self.eventManager.post(event)

    def postCancelOptionsEvent(self):
        event = Events.CancelOptionsEvent()
        self.eventManager.post(event)

    def makeLevel(self):
        screen = Engine.Layer()

        windowWidth = self.window.get_rect().width
        windowHeight = self.window.get_rect().height

        wall = Bricks(self.eventManager, windowWidth, windowHeight)
        screen.addSprite(wall.getPile().sprites())

        ball = Ball(self.eventManager)
        screen.addSprite(ball)

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

        sensitivity = SliderWidget(self.eventManager, range(0, 100), 99)
        sensitivity.setPosition(530, sensitivityLabel.rect.y + 20)
        screen.addWidget(sensitivity)

        difficultyLabel = Label(self.eventManager, "Difficulty", self.Colors.BLACK)
        difficultyLabel.setPosition(50, 300)
        screen.addWidget(difficultyLabel)

        difficulty = SliderWidget(self.eventManager, self.Options.availableDifficulties, 1)
        difficulty.setPosition(530, difficultyLabel.rect.y + 20)
        screen.addWidget(difficulty)

        saveButton = Button(self.eventManager, "Save", buttonColor = self.Colors.LIGHT_GREY, onClickAction = self.postSaveOptionsEvent)
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

    def makeStart(self):
        screen = Engine.Layer()

        title = Label(self.eventManager, self.name, self.Colors.LAVENDER)
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

        self.activeScreen = screenName
        screen = self.screens[self.activeScreen]

        self.window.fill(self.windowFillColor)
        screen.redrawWidgets(self.window)
        screen.redrawSprites(self.window)

        event = Events.ActivateScreenEvent() # If not posted as an event, the activate method will add listeners in time for a click event to hit buttons that weren't listening at the time of the click
        self.eventManager.post(event) #seems to indicate that pygame is muli-threaded, but we haven't started another thread so why is this acting like a race condition?

    def notify(self, event):
        if isinstance(event, Events.ActivateScreenEvent):
            self.screens[self.activeScreen].activate()

        if isinstance(event, Events.NewGameEvent):
            self.showScreen("level")

        if isinstance(event, Events.ShowOptionsEvent):
            self.showScreen("options")

        if isinstance(event, Events.SaveOptionsEvent):
            self.showScreen("start")

        if isinstance(event, Events.ResetValuesToDefaultsEvent):
            widgets = self.screens[self.activeScreen].getWidgets()
            for widget in widgets:
                if hasattr(widget, "defaultValue"):
                    widget.setValue(widget.defaultValue)

        if isinstance(event, Events.CancelOptionsEvent):
            self.showScreen("start")

    @staticmethod
    def launch():
        game = Game()

        game.screens["start"] = game.makeStart()
        game.screens["options"] = game.makeOptions()
        game.screens["level"] = game.makeLevel()

        game.activeScreen = "start"

        game.showScreen(game.activeScreen)
        game.eventManager.processEvents()
        game.end()

Game.launch()
