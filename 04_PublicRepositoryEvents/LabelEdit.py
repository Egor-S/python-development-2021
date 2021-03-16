import tkinter as tk
from tkinter import font


class LabelInput(tk.Label):
    def __init__(self, master, **kwargs):
        default_kwargs = dict(takefocus=1, highlightthickness=1)
        default_kwargs.update(kwargs)
        super().__init__(master, **default_kwargs)
        self.bind('<Any-Key>', self._on_any_key)
        self._pos = len(self['text'])
        self._cursor = tk.Frame(self, bg='black')
        self._x_shift = 4.5
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        self.bind('<Button-1>', self._on_mouse_click)

    def _on_any_key(self, ev):
        text = self['text']
        if ev.keysym == 'BackSpace':
            if self._pos > 0:
                self.configure(text=text[:self._pos - 1] + text[self._pos:])
                self._pos -= 1
        elif ev.keysym == 'Delete':
            if self._pos < len(text):
                self.configure(text=text[:self._pos] + text[self._pos + 1:])
        elif ev.keysym == 'Left':
            if self._pos > 0:
                self._pos -= 1
        elif ev.keysym == 'Right':
            if self._pos < len(text):
                self._pos += 1
        elif ev.keysym == 'Home':
            self._pos = 0
        elif ev.keysym == 'End':
            self._pos = len(text)
        elif ev.char and ev.char.isprintable():
            self.configure(text=text[:self._pos] + ev.char + text[self._pos:])
            self._pos += 1
        self._move_cursor()

    def _move_cursor(self):
        text = self['text']
        f = font.Font(font='TkDefaultFont')
        h = f.metrics('linespace')
        x = f.measure(text[:self._pos])
        self._cursor.place(x=x + self._x_shift, y=3, width=1, height=h + 2)

    def _on_focus_in(self, ev):
        self._move_cursor()

    def _on_focus_out(self, ev):
        self._cursor.place_forget()

    def _on_mouse_click(self, ev):
        self.focus_set()
        text = self['text']
        f = font.Font(font='TkDefaultFont')
        self._pos = 0
        while f.measure(text[:self._pos]) + self._x_shift + 2 < ev.x and self._pos < len(text):
            self._pos += 1
        self._move_cursor()


class Application(tk.Frame):
    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)

    def create_widgets(self):
        '''Create all the widgets'''
        self.entry = LabelInput(self, text='')
        self.entry.grid(row=0, sticky='NW')
        self.quit = tk.Button(self, text='Quit', command=self.quit)
        self.quit.grid(row=1, sticky='ES')


def main():
    app = Application(title='Editable Label')
    app.mainloop()


if __name__ == '__main__':
    main()
