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

            Events.lookUp[self.name] = self # register name in the lookup table

    class TickEvent(Event):
        def __init__(self):
            self.name = "Game Tick Event"
            super().__init__() # ensure name is registered in the lookup table

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

    class StatUpdateEvent(Event):
        def __init__(self, stat = None, value = None):
            self.name = "Stat Update Event"
            self.stat = stat
            self.value = value
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

    class ShowStartEvent(Event):
        def __init__(self):
            self.name = "Show Start Event"
            super().__init__()

    class NewGameEvent(Event):
        def __init__(self):
            self.name = "New Game Event"
            super().__init__()

    class LowerVolumeEvent(Event):
        def __init__(self):
            self.name = "Lower Volume Event"
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

    class UnpauseGameEvent(Event):
        def __init__(self):
            self.name = "Unpause Game Event"
            super().__init__()

    class GameOverEvent(Event):
        def __init__(self):
            self.name = "Game Over Event"
            super().__init__()

    class LevelCompleteEvent(Event):
        def __init__(self):
            self.name = "Level Complete Event"
            super().__init__()

# The definition of the Singleton metaclass below was taken from:
#    http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
#
# The method used is listed as (at the time of this writing): Method 3
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

class EventManager(metaclass = Singleton):
    __sealed = False
    game = None

    #Used to decouple event handling from interface generation
    def __init__(self, game = None):
        if not self.__sealed:
            self.events = {}
            self.running = True
            self.game = game
            self.__sealed = True

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

    def __printListeners(self, event): # used for debugging
        if event in self.events.keys():
            for listener in self.events[event]:
                print(listener.text, "is registered for", event)

    def removeListeners(self, widget):
        listeners = self.getListeners()
        if widget in listeners.keys():
            for event in listeners[widget]:
                e = Events.getEvent(event)
                self.removeListener(e, widget)

        #self.game.sleep(2) # IMPORTANT! Leave this line here, otherwise pygame acts like it's multi-threaded which is an undesired behavior.

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

            pygame.event.pump() # per documentation: "you should call pygame.event.pump() to allow pygame to handle internal actions."
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
                        if self.game.activeScreen == "pause":
                            event = Events.CancelOptionsEvent()
                        else:
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
