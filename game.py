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

        event = Events.ShowOptionsEvent()
        self.eventManager.addListener(event, self)

        event = Events.NewGameEvent()
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

    def makeLevel(self):
        screen = Engine.Layer()
        
        windowWidth = self.window.get_rect().width
        windowHeight = self.window.get_rect().height
        
        wall = Bricks(self.eventManager, windowWidth, windowHeight)
        screen.addSprite(wall.getPile().sprites())

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

        sensitivity = SliderWidget(self.eventManager, range(0, 100), 0)
        sensitivity.setPosition(550, sensitivityLabel.rect.y + 20)
        screen.addWidget(sensitivity)

        difficultyLabel = Label(self.eventManager, "Difficulty", self.Colors.BLACK)
        difficultyLabel.setPosition(50, 300)
        screen.addWidget(difficultyLabel)

        difficulty = SliderWidget(self.eventManager, [0,1,2,3,4], 0)
        difficulty.setPosition(550, difficultyLabel.rect.y + 20)
        screen.addWidget(difficulty)

        saveButton = Button(self.eventManager, "Set Options", buttonColor = self.Colors.GREY)
        saveButton.setPosition(50, 500)
        screen.addWidget(saveButton)

        cancelButton = Button(self.eventManager, "Cancel", buttonColor = self.Colors.LAVENDER)
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
        screen = self.screens[screenName]

        self.screens[self.activeScreen].deactivate()
        self.activeScreen = screenName

        self.window.fill(self.windowFillColor)
        screen.addWidgetListeners()
        screen.redrawWidgets(self.window)
        screen.addSpriteListeners()
        screen.redrawSprites(self.window)

    def notify(self, event):
        if isinstance(event, Events.ShowOptionsEvent):
            self.showScreen("options")

        if isinstance(event, Events.NewGameEvent):
            self.showScreen("level")

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
