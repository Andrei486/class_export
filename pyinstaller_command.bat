pyinstaller --onefile --nowindow^
    --add-data="wingicon.ico;." ^
    --add-data="recurrent_ics/grammar/contentline.ebnf;recurrent_ics/grammar/"^
    --icon=wingicon.ico ^
    Course_Export.py