import tkinter

from domain import GameEndedError, IllegalPlayError, NoHistoryError, RewritableTTT


class Interface(tkinter.Tk):
    
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Rewritable Tic-Tac-Toe")
        self.__init_assets()
        self.__init_menu()
        self.__init_turn_info()
        self.__init_error_info()
        self.__init_playing_grid()
        self.__init_back_arrow()
        self.__init_forward_arrow()
        self.__init_history_info()
        self.__reset()
    
    def __init_assets(self):
        self.__blank = tkinter.PhotoImage(file="assets/blank.png")
        self.__blue = tkinter.PhotoImage(file="assets/blue.png")
        #self.__blue_locked = tkinter.PhotoImage(file="blue_locked.png")
        self.__red = tkinter.PhotoImage(file="assets/red.png")
        #self.__red_locked = tkinter.PhotoImage(file="red_locked.png")
        self.__back_icon = tkinter.PhotoImage(file="assets/back.png")
        self.__forward_icon = tkinter.PhotoImage(file="assets/forward.png")
    
    def __init_menu(self):
        self.__menu = tkinter.Menu(self)
        self.__game_menu = tkinter.Menu(self.__menu)
        self.__game_menu.add_command(label="Reset", command=self.__reset)
        self.__game_menu.add_command(label="Undo", command=self.__undo)
        self.__game_menu.add_command(label="Undo to Here", command=self.__undo_here)
        self.__menu.add_cascade(label="Game", menu=self.__game_menu)
        self.config(menu=self.__menu)
    
    def __init_turn_info(self):
        self.__turn_var = tkinter.StringVar()
        self.__turn_info = tkinter.Label(
            self, fg="white", textvariable=self.__turn_var
        )
        self.__turn_info.grid(row=0, column=0, columnspan=5)
    
    def __init_error_info(self):
        self.__error_var = tkinter.StringVar()
        self.__error_info = tkinter.Label(
            self, fg="white", textvariable=self.__error_var
        )
        self.__error_info.grid(row=1, column=0, columnspan=5)

    def __init_playing_grid(self):
        self.__playing_grid = []
        for i in range(9):
            button = tkinter.Button(
                self, command=self.__play(i), height=62, image=self.__blank,
                width=50
            )
            button.grid(row=(2 + i//3), column=(1 + i%3))
            self.__playing_grid.append(button)
    
    def __init_back_arrow(self):
        self.__back_arrow = tkinter.Button(
            self, command=self.__back, height=62, image=self.__back_icon,
            width=50
        )
        self.__back_arrow.grid(row=3, column=0)

    def __init_forward_arrow(self):
        self.__forward_arrow = tkinter.Button(
            self, command=self.__forward, height=62,
            image=self.__forward_icon, width=50
        )
        self.__forward_arrow.grid(row=3, column=4)

    def __init_history_info(self):
        self.__history_var = tkinter.StringVar()
        self.__history_info = tkinter.Label(
            self, fg="white", textvariable=self.__history_var
        )
        self.__history_info.grid(row=5, column=0, columnspan=5)
    
    def __update(self):
        self.__update_turn_info()
        self.__update_error_info()
        self.__update_playing_grid()
        self.__update_history_info()
    
    def __update_turn_info(self):
        if self.__game.winner == 1:
            self.__turn_var.set("Blue wins!")
        elif self.__game.winner == 2:
            self.__turn_var.set("Red wins!")
        elif self.__game.next_player == 1:
            self.__turn_var.set("Blue to play:")
        elif self.__game.next_player == 2:
            self.__turn_var.set("Red to play:")
        else:
            self.__turn_var.set("")
    
    def __update_error_info(self):
        self.__error_var.set("")
    
    def __update_playing_grid(self):
        for i in range(9):
            grid = self.__game.history[self.__history_view]
            if grid[i] == 0:
                self.__playing_grid[i].config(image=self.__blank)
            elif grid[i] == 1:
                self.__playing_grid[i].config(image=self.__blue)
                #if i == grid.previous_move:
                #    self.__playing_grid[i].config(image=self.__blue_locked)
                #else:
                #    self.__playing_grid[i].config(image=self.__blue)
            elif grid[i] == 2:
                self.__playing_grid[i].config(image=self.__red)
                #if i == grid.previous_move:
                #    self.__playing_grid[i].config(image=self.__red_locked)
                #else:
                #    self.__playing_grid[i].config(image=self.__red)
        
    def __update_history_info(self):
        if self.__history_view == -1:
            self.__history_var.set("Current turn")
        else:
            self.__history_var.set(
                f"History: "
                f"{len(self.__game.history) + self.__history_view}"
                f"/{len(self.__game.history) - 1}"
            )

    def __play(self, tile):
        def play_tile():
            if self.__history_view < -1:
                return
            try:
                self.__game.play(tile)
                self.__update()
            except GameEndedError:
                return
            except IllegalPlayError:
                self.__error_var.set(
                    "This is an invalid play. Choose another tile."
                )
        return play_tile
    
    def __back(self):
        if self.__history_view <= -len(self.__game.history):
            return
        self.__history_view -= 1
        self.__update()

    def __forward(self):
        if self.__history_view >= -1:
            return
        self.__history_view += 1
        self.__update()
    
    def __reset(self):
        self.__game = RewritableTTT()
        self.__history_view = -1
        self.__update()
    
    def __undo(self):
        try:
            self.__game.undo()
            self.__history_view = -1
            self.__update()
        except NoHistoryError:
            self.__error_var.set("There's no game history to undo.")
    
    def __undo_here(self):
        for i in range(-self.__history_view - 1):
            self.__game.undo()
        self.__history_view = -1
        self.__update()


Interface().mainloop()
