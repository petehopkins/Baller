import pygame

class Events():
    lookUp = {}

    @staticmethod
    def getEvent(name):
        event = None
        if name in Events.lookUp.keys():
            event = Events.lookUp[name]

        return event

    class Event():
        #Base class for events
        def __init__(self):
            if not self.name:
                self.name = "Generic Event"

            Events.lookUp[self.name] = self

    class TickEvent(Event):
        def __init__(self):
            self.name = "Game Tick Event"
            super().__init__()

    class NewGameEvent(Event):
        def __init__(self):
            self.name = "New Game Event"
            super().__init__()

    class QuitEvent(Event):
        def __init__(self):
            self.name = "Program Quit Event"
            super().__init__()

    class ShowOptionsEvent(Event):
        def __init__(self):
            self.name = "Show Options Event"
            super().__init__()

    class CollisionEvent(Event):
        """..."""
        def __init__(self, obj = None):
            self.name = "Collision Event"
            self.obj = obj
            super().__init__()

    class HoverWidgetEvent(Event):
        """..."""
        def __init__(self, pos = None):
            self.name = "Widget Mouse Hover Event"
            self.pos = pos
            super().__init__()

    class DragWidgetEvent(Event):
        """..."""
        def __init__(self, pos = None):
            self.name = "Widget Mouse Drag Event"
            self.pos = pos
            super().__init__()

    class KeyboardActivateWidgetEvent(Event):
        """..."""
        def __init__(self, widget):
            self.name = "Keyboard Activate Widget Event"
            self.widget = widget
            super().__init__()

    class LeftClickWidgetEvent(Event):
        """..."""
        def __init__(self, pos = None):
            self.name = "Widget Left Click Event"
            self.pos = pos
            super().__init__()

    class MiddleClickWidgetEvent(Event):
        """..."""
        def __init__(self, pos = None):
            self.name = "Widget Middle Click Event"
            self.pos = pos
            super().__init__()

    class RightClickWidgetEvent(Event):
        """..."""
        def __init__(self, pos = None):
            self.name = "Widget Right Click Event"
            self.pos = pos
            super().__init__()

class EventManager:
    #Used to decouple event handling from interface generation
    def __init__(self):
        self.events = {}
        self.running = True

    def getListeners(self):
        listeners = {}

        #loop through and get all listeners
        for event in self.events:
            for listener in self.events[event]:
                if listener not in listeners.keys():
                    listeners[listener] = []

        #loop through again to add events
        for event in self.events:
            for listener in self.events[event]:
                if listener in listeners.keys():
                    listeners[listener].append(event)

        return listeners

    def addListener(self, event, listener):
        type = event.name
        if not type in self.events.keys():
            self.events[type] = []

        if not listener in self.events[type]: #no sense in adding it twice
            self.events[type].append(listener)

    def removeListener(self, event, listener):
        type = event.name
        if type in self.events.keys():
            if listener in self.events[type]:
                self.events[type].remove(listener)

    def post(self, event):
        type = event.name
        if type in self.events.keys():
            for listener in self.events[type]:
                listener.notify(event)

    def processEvents(self):
        event = None
        while self.running:
            event = Events.TickEvent()
            self.post(event)

            pygame.event.pump()
            for e in pygame.event.get():

                if e.type ==  pygame.MOUSEMOTION:
                    event = Events.HoverWidgetEvent(e.pos)
                    self.post(event)
##
##				  if e.type ==  pygame.KEYDOWN:
##
##				  if e.type ==  pygame.KEYUP:


                if e.type == pygame.MOUSEBUTTONUP:
                    if e.button == 1:
                        event = Events.LeftClickWidgetEvent(e.pos)
                        self.post(event)
                    if e.button == 2:
                        event = Events.MiddleClickWidgetEvent(e.pos)
                        self.post(event)
                    if e.button == 3:
                        event = Events.RightClickWidgetEvent(e.pos)
                        self.post(event)

                if e.type == pygame.QUIT:
                    event = Events.QuitEvent()
                    self.post(event)
