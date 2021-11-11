# import time

class Event(object):

    def __init__(self, description, date, time):
        self.description = description
        self.date = date
        self.time = time

    def getDescription(self):
        return self.description

    def getDate(self):
        return self.date

    def getMonth(self):
        month = self.date.split('-')
        return month[1]        

    def getDay(self):
        day = self.date.split('-')
        return day[2]

    def __str__(self):
        return self.description + "\n" + self.date + "\n" + self.time + "\n"

