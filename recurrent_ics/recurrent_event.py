import copy
from datetime import datetime, timedelta
from typing import (Dict, Iterable, List, NamedTuple, Optional, Set,
                    Tuple, Union)

from arrow import Arrow

from .alarm.base import BaseAlarm
from .attendee import Attendee, Organizer
from .component import Component
from recurrent_ics.grammar.parse import Container
from .types import ArrowLike
from .utils import (get_arrow, uid_gen)
from recurrent_ics.parsers.event_parser import EventParser
from recurrent_ics.serializers.recurrent_event_serializer import RecurrentEventSerializer
from recurrent_ics.event import Event

RECURRENCE_TYPES = {"HOURLY", "DAILY", "WEEKLY", "MONTHLY", "YEARLY"}
WEEKDAY_CODES = {1: "MO", 2: "TU", 3: "WE", 4: "TH", 5: "FR", 6: "SA", 7: "SU"}

class RecurrentEvent(Event):

    class Meta:
        name = "VEVENT"
        parser = EventParser
        serializer = RecurrentEventSerializer
    
    def __init__(self,
                 name: str = None,
                 begin: ArrowLike = None,
                 end: ArrowLike = None,
                 duration: timedelta = None,
                 uid: str = None,
                 description: str = None,
                 created: ArrowLike = None,
                 last_modified: ArrowLike = None,
                 location: str = None,
                 url: str = None,
                 transparent: bool = None,
                 alarms: Iterable[BaseAlarm] = None,
                 attendees: Iterable[Attendee] = None,
                 categories: Iterable[str] = None,
                 status: str = None,
                 organizer: Organizer = None,
                 geo=None,
                 classification: str = None,
                 recurrent: str = 0,
                 recurrence_weekdays: List[Union[str, int]] = [], # Accepts ISO weekdays or ICS weekday codes.
                 recurrence_count: int = 0,
                 recurrence_end: ArrowLike = None,
                 recurrence_interval: int = 1
                 ) -> None:

        """Instantiates a new :class:`recurrent_ics.event.Event`.

        Args:
            name: rfc5545 SUMMARY property
            begin (Arrow-compatible)
            end (Arrow-compatible)
            duration
            uid: must be unique
            description
            created (Arrow-compatible)
            last_modified (Arrow-compatible)
            location
            url
            transparent
            alarms
            attendees
            categories
            status
            organizer
            classification
            recurrent: must be one of HOURLY, DAILY, WEEKLY, MONTHLY, or YEARLY
            recurrence_weekdays: either listed as ISO weekdays or ICS weekday codes
            recurrence_count
            recurrence_end (Arrow-compatible)
            recurrence_interval

        Raises:
            ValueError: if `end` and `duration` are specified at the same time
            ValueError: if `recurrence_count` and `recurrence_end` are specified at the same time
        """

        super().__init__(name, begin, end, duration, uid, description, created, last_modified, location, 
                       url, transparent, alarms, attendees, categories, status, organizer, geo, classification)

        self._recurrence_count: Optional[int] = None
        self._recurrence_end: Optional[ArrowLike] = None

        self.recurrent = recurrent if recurrent in RECURRENCE_TYPES else None

        if not recurrent:
            return
        
        self.recurrence_weekdays = []
        for weekday in recurrence_weekdays:
            if isinstance(weekday, str):
                self.recurrence_weekdays.append(weekday)
            elif isinstance(weekday, int):
                self.recurrence_weekdays.append(WEEKDAY_CODES[weekday])
        
        if recurrence_count and recurrence_end:
            raise ValueError(
                'RecurrentEvent() may not specify an recurrence count and a \
                recurrence end date at the same time')
        elif recurrence_count:
            self.recurrence_count = recurrence_count
        else:
            self.recurrence_end = recurrence_end
        
        self.recurrence_interval = recurrence_interval if recurrence_interval >= 1 else 1
        
    @property
    def recurrence_end(self) -> Arrow:
        """Get or set the last day for the event's recurrence.

        |  Will return an :class:`Arrow` object.
        |  May be set to anything that :func:`Arrow.get` understands.
        """
        return self._recurrence_end
    
    @recurrence_end.setter
    def recurrence_end(self, value: ArrowLike):
        value = get_arrow(value)
        self._recurrence_end = value
        self._recurrence_count = None
    
    @property
    def recurrence_count(self) -> int:
        """Get or set the number of instances for this event's recurrence.

        |  Will return an `int`.
        |  May be set to anything that `int` can convert.
        """
        return self._recurrence_count
    
    @recurrence_count.setter
    def recurrence_count(self, value):
        value = int(value)
        self._recurrence_count = value
        self._recurrence_end = None
        