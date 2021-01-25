import datetime
import requests
import icalendar
import ics
import re


class Event:
    def __init__(self, event: list):

        time = event[2].lstrip("DTSTART;TZID=Europe/Paris:")
        self.beginTime = datetime.datetime(year=int(time[0:4]), month=int(time[4:6]), day=int(time[6:8]),
                                           hour=int(time[9:11]),
                                           minute=int(time[11:13]), second=int(time[13:15]))
        time = event[3].lstrip("DTEND;TZID=Europe/Paris:")
        self.endTime = datetime.datetime(year=int(time[0:4]), month=int(time[4:6]), day=int(time[6:8]),
                                         hour=int(time[9:11]),
                                         minute=int(time[11:13]), second=int(time[13:15]))
        for i in event:
            if i.startswith("SUMMARY:"):
                self.name = i.lstrip("SUMMARY")


class Calendar:
    def getCalendar(self):
        r = requests.get(self.link)
        for event in re.findall(r'BEGIN:VEVENT\n((.|\n)*?)\nEND:VEVENT', r.text, re.MULTILINE):
            self.Calendar.append(Event(event[0].split('\n')))

        self.Calendar.sort(key=lambda x: x.beginTime)

    def __init__(self, name, link):
        self.Calendar = list()
        self.name = name
        self.link = link
        self.getCalendar()

    def __GetEventsOfDay(self, day: datetime.datetime):
        i = 0
        result = list()
        while self.Calendar[i].beginTime.date() <= day.date():
            result.append(self.Calendar[i])
            i += 1
        return result

    def getClassOfTheDay(self):
        return self.__GetEventsOfDay(datetime.datetime.utcnow())

    def getClassOfTomorrow(self):
        return self.__GetEventsOfDay(datetime.datetime.utcnow() + datetime.timedelta(days=1))
