# class_export
## v1.0
 An executable that allows for Carleton University course schedules to be exported as ICS calendar files.

## Use
 Download and run the executable `Course_Export.exe` found under `dist`. The executable provides some help on using it.
 The executable will produce an ICS file which can then be imported into Google Calendar (https://support.google.com/calendar/answer/37118?co=GENIE.Platform%3DDesktop&hl=en) or other calendar applications.

## Development Notice
 This project uses a package `recurrent_ics`, largely based on the `ics` package (https://pypi.org/project/ics/). This package is meant to provide very limited functionality related to recurring events, that is missing in the current release of `ics`. The `recurrent_ics` package can be attributed to the developers of the `ics` package: this project claims no rights to any of the code in the package.

## History
- v1.0, Aug 25 2020: Initial release