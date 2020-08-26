from recurrent_ics.attendee import Attendee, Organizer
from recurrent_ics.grammar.parse import ContentLine
from recurrent_ics.serializers.serializer import Serializer
from recurrent_ics.utils import (arrow_date_to_iso, arrow_to_iso, escape_string,
                       timedelta_to_duration, uid_gen)
from recurrent_ics.serializers.event_serializer import EventSerializer

class RecurrentEventSerializer(EventSerializer):
    def serialize_recurrent(event, container):
        if event.recurrent:
            params = {
                "FREQ": event.recurrent,
                "BYDAY": ",".join(event.recurrence_weekdays),
                "INTERVAL": str(event.recurrence_interval)
            }
            if event.recurrence_count:
                params["COUNT"] = event.recurrence_count
            if event.recurrence_end:
                params["UNTIL"] = arrow_to_iso(event.recurrence_end)

            container.append(ContentLine("RRULE", value=parse_rrule_dict(params)))
    
def parse_rrule_dict(rrule) -> str:
    output = []
    for key in rrule:
        output.append(f"{key}={rrule[key]}")
    return ";".join(output)