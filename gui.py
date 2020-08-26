import tkinter as tk
from tkinter_common import FileSelector
from script import calendar_from_filepath
from help_gui import HelpButtons
import logging, logconfig

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Export Carleton schedule")
        self.protocol("WM_DELETE_WINDOW", self.quit)
    
class MainWindow(tk.Frame):
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.document_selector = FileSelector(self, "Select saved HTML page", "html")
        self.document_selector.pack(fill=tk.BOTH, expand=True)
        self.output_selector = FileSelector(self, "Select output file", "ics")
        self.output_selector.pack(fill=tk.BOTH, expand=True)
        tk.Button(self, text='Create ICS file', command=self.activate).pack(fill=tk.BOTH)
        self.message = tk.Label(self, text="")
        self.message.pack(fill=tk.BOTH, expand=True)
        HelpButtons(self, app).pack(fill=tk.BOTH, expand=True)
    
    def activate(self):
        document_path = self.document_selector.get_filepath()
        output_path = self.output_selector.get_filepath()
        if document_path and output_path:
            try:
                calendar_from_filepath(document_path, output_path)
                self.show_message("Successfully created an ICS file.")
                logging.info("Successfully created an ICS file.")
            except Exception as e:
                self.show_message("Something went wrong.")
                logging.error(e)
            
        else:
            self.show_message("At least one file path is missing.")
            logging.info("At least one file path is missing.")
    
    def show_message(self, message: str):
        self.message.config(text=message)

def run():
    root = Application()
    MainWindow(root, root).pack(fill=tk.BOTH, expand=True)
    tk.mainloop()

if __name__ == "__main__":
    run()