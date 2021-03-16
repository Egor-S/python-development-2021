import tkinter as tk


class LabelInput(tk.Label):
    def __init__(self, master, **kwargs):
        default_kwargs = dict(takefocus=1, highlightthickness=1)
        default_kwargs.update(kwargs)
        super().__init__(master, **default_kwargs)
        self.bind('<Any-Key>', self._on_any_key)
        self._pos = len(self['text'])

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
            if self._pos > 1:
                self._pos -= 1
        elif ev.keysym == 'Right':
            if self._pos < len(text):
                self._pos += 1
        elif ev.keysym == 'Home':
            self._pos = 0
        elif ev.keysym == 'End':
            self._pos = len(text)
        elif ev.char.isprintable():
            self.configure(text=text[:self._pos] + ev.char + text[self._pos:])
            self._pos += 1
        

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
        self.entry = LabelInput(self, text='123')
        self.entry.grid(row=0, sticky='NWE')
        self.quit = tk.Button(self, text='Quit', command=self.quit)
        self.quit.grid(row=1, sticky='ES')


def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
