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
            pos = self.map.index(n)
            try:
                t_pos = self.test_move(pos)
                self.map[pos], self.map[t_pos] = self.map[t_pos], self.map[pos]  # swap numbers
                self.numeric_buttons[n].grid(row=t_pos // 4 + 1, column=t_pos % 4, sticky=tk_NESW)
            except IndexError as e:
                pass
        return callback

    def test_move(self, pos):
        x, y = pos % 4, pos // 4
        if x > 0 and self.map[pos - 1] is None:
            return pos - 1
        if x < 3 and self.map[pos + 1] is None:
            return pos + 1
        if y > 0 and self.map[pos - 4] is None:
            return pos - 4
        if y < 3 and self.map[pos + 4] is None:
            return pos + 4
        raise IndexError("No possible moves")



def main():
    game = FifteenGame()
    game.master.title("15")
    game.master.geometry("300x300")
    game.mainloop()



if __name__ == '__main__':
    main()
