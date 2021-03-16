import re
import tkinter as tk
from tkinter.messagebox import showinfo


def parse_geometry(geometry):
    g = re.match(r"(?P<r>\d+)(?:\.(?P<rw>\d+))?(?:\+(?P<rs>\d+))?:(?P<c>\d+)(?:\.(?P<cw>\d+))?(?:\+(?P<cs>\d+))?(?:\/(?P<s>\w+))?", geometry).groupdict()
    return {
        key: func(default if g[key] is None else g[key])
        for key, (default, func)
        in {'r': (None, int), 'rw': (1, int), 'rs': (0, int), 'c': (None, int), 'cw': (1, int), 'cs': (0, int), 's': ('NEWS', str)}.items()
    }


def widget_constructor(attr, master):
    def wrapper(widget, geometry, **kwargs):
        g = parse_geometry(geometry)
        class VirtualWidget(widget):
            def __init__(self):
                super().__init__(master, **kwargs)
                self.grid(row=g['r'], column=g['c'], rowspan=1 + g['rs'], columnspan=1 + g['cs'], sticky=g['s'])
                self.master.columnconfigure(g['c'], weight=g['cw'])
                self.master.rowconfigure(g['r'], weight=g['rw'])

            def __getattr__(self, attr2):
                return widget_constructor(attr2, self)
        print('create widget', attr)
        setattr(master, attr, VirtualWidget())
    return wrapper


class Application(tk.Frame):
    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.createWidgets()

    def __getattr__(self, attr):
        print('query', attr)
        return widget_constructor(attr, self)
        


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()
