import tkinter as tk


tk_NESW = tk.N + tk.E + tk.S + tk.W


class FifteenGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid(sticky=tk_NESW)
        self.map = [
            0, 1, 2, None,
            4, 5, 6, 3,
            8, 9, 10, 7,
            12, 13, 14, 11
        ]
        self.create_widgets()


    def create_widgets(self):
        self.new_button = tk.Button(self, text='New')
        self.new_button.grid(row=0, column=0, columnspan=2)
        self.quit_button = tk.Button(self, text='Exit', command=self.quit)
        self.quit_button.grid(row=0, column=2, columnspan=2)
        self.numeric_buttons = []
        for i in range(15):
            btn = tk.Button(self, text='{}'.format(i + 1), command=self.create_callback(i))
            self.numeric_buttons.append(btn)
        self.grid_numeric_buttons()

        # resizable grid
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        for i in range(4):
            self.rowconfigure(i + 1, weight=1)
            self.columnconfigure(i, weight=1)

    def grid_numeric_buttons(self):
        for i, n in enumerate(self.map):
            if n is not None:
                self.numeric_buttons[n].grid(row=i // 4 + 1, column=i % 4, sticky=tk_NESW)

    def create_callback(self, n):
        def callback():
            print(self.map.index(n))
        return callback


def main():
    game = FifteenGame()
    game.master.title("15")
    game.master.geometry("300x300")
    game.mainloop()



if __name__ == '__main__':
    main()
