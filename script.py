from typing import Set, List
import bs4
from bs4 import BeautifulSoup
import arrow
import re
from recurrent_ics import RecurrentEvent, Event, Calendar
from arrow_extensions import parse_date, parse_time, get_weekday_after, shift_timezone, combine_date_time

ISO_WEEKDAY = {"M": 1, "T": 2, "W": 3, "R": 4, "F": 5, "S": 6, "U": 7}

class Course():
    def __init__(self):
        pass

    def set_course_info(self, course_detail: bs4.Tag) -> None:
        """
        Set this object's general info properties
        from the course_detail table tag.
        """
        rows = course_detail.find("tbody").find_all("tr")
        self.name = rows[0].select("th a")[0].get_text()
        return
    
    def set_schedule_info(self, schedule_detail: bs4.Tag) -> None:
        """
        Set this object's scheduling info properties
        from the schedule_detail table tag.
        """
        self.unscheduled = False
        info = schedule_detail.find("tbody").select("tr:nth-of-type(2)")[0].find_all("td")
        times = re.search(string=info[1].get_text(), pattern=r"([0-9]{1,2}:[0-9]{2} [a,p]m) - ([0-9]{1,2}:[0-9]{2} [a,p]m)")
        if times:
            times = times.groups()
        else:
            self.unscheduled = True
            return
        self.weekdays = [ISO_WEEKDAY[letter] for letter in info[2].get_text()]
        date_range = re.search(string=info[4].get_text(), pattern=r"([A-z]{3} [0-9]{2}, [0-9]{4}) - ([A-z]{3} [0-9]{2}, [0-9]{4})").groups()
        first_day = parse_date(date_range[0])
        self.last_day = shift_timezone(parse_date(date_range[1]).shift(days=1)) # Shift one day later: classes CAN occur on the last day
        start_time = parse_time(times[0])
        end_time = parse_time(times[1])
        self.starts = []
        self.ends = []
        shift = 0
        for weekday in self.weekdays:
            first_occurrence = get_weekday_after(first_day, weekday)
            start = shift_timezone(combine_date_time(first_occurrence, start_time))
            if start.weekday() + 1 > weekday or weekday == 7 and start.weekday() + 1 < 7:
                shift = 1
            elif start.weekday() + 1 < weekday or weekday == 1 and start.weekday() + 1 > 1:
                shift = -1
            self.starts.append(start)
            end = shift_timezone(combine_date_time(first_occurrence, end_time))
            self.ends.append(end)
        if shift:
            print(start.weekday(), weekday)
            print(shift)
            for i in range(len(self.weekdays)):
                self.weekdays[i] = (self.weekdays[i] + shift - 1) % 7 + 1

        self.location = info[3].get_text()

    
    def to_event(self) -> Event:
        if self.unscheduled:
            return None
        
        min_start_index = 0
        for i in range(len(self.starts)):
            if self.starts[i] < self.starts[min_start_index]:
                min_start_index = i
        
        evt = RecurrentEvent(name=self.name, \
            begin=self.starts[min_start_index], end=self.ends[min_start_index],
            location=self.location,
            created=arrow.utcnow(), last_modified=arrow.utcnow(),
            recurrent="WEEKLY", recurrence_weekdays=self.weekdays,
            recurrence_end=self.last_day)
        return evt

def load_document(filepath: str) -> BeautifulSoup:
    """
    Loads the HTML document contained at filepath into a BeautifulSoup object.
    Returns the BeautifulSoup object.
    """
    with open(filepath, "r") as f:
        document = BeautifulSoup(f.read(), features="html5lib")
        f.close()
    return document

def get_courses(document: BeautifulSoup) -> List[Course]:
    """
    Returns the list of courses with data in the HTML page document.
    """
    body = document.find("div", class_="pagebodydiv", role="main", recursive=True)
    courses = []
    schedule_detail_table = False
    for table in body.find_all("table", class_="datadisplaytable"):
        if not schedule_detail_table:
            obj = Course()
            obj.set_course_info(table)
            courses.append(obj)
        else:
            courses[-1].set_schedule_info(table)
        # General info tables and schedule info tables alternate.
        schedule_detail_table = not schedule_detail_table
    return courses

def make_calendar(courses: List[Course]) -> Calendar:
    """
    Returns a Calendar object containing all the course events in courses.
    """
    calendar = Calendar()
    for course in courses:
        evt = course.to_event()
        if evt:
            calendar.events.add(evt)
    return calendar

def calendar_from_filepath(filepath: str, output_path: str) -> None:
    doc = load_document(filepath)
    courses = get_courses(doc)
    calendar = make_calendar(courses)
    with open(output_path, "w") as f:
        f.writelines(calendar)
        f.close()

if __name__ == "__main__":
    filenames = ["Fall2019", "Winter2020", "Summer2020", "Fall2020", "Winter2021"]
    for filename in filenames:
        calendar_from_filepath(f"test/{filename}.html", f"output/{filename}.ics")