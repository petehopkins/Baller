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

    class CollisionEvent(Event):
        def __init__(self, obj = None):
            self.name = "Collision Event"
            self.obj = obj
            super().__init__()

    class PaddleMoveEvent(Event):
        def __init__(self, pos = None):
            self.name = "Paddle Move Event"
            self.pos = pos
            super().__init__()

    class HoverWidgetEvent(Event):
        def __init__(self, pos = None):
            self.name = "Widget Mouse Hover Event"
            self.pos = pos
            super().__init__()

    class DragWidgetEvent(Event):
        def __init__(self, pos = None):
            self.name = "Widget Mouse Drag Event"
            self.pos = pos
            super().__init__()

    class KeyboardActivateWidgetEvent(Event):
        def __init__(self, keys):
            self.name = "Keyboard Activate Widget Event"
            self.keys = keys
            super().__init__()

    class LeftClickWidgetEvent(Event):
        def __init__(self, pos = None):
            self.name = "Widget Left Click Event"
            self.pos = pos
            super().__init__()

    class MiddleClickWidgetEvent(Event):
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

    class ActivateScreenEvent(Event):
        def __init__(self):
            self.name = "Activate Screen Event"
            super().__init__()

    class NewGameEvent(Event):
        def __init__(self):
            self.name = "New Game Event"
            super().__init__()

    class ShowOptionsEvent(Event):
        def __init__(self):
            self.name = "Show Options Event"
            super().__init__()

    class QuitEvent(Event):
        def __init__(self):
            self.name = "Program Quit Event"
            super().__init__()

    class ApplyOptionsEvent(Event):
        def __init__(self):
            self.name = "Save Options Event"
            super().__init__()

    class ResetValuesToDefaultsEvent(Event):
        def __init__(self):
            self.name = "Reset Values To Defaults Event"
            super().__init__()

    class CancelOptionsEvent(Event):
        def __init__(self):
            self.name = "Cancel Options Event"
            super().__init__()

    class PauseGameEvent(Event):
        def __init__(self):
            self.name = "Pause Game Event"
            super().__init__()

class EventManager:
    #Used to decouple event handling from interface generation
    def __init__(self, game):
        self.events = {}
        self.running = True
        self.game = game

    def getListeners(self):
        # Listeners are stored as the value part of a key/value dictionary where events are used as keys.
        # This method reverses that mapping, returning a dictionary where the listener is the key and the
        # events it's registered for are stored as the value.
        listeners = {}

        #loop through all events and add all listeners as the key part of a dictionary
        for event in self.events:
            for listener in self.events[event]:
                if listener not in listeners.keys():
                    listeners[listener] = [] #store an empty list for now

        #loop through again to add events. Could probably refactor this to use the same loop as above,
        #but the extra time taken to loop through again here is trivial and this is more readable.
        for event in self.events:
            for listener in self.events[event]:
                if listener in listeners.keys():
                    listeners[listener].append(event)

        return listeners

    def addListener(self, event, listener):
        eventName = event.name
        if not eventName in self.events.keys():
            self.events[eventName] = []

        if not listener in self.events[eventName]: #no sense in adding it twice
            self.events[eventName].append(listener)

    def removeListener(self, event, listener):
        eventName = event.name
        if eventName in self.events.keys():
            if listener in self.events[eventName]:
                self.events[eventName].remove(listener)

    def post(self, event):
        eventName = event.name
        if eventName in self.events.keys():
            for listener in self.events[eventName]:
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

                    event = Events.PaddleMoveEvent(e.pos)
                    self.post(event)

                    if e.buttons[0] == 1:
                        event = Events.DragWidgetEvent(e.pos)
                        self.post(event)

                if e.type == pygame.KEYDOWN:
                    #e.unicode, e.key, e.mod
                    pass

                if e.type ==  pygame.KEYUP:
                    #e.key, e.mod
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_p:
                        event = Events.PauseGameEvent()
                        self.post(event)

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
