import tkinter as tk
from tkinter_common import ToggledFrame

class HelpButtons(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        tk.Button(self, text="How to get the HTML page", command=self.get_html_page_help).pack(fill=tk.X, expand=True)
        tk.Button(self, text="What filepaths to select", command=self.get_filepath_help).pack(fill=tk.X, expand=True)
    
    def get_html_page_help(self):
        window = tk.Toplevel(self.app)
        tk.Label(window, text=
        """
        Login to Carleton Central, then navigate to Student Timetable -> Detail Schedule.
        Select the term for which you wish to export your courses, then save the page
        (Ctrl+S on Windows) as a complete webpage. This will download an HTML file
        along with a folder: provide the HTML file's path to the HTML page field.
        """).pack(fill=tk.BOTH)
    
    def get_filepath_help(self):
        window = tk.Toplevel(self.app)
        tk.Label(window, text=
        """
        For help with downloading the HTML page, see "How to get the HTML page". Provide the filepath of the HTML file
        (not the folder!) that you download when following those steps.
        For the output file, create a file with a .ics extension at a location on your computer. Provide the path
        to this file as an output file. WARNING: this will overwrite any pre-existing file with that name!
        You can also manually enter a path to a file that does not exist. Doing so will create a file at that location
        (so long as the path is valid).
        """).pack(fill=tk.BOTH)
