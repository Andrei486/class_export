import tkinter as tk
from tkinter import ttk
import tkinter.filedialog

class FileSelector(tk.Frame):
    def __init__(self, parent, title: str, extension: str, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.filepath = tk.StringVar()
        frame = tk.Frame(self)
        tk.Label(frame, text=title).pack(fill=tk.X, expand=True, side=tk.LEFT)
        tk.Button(frame, text="Select File", command=(lambda: self.select_file(title, extension))).pack(fill=tk.X, expand=False, side=tk.RIGHT)
        self.entry = tk.Entry(frame, textvariable=self.filepath)
        self.entry.pack(fill=tk.X, expand=False, side=tk.RIGHT)
        frame.pack(fill=tk.BOTH, expand=True)
    
    def get_filepath(self) -> str:
        return self.filepath.get()
    
    def select_file(self, title: str, extension: str) -> None:
        window = tk.Toplevel()
        window.withdraw()

        path = tkinter.filedialog.askopenfilename(title=title, filetypes=(("{0} files".format(extension),"*.{0}".format(extension)),("all files","*.*")))

        window.destroy()
        self.entry.delete(0, tk.END)
        self.entry.insert(0, path)
        return

class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)
        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill=tk.X, expand=True)

        ttk.Label(self.title_frame, text=text).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show)
        self.toggle_button.pack(side=tk.LEFT)

        self.sub_frame = ttk.Frame(self)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill=tk.X, expand=True)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')
