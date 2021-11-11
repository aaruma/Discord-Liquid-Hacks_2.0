from event import Event

class Calendar():
    
    events = []
    eventNum = 0

    def __init__(self, name):
        self.name = name

    def addEvent(self, Event):

        self.eventNum += 1
        self.events.append(Event)

    def getEvents(self):
        
        return self.events
    
    def __str__(self):
        n = ""
        for event in self.events:
            n += str(event) + " "
        return n

