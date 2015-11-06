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

class Game(Engine):
    def __init__(self):
        super().__init__()
        self.eventManager = EventManager()
        self.ticker = Engine.Ticker(self.eventManager, self)

##    def makeWallOBricks(self):
##        self.window.fill(self.windowFillColor)
##        wall = Bricks(self.window, 8)
##        wall.redrawWall(self.window)
##        return True

    def showSplash(self):
        pass

    def postNewGameEvent(self):
        event = Events.NewGameEvent()
        self.eventManager.post(event)

    def postShowOptionsEvent(self):
        event = Events.ShowOptionsEvent()
        self.eventManager.post(event)

    def postQuitEvent(self):
        event = Events.QuitEvent()
        self.eventManager.post(event)

    def makeOptions(self):
        screen = Engine.Layer()

        title = Label(self.eventManager, "Options", self.Colors.BLACK)
        title.centerOn(self.window)
        title.setPosition(y = 100)
        screen.addWidget(title)

        difficulty = Label(self.eventManager, "Difficulty", self.Colors.BLACK)
        difficulty.setPosition(50, 300)
        screen.addWidget(difficulty)

        saveButton = Button(self.eventManager, "Save", buttonColor = self.Colors.GREY)
        saveButton.setPosition(50, 400)
        screen.addWidget(saveButton)

        cancelButton = Button(self.eventManager, "Cancel", buttonColor = self.Colors.LAVENDER)
        cancelButton.setPosition(625, 400)
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

    def showScreen(self, screen):
        self.window.fill(self.windowFillColor)
        screen.addWidgetListeners()
        screen.redrawWidgets(self.window)

    def notify(self, event):
        if isinstance(event, Events.ShowOptionsEvent):
            self.screens[self.activeScreen].deactivate()
            self.activeScreen = "options"
            self.showScreen(self.screens[self.activeScreen])

    @staticmethod
    def launch():
        game = Game()

        event = Events.ShowOptionsEvent()
        game.eventManager.addListener(event, game)

        screen =game.makeStart()
        game.screens["start"] = screen
        game.activeScreen = "start"

        screen = game.makeOptions()
        game.screens["options"] = screen

        game.showScreen(game.screens[game.activeScreen])
        game.eventManager.processEvents()

Game.launch()
