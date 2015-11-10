import pygame
from engine import *
from eventManager import *

class HoverableWidget(Engine.GUI.Widget):
    def __init__(self, eventManager, text, textColor = None, backgroundColor = None, width = None, height = None, container = None, onHoverAction = None):
        super().__init__(eventManager, container)

        if textColor:
            self.textColor = textColor
        else:
            self.textColor = Engine.Colors.BLACK

        if backgroundColor == None:
            backgroundColor = (255, 255, 255, 0)

        self.backgroundColor = backgroundColor
        self.unfocusedBackgroundColor = self.backgroundColor
        self.focusedBackgroundColor = self.getFocusedColor(self.backgroundColor)

        self.font = pygame.font.Font(None, 56)
        self.text = text

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor) #need this here to get initial size
        self.textRect = self.renderedText.get_rect()
        self.rect = self.textRect #self.rect is actually Rect for widget, used here to provide initial size values

        self.width = width
        if self.width == None:
            self.width = self.rect.width + 40
            self.rect.width = self.width

        self.height = height
        if self.height == None:
            self.height = self.rect.height + 40
            self.rect.height = self.height

        if onHoverAction:
            self.onHoverAction = onHoverAction
        else:
            self.onHoverAction = self.changeBackground

    def get_rect(self):
        return self.rect

    def addListeners(self):
        event = Events.HoverWidgetEvent()
        self.eventManager.addListener(event, self)

    def redrawWidget(self):
        self.dirty = True
        self.widget = pygame.Surface((self.width, self.height))
        self.widget.fill(self.backgroundColor)

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()

        self.textRect.x = (self.width / 2) - (self.textRect.width / 2)
        self.textRect.y = (self.height / 2) - (self.textRect.height / 2)

        self.widget.blit(self.renderedText, self.textRect)

    def getContrastingShade(self, color):
        constrastingShadeOffset = .2 * 255

        if 255 - color > constrastingShadeOffset:
            color += constrastingShadeOffset
        else:
            color -= constrastingShadeOffset

        return color

    def getFocusedColor(self, color):
        r = self.getContrastingShade(color[0])
        g = self.getContrastingShade(color[1])
        b = self.getContrastingShade(color[2])
        a = None
        rgb = None

        if len(color) > 3:
            a = self.getContrastingShade(color[3])

        if a:
            rgb = (r, g, b, a)
        else:
            rgb = (r, g, b)

        return rgb

    def changeBackground(self):
        self.dirty = True

        if self.focused:
            self.backgroundColor = self.focusedBackgroundColor
        else:
            self.backgroundColor = self.unfocusedBackgroundColor

        self.update()

    def update(self):
        if self.dirty:
            self.redrawWidget()
            self.dirty = False

    def hover(self, focused):
        if self.onHoverAction:
            self.dirty = True
            self.focused = focused
            self.onHoverAction()
            self.update()

    def notify(self, event):
        if isinstance(event, Events.HoverWidgetEvent):
            focused = self.rect.collidepoint(event.pos)
            self.hover(focused)

Label = HoverableWidget #Friendly alias for HoverableWidget
##class Label(HoverableWidget):
##    def __init__(self, eventManager, text, textColor = None, backgroundColor = None, container = None, onHoverAction = None):
##        super().__init__(eventManager, text, textColor, backgroundColor, container, onHoverAction)

class Button(HoverableWidget):
    def __init__(self, eventManager, text, textColor = None, buttonColor = None, container = None, onClickAction = None, onHoverAction = None):
        super().__init__(eventManager, text, textColor, buttonColor, container, onHoverAction)

        self.onClickAction = onClickAction

    def addListeners(self):
        super().addListeners()

        event = Events.LeftClickWidgetEvent()
        self.eventManager.addListener(event, self)

    def click(self):
        if self.onClickAction:
            self.dirty = True
            self.onClickAction()

    def notify(self, event):
        super().notify(event)

        if isinstance(event, Events.LeftClickWidgetEvent) and self.rect.collidepoint(event.pos):
            self.click()

        elif isinstance(event, Events.KeyboardActivateWidgetEvent) and self.focused:
            self.click()

class SliderWidget(Engine.GUI.Widget):
    def __init__(self, eventManager, values, defaultValue, textColor = None, backgroundColor = None, container = None, onDragAction = None):
        super().__init__(eventManager, container)

        self.eventManager = eventManager

        if textColor:
            self.textColor = textColor
        else:
            self.textColor = Engine.Colors.BLACK

        if backgroundColor == None:
            backgroundColor = (255, 255, 255, 0)

        self.backgroundColor = backgroundColor
        self.width = 200
        self.height = 72

        self.font = pygame.font.Font(None, 24)
        self.values = values
        self.step = self.width / len(values)
        self.value = str(defaultValue)

        if onDragAction:
            self.onDragAction = onDragAction
        else:
            self.onDragAction = self.changeValue

        self.widget = pygame.Surface((200, 72)) #contains bar, box and text; defined here for initial positioning
        self.rect = self.widget.get_rect()

    def addListeners(self):
        event = Events.DragWidgetEvent()
        self.eventManager.addListener(event, self)

        event = Events.LeftClickWidgetEvent()
        self.eventManager.addListener(event, self)

    def redrawWidget(self):
        self.dirty = True

        self.widget = pygame.Surface((200, 72)) #contains bar, box and text
        self.widget.fill(self.backgroundColor)
        #self.rect = self.widget.get_rect()

        self.bar = pygame.Surface((200, 10))
        self.bar.fill(Engine.Colors.GREY)
        self.barRect = self.bar.get_rect()
        self.barRect.x = 0
        self.barRect.y = 15

        self.box = pygame.Surface((10, 40))
        self.box.fill(Engine.Colors.GREY)
        self.boxRect = self.box.get_rect()

        self.renderedText = self.font.render(self.value, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()
        self.textRect.x = (self.widget.get_rect().width / 2) - (self.textRect.width / 2)
        self.textRect.y = self.widget.get_rect().height - 8 - self.textRect.height

        self.widget.blit(self.bar, self.barRect)
        self.widget.blit(self.box, self.boxRect)
        self.widget.blit(self.renderedText, self.textRect)

    def update(self):
        if self.dirty:
            self.redrawWidget()
            self.dirty = False

    def drag(self, pos):
        if self.onDragAction:
            self.dirty = True
            self.onDragAction(pos)
            self.update()

    def changeValue(self, pos):
        dx = pos[0]

    def notify(self, event):
        if isinstance(event, Events.DragWidgetEvent) and self.rect.collidepoint(event.pos):
            self.drag(event.pos)

        if isinstance(event, Events.LeftClickWidgetEvent) and self.rect.collidepoint(event.pos):
            self.drag(event.pos)
