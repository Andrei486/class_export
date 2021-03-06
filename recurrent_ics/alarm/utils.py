from recurrent_ics.alarm.audio import AudioAlarm
from recurrent_ics.alarm.none import NoneAlarm
from recurrent_ics.alarm.custom import CustomAlarm
from recurrent_ics.alarm.display import DisplayAlarm
from recurrent_ics.alarm.email import EmailAlarm
from recurrent_ics.utils import get_lines


def get_type_from_action(action_type):
    if action_type == "DISPLAY":
        return DisplayAlarm
    elif action_type == "AUDIO":
        return AudioAlarm
    elif action_type == "NONE":
        return NoneAlarm
    elif action_type == 'EMAIL':
        return EmailAlarm
    else:
        return CustomAlarm


def get_type_from_container(container):
    action_type_lines = get_lines(container, "ACTION", keep=True)
    if len(action_type_lines) > 1:
        raise ValueError("Too many ACTION parameters in VALARM")

    action_type = action_type_lines[0]
    return get_type_from_action(action_type.value)
