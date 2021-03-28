import tkinter as tk
from tkinter import colorchooser


class Application(tk.Frame):
    '''Sample tkinter application class'''

    def __init__(self, master=None, title="<application>", **kwargs):
        '''Create root window with frame, tune weight and resize'''
        super().__init__(master, **kwargs)
        self.master.title(title)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.grid(sticky="NEWS")
        self.create_widgets()
        self.configure_widgets()

    def create_widgets(self):
        '''Create all the widgets'''

    def configure_widgets(self):
        for column in range(self.grid_size()[0]):
            self.columnconfigure(column, weight=1)
        for row in range(self.grid_size()[1]):
            self.rowconfigure(row, weight=1)


class GraphEdit(Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.figures = []
        self.ink_color = 'black'
        self.fill_color = 'green'
        self.active_figure = None
        self.start_point = None
        self.mode = None  # 'create' or 'move'

    def create_widgets(self):
        self.edit_frame = tk.LabelFrame(self, text="<Untitled>")
        self.edit_frame.grid(row=0, column=0, sticky='NEWS')
        self.T = tk.Text(self.edit_frame, undo=True, wrap=tk.WORD, font='fixed', inactiveselectbackground="MidnightBlue")
        self.T.grid(row=0, column=0, sticky='NEWS')
        
        self.file_controls = tk.Frame(self)
        self.file_controls.grid(row=1, column=0, sticky='NEWS')
        self.load = tk.Button(self.file_controls, text='Load')  # todo command
        self.load.grid(row=0, column=0)
        self.save = tk.Button(self.file_controls, text='Save')  # todo command
        self.save.grid(row=0, column=1)

        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.grid(row=0, column=1, sticky='NEWS')
        self.canvas_controls = tk.Frame(self.canvas_frame)
        self.canvas_controls.grid(row=0, column=0, sticky='NEWS')
        
        self.ink = tk.Button(self.canvas_controls, text='Ink', command=self.ask_ink_color)
        self.ink.grid(row=0, column=0)
        self.width = tk.StringVar()
        self.width.set('1.1')
        self.width_box = tk.Spinbox(self.canvas_controls, from_=0.0, to=10.0, textvariable=self.width)  # todo command
        self.width_box.grid(row=0, column=1)
        self.fill = tk.Button(self.canvas_controls, text='Fill', command=self.ask_fill_color)
        self.fill.grid(row=0, column=2)
        self.P = tk.Label(self.canvas_controls, text='0:0')
        self.P.grid(row=0, column=4)
        
        self.C = tk.Canvas(self.canvas_frame, bg='red')
        self.C.grid(row=1, column=0, sticky='NEWS')
        self.C.bind('<Motion>', self.canvas_on_mouse_move)
        self.C.bind('<Button>', self.canvas_on_mouse_press)
        self.C.bind('<ButtonRelease>', self.canvas_on_mouse_release)
        
        self.quit_controls = tk.Frame(self)
        self.quit_controls.grid(row=1, column=1, sticky='NEWS')
        self.quit = tk.Button(self.quit_controls, text='Quit', command=self.master.quit)
        self.quit.grid(sticky='E')

    def configure_widgets(self):
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform='tabs')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)  # disable bottom controls stretch
        
        self.edit_frame.columnconfigure(0, weight=1)
        self.edit_frame.rowconfigure(0, weight=1)

        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(1, weight=1)

    def ask_ink_color(self):
        c = colorchooser.askcolor(color=self.ink_color)
        print(c)
        if c is not None:
            self.ink_color = c[1]

    def ask_fill_color(self):
        c = colorchooser.askcolor(color=self.fill_color)
        if c is not None:
            self.fill_color = c[1]

    def canvas_on_mouse_move(self, ev):
        self.P.config(text=f'{ev.x}:{ev.y}')
        if self.mode == 'create':
            x0, x1 = sorted((ev.x, self.start_point[0]))
            y0, y1 = sorted((ev.y, self.start_point[1]))
            self.C.coords(self.active_figure, x0, y0, x1, y1)
        elif self.mode == 'move':
            x, y = self.start_point
            self.C.move(self.active_figure, ev.x - x, ev.y - y)
            self.start_point = (ev.x, ev.y)

    def figure_on_mouse_press(self, ev):
        self.mode = 'move'
        self.start_point = (ev.x, ev.y)
        self.active_figure = self.C.find_closest(*self.start_point)[0]

    def canvas_on_mouse_press(self, ev):
        if self.mode == 'move':
            return
        self.mode = 'create'
        self.start_point = (ev.x, ev.y)
        self.active_figure = self.C.create_oval(
            *self.start_point, *self.start_point, width=float(self.width.get()),
            outline=self.ink_color, fill=self.fill_color
        )
        self.C.tag_bind(self.active_figure, '<Button>', self.figure_on_mouse_press)
        self.figures.append(self.active_figure)

    def canvas_on_mouse_release(self, ev):
        self.mode = None
        self.active_figure = None
        self.start_point = None


def main():
    app = GraphEdit(title="Graph Edit")
    app.mainloop()


if __name__ == '__main__':
    main()
