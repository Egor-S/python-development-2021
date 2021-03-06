import tkinter as tk


class FifteenGame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.buttons = []
        self.grid(sticky=tk.N+tk.E+tk.S+tk.W)
        self.create_widgets()


    def create_widgets(self):
        self.new_button = tk.Button(self, text='New')
        self.new_button.grid(row=0, column=0, columnspan=2)
        self.quit_button = tk.Button(self, text='Exit', command=self.quit)
        self.quit_button.grid(row=0, column=2, columnspan=2)
        for i in range(15):
            self.buttons.append(tk.Button(self, text='{}'.format(i + 1)))
            self.buttons[-1].grid(row=i // 4 + 1, column=i % 4, sticky=tk.N+tk.E+tk.S+tk.W)

        # resizable grid
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        for i in range(4):
            self.rowconfigure(i + 1, weight=1)
            self.columnconfigure(i, weight=1)


def main():
    game = FifteenGame()
    game.master.title("15")
    game.master.geometry("300x300")
    game.mainloop()



if __name__ == '__main__':
    main()
