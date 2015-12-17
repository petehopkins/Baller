import pygame
from engine import *
from eventManager import *

class Label(Engine.GUI.Widget):
    def __init__(self, text, textColor = None, backgroundColor = None, fontSize = None, padding = None, width = None, height = None, transparentBackground = True):
        super().__init__()

        self.textColor = textColor if textColor != None else self.options.labelWidgetTextColor
        self.backgroundColor = backgroundColor if backgroundColor != None else self.options.labelWidgetBackgroundColor
        self.hasTransparentBackground = transparentBackground

        self.fontSize = fontSize if fontSize != None else self.options.widgetFontSize
        self.font = pygame.font.Font(self.options.widgetFont, self.fontSize)
        self.text = text

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor) #need this here to get initial size
        self.textRect = self.renderedText.get_rect()
        self.rect = self.textRect #self.rect is actually Rect for widget, used here to provide initial size values

        self.padding = padding if padding != None else self.options.widgetPadding
        self.width = width
        if self.width == None:
            self.width = self.rect.width + self.padding
            self.rect.width = self.width

        self.height = height
        if self.height == None:
            self.height = self.rect.height + self.padding
            self.rect.height = self.height

    def redrawWidget(self):
        self.dirty = True
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.backgroundColor)

        if self.hasTransparentBackground:
            self.image.set_colorkey(self.backgroundColor)

        self.renderedText = self.font.render(self.text, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()

        self.textRect.x = (self.width / 2) - (self.textRect.width / 2)
        self.textRect.y = (self.height / 2) - (self.textRect.height / 2)

        self.image.blit(self.renderedText, self.textRect)

    def update(self):
        if self.dirty:
            self.redrawWidget()
            self.dirty = False

class StatTracker(Label):
    def __init__(self, stat, value, textColor = None, backgroundColor = None, fontSize = None, padding = None, width = None, height = None, transparentBackground = True):
        super().__init__(stat, textColor, backgroundColor, fontSize, padding, width, height, transparentBackground)

        self.stat = stat

        self.statValue = value
        self.text = stat

        self.valueFontSize = fontSize if fontSize != None else self.options.widgetFontSize
        self.valueFont = pygame.font.Font(self.options.widgetFont, self.valueFontSize)

        self.textFontSize = self.options.statTrackerTextFontSize
        self.textFont = pygame.font.Font(self.options.widgetFont, self.textFontSize)

        # get initial sizes
        self.renderedValue = self.valueFont.render(str(self.statValue), True, self.textColor, self.backgroundColor)
        self.valueRect = self.renderedValue.get_rect()

        self.renderedText = self.textFont.render(self.text, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()

        self.padding = padding if padding != None else self.options.statTrackerTextPadding
        self.width = width if width != None else max(self.valueRect.width, self.textRect.width) + self.padding
        self.height = height if height != None else self.valueRect.height + self.textRect.height + self.padding + self.options.statTrackerValueTextSpacing

        self.rect = self.textRect #self.rect is actually Rect for widget, used here to provide initial size values
        self.rect.width = self.width
        self.rect.height = self.height

    def addListeners(self):
        event = Events.StatUpdateEvent()
        self.eventManager.addListener(event, self)

    def notify(self, event):
        if isinstance(event, Events.StatUpdateEvent):
            if event.stat == self.stat:
                self.value(event.value)

    def value(self, value = None):
        if value != None:
            self.statValue += value
            self.redrawWidget()

        return self.statValue

    def redrawWidget(self):
        self.dirty = True
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.backgroundColor)

        if self.hasTransparentBackground:
            self.image.set_colorkey(self.backgroundColor)

        self.renderedValue = self.valueFont.render(str(self.statValue), True, self.textColor, self.backgroundColor)
        self.valueRect = self.renderedValue.get_rect()
        self.valueRect.x = (self.width / 2) - (self.valueRect.width / 2)
        self.valueRect.y = (self.padding / 2) #self.topEdge() +

        self.renderedText = self.textFont.render(self.text, True, self.textColor, self.backgroundColor)
        self.textRect = self.renderedText.get_rect()
        self.textRect.x = (self.width / 2) - (self.textRect.width / 2)
        self.textRect.y = self.rect.height - (self.padding / 2) - self.textRect.height

        self.width = max(self.valueRect.width, self.textRect.width) + self.padding
        self.rect.width = self.width

        self.image.blit(self.renderedValue, self.valueRect)
        self.image.blit(self.renderedText, self.textRect)

class HoverableWidget(Label):
    def __init__(self, text, textColor = None, backgroundColor = None, fontSize = None, padding = None, onHoverAction = None, width = None, height = None, transparentBackground = False):
        super().__init__(text, textColor, backgroundColor, fontSize, padding, width, height, transparentBackground)

        self.unfocusedBackgroundColor = self.backgroundColor
        self.focusedBackgroundColor = self.getFocusedColor(self.backgroundColor)

        if onHoverAction:
            self.onHoverAction = onHoverAction
        else:
            self.onHoverAction = self.changeBackground

    def addListeners(self):
        event = Events.HoverWidgetEvent()
        self.eventManager.addListener(event, self)

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

class Button(HoverableWidget):
    def __init__(self, text, textColor = None, buttonColor = None, fontSize = None, padding = None, onClickAction = None, onHoverAction = None, width = None, height = None):
        super().__init__(text, textColor, buttonColor, fontSize, padding, onHoverAction, width, height, transparentBackground = False)

        self.onClickAction = onClickAction

    def addListeners(self):
        super().addListeners()

        event = Events.LeftClickWidgetEvent()
        self.eventManager.addListener(event, self)
        #print("Adding listeners for", self.text)

    def click(self):
        if self.onClickAction:
            self.dirty = True
            self.onClickAction()

    def notify(self, event):
        super().notify(event)

        if isinstance(event, Events.LeftClickWidgetEvent) and self.rect.collidepoint(event.pos):
            #print("Firing", event.name, "for Listener", self.text)
            self.click()

        elif isinstance(event, Events.KeyboardActivateWidgetEvent) and self.focused:
            self.click()

class SliderWidget(Engine.GUI.Widget):
    def __init__(self, valueKey, values, defaultValue, textColor = None, fillColor = None, backgroundColor = None, onDragAction = None, transparentBackground = True):
        super().__init__()

        self.eventManager = EventManager()

        self.textColor = textColor if textColor != None else self.options.sliderWidgetTextColor
        self.fillColor = fillColor if fillColor != None else self.options.sliderWidgetFillColor
        self.backgroundColor = backgroundColor if backgroundColor != None else self.options.sliderWidgetBackgroundColor
        self.hasTransparentBackground = transparentBackground

        self.width = self.options.sliderWidth
        self.height = self.options.sliderHeight

        self.valueKey = valueKey
        self.defaultValue = defaultValue
        self.text = str(self.defaultValue)
        self.value = self.defaultValue
        self.stepValues = {}

        self.font = pygame.font.Font(self.options.widgetFont, self.options.sliderFontSize)

        self.onDragAction = onDragAction if onDragAction != None else self.slideToValue

        self.image = pygame.Surface((self.width, self.height)) #contains bar, slide and text; all are defined here for initial positioning
        self.rect = self.image.get_rect()

        self.bar = pygame.Surface((self.options.sliderWidth, self.options.sliderBarHeight))
        self.bar.fill(self.fillColor)
        self.barRect = self.bar.get_rect()
        self.barRect.x = self.options.sliderBarOffsetX
        self.barRect.y = self.options.sliderBarOffsetY

        self.slide = pygame.Surface((self.options.sliderSlideWidth, self.options.sliderSlideHeight))
        self.slide.fill(self.fillColor)
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

        if self.hasTransparentBackground:
            self.image.set_colorkey(self.backgroundColor)

        self.bar = pygame.Surface((self.options.sliderWidth, self.options.sliderBarHeight))
        self.bar.fill(self.fillColor)

        self.slide = pygame.Surface((self.options.sliderSlideWidth, self.options.sliderSlideHeight))
        self.slide.fill(self.fillColor)

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
