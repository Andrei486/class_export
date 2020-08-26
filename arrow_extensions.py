import arrow
from dateutil.tz import tzlocal
from datetime import datetime

def parse_date(date: str) -> arrow.Arrow:
    return arrow.get(date, "MMM DD, YYYY")

def parse_time(time: str) -> arrow.Arrow:
    return arrow.get(time, "h:mm a")

def combine_date_time(date: arrow.Arrow, time: arrow.Arrow) -> arrow.Arrow:
    """
    Returns an Arrow object with the date of the first argument and the time of the second.
    """
    return date.shift(hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond)

def shift_timezone(date: arrow.Arrow) -> arrow.Arrow:
    shifted = date.naive - datetime.now(tzlocal()).utcoffset()
    return arrow.get(shifted)

def get_weekday_after(date: arrow.Arrow, iso_weekday: int) -> arrow.Arrow:
    """
    Returns the first day with the given weekday that is equal to or greater than
    the given date.
    """
    new_date = date.shift(weekday=iso_weekday - 1)
    return new_date

if __name__ == "__main__":
    date = arrow.Arrow(2020, 9, 9)
    print(shift_timezone(date))