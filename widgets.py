import pygame
from engine import *
from eventManager import *

class HoverableWidget(Engine.GUI.Widget):
    def __init__(self, eventManager, text, textColor = None, backgroundColor = None, width = None, height = None, onHoverAction = None, container = None):
        super().__init__(eventManager, container)

        if textColor:
            self.textColor = textColor
        else:
            self.textColor = Engine.Colors.BLACK

        if backgroundColor == None:
            backgroundColor = Engine.Colors.WHITE

        self.backgroundColor = backgroundColor
        self.unfocusedBackgroundColor = self.backgroundColor
        self.focusedBackgroundColor = self.getFocusedColor(self.backgroundColor)

        self.font = pygame.font.Font(None, self.options.widgetFontSize)
        self.text = text

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor) #need this here to get initial size
        self.textRect = self.renderedText.get_rect()
        self.rect = self.textRect #self.rect is actually Rect for widget, used here to provide initial size values

        self.width = width
        if self.width == None:
            self.width = self.rect.width + self.options.widgetPadding
            self.rect.width = self.width

        self.height = height
        if self.height == None:
            self.height = self.rect.height + self.options.widgetPadding
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
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.backgroundColor)

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()

        self.textRect.x = (self.width / 2) - (self.textRect.width / 2)
        self.textRect.y = (self.height / 2) - (self.textRect.height / 2)

        self.image.blit(self.renderedText, self.textRect)

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
    def __init__(self, eventManager, text, textColor = None, buttonColor = None, onClickAction = None, onHoverAction = None, container = None):
        super().__init__(eventManager, text, textColor, buttonColor, onHoverAction, container)

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
    def __init__(self, eventManager, valueKey, values, defaultValue, textColor = None, backgroundColor = None, container = None, onDragAction = None):
        super().__init__(eventManager, container)

        self.eventManager = eventManager

        if textColor:
            self.textColor = textColor
        else:
            self.textColor = Engine.Colors.BLACK

        if backgroundColor == None:
            backgroundColor = Engine.Colors.WHITE

        self.backgroundColor = backgroundColor
        self.width = self.options.sliderWidth
        self.height = self.options.sliderHeight

        self.valueKey = valueKey
        self.defaultValue = defaultValue
        self.text = str(self.defaultValue)
        self.value = self.defaultValue
        self.stepValues = {}

        self.font = pygame.font.Font(None, self.options.sliderFontSize)

        if onDragAction:
            self.onDragAction = onDragAction
        else:
            self.onDragAction = self.slideToValue

        self.image = pygame.Surface((self.width, self.height)) #contains bar, slide and text; all are defined here for initial positioning
        self.rect = self.image.get_rect()

        self.bar = pygame.Surface((self.options.sliderWidth, self.options.sliderBarHeight))
        self.bar.fill(Engine.Colors.LIGHT_GREY)
        self.barRect = self.bar.get_rect()
        self.barRect.x = self.options.sliderBarOffsetX
        self.barRect.y = self.options.sliderBarOffsetY

        self.slide = pygame.Surface((self.options.sliderSlideWidth, self.options.sliderSlideHeight))
        self.slide.fill(Engine.Colors.LIGHT_GREY)
        self.slideRect = self.slide.get_rect()

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()
        self.textRect.x = (self.image.get_rect().width / 2) - (self.textRect.width / 2)
        self.textRect.y = self.image.get_rect().height - self.options.sliderTextOffsetY - self.textRect.height

        #make a lookup table for slide position and value
        vals = len(values) - 1
        isRawList = not (type(values[0]) == type([]) or type(values[0]) == type(()))
        maxStep = self.barRect.width - self.slideRect.width
        minStep = 0
        stepCounter = 0
        self.step = ((maxStep - minStep) / vals)
        for val in values:
            key = self.step * stepCounter
            if isRawList:
                self.stepValues[key] = (str(val), val) #mimic (label, value)
            else:
                self.stepValues[key] = val #should already be (label, value) or [label, value]

            stepCounter += 1

        self.setValue(self.defaultValue)

    def addListeners(self):
        event = Events.DragWidgetEvent()
        self.eventManager.addListener(event, self)

        event = Events.LeftClickWidgetEvent()
        self.eventManager.addListener(event, self)

    def redrawWidget(self):
        self.dirty = True

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.backgroundColor)

        self.bar = pygame.Surface((self.options.sliderWidth, self.options.sliderBarHeight))
        self.bar.fill(Engine.Colors.LIGHT_GREY)

        self.slide = pygame.Surface((self.options.sliderSlideWidth, self.options.sliderSlideHeight))
        self.slide.fill(Engine.Colors.LIGHT_GREY)

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()
        self.textRect.x = (self.image.get_rect().width / 2) - (self.textRect.width / 2)
        self.textRect.y = self.image.get_rect().height - self.options.sliderTextOffsetY - self.textRect.height

        self.image.blit(self.bar, self.barRect)
        self.image.blit(self.slide, self.slideRect)
        self.image.blit(self.renderedText, self.textRect)

    def update(self):
        if self.dirty:
            self.redrawWidget()
            self.dirty = False

    def drag(self, pos):
        if self.onDragAction:
            self.dirty = True
            self.onDragAction(pos)
            self.update()

    def setValue(self, val):
        for key in self.stepValues.keys():
            item = self.stepValues[key]
            if val == item[0] or val == item[1]:
                self.slideToValue(key)

    def slideToValue(self, dx):
        self.dirty = True
        closestStep = int(dx / self.step) #ensure integer
        key = closestStep * self.step

        if key in self.stepValues.keys():
            item = self.stepValues[key]
            self.text = item[0]
            self.value = item[1]
            self.slideRect.x = key
        self.update()


    def handleIfOnSelf(self, event):
        relx = event.pos[0] - self.rect.x
        minx = self.barRect.x - self.options.sliderDragPaddingX
        maxx = minx + self.barRect.width + self.options.sliderDragPaddingX

        rely = event.pos[1] - self.rect.y
        miny = self.slideRect.y
        maxy = miny + self.slideRect.height

        if (minx <= relx <= maxx and miny <= rely <= maxy):
            self.drag(relx)

    def notify(self, event):
        if isinstance(event, Events.DragWidgetEvent):
            self.handleIfOnSelf(event)

        if isinstance(event, Events.LeftClickWidgetEvent):
            self.handleIfOnSelf(event)
