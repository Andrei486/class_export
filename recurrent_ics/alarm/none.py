from recurrent_ics.alarm.base import BaseAlarm

from recurrent_ics.serializers.alarm_serializer import NoneAlarmSerializer
from recurrent_ics.parsers.alarm_parser import NoneAlarmParser


class NoneAlarm(BaseAlarm):
    """
    A calendar event VALARM with NONE option.
    """

    class Meta:
        name = "VALARM"
        parser = NoneAlarmParser
        serializer = NoneAlarmSerializer

    @property
    def action(self):
        return "NONE"
