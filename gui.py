import tkinter

import domain


class CurrentStateDisplay(tkinter.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.__square_displays = []
        for ii in range(9):
            square_display = tkinter.Button(
                self, command=self.__click_square_command(ii + 1)
            )
            square_display.grid(row=ii//3, column=ii%3)
            self.__square_displays.append(square_display)

    def __click_square_command(self, position: int):
        def command():
            self.master.click_square(position)
        return command

    def show(self, state: domain.GameState):
        for sq, sqd in zip(state.squares, self.__square_displays):
            square = sq
            square_display = sqd
            square_display.config(image=self.master.square_image(square))


class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title("Rewritable Tic-Tac-Toe")
        self.__game = domain.Game()
        self.__displayed_turn = 0
        self.__init_images()
        self.__init_menu()
        self.__init_info_pane()
        self.__init_game_pane()
        self.__update_state_displays()

    def __init_images(self):
        self.__images = (
            tkinter.PhotoImage(file="assets/square_blank.png"),
            tkinter.PhotoImage(file="assets/square_blue.png"),
            tkinter.PhotoImage(file="assets/square_red.png"),
        )

    def __init_menu(self):
        self.__menu = tkinter.Menu(self)
        self.__game_menu = tkinter.Menu(self.__menu)
        self.__game_menu.add_command(
            label="Reset", command=self.reset
        )
        self.__game_menu.add_command(
            label="Undo", command=self.undo
        )
        self.__game_menu.add_command(
            label="Undo to Here", command=self.undo_to_here
        )
        self.__menu.add_cascade(
            label="Game", menu=self.__game_menu
        )
        self.config(menu=self.__menu)

    def __init_game_pane(self):
        self.__current_state_display = CurrentStateDisplay(self)
        self.__current_state_display.grid(row=1, column=0)

    def __init_info_pane(self):
        self.__info_pane = tkinter.Frame(self)
        self.__info_pane.grid(row=0, column=0)
        self.__message_var = tkinter.StringVar()
        self.__message_label = tkinter.Label(
            self.__info_pane, textvariable=self.__message_var
        )
        self.__message_label.grid(row=0, column=0, columnspan=3)
        self.__back_button = tkinter.Button(
            self.__info_pane, command=self.go_back, text="<"
        )
        self.__back_button.grid(row=1, column=0)
        self.__turn_var = tkinter.StringVar()
        self.__turn_label = tkinter.Label(
            self.__info_pane, textvariable=self.__turn_var
        )
        self.__turn_label.grid(row=1, column=1)
        self.__forward_button = tkinter.Button(
            self.__info_pane, command=self.go_forward, text=">"
        )
        self.__forward_button.grid(row=1, column=2)
        self.__status_var = tkinter.StringVar()
        self.__status_label = tkinter.Label(
            self.__info_pane, textvariable=self.__status_var
        )
        self.__status_label.grid(row=2, column=1)

    def __update_state_displays(self):
        self.__current_state_display.show(self.__game[self.__displayed_turn])
        self.__message_var.set("")
        self.__turn_var.set(
            f"Turn {self.__displayed_turn}/{self.__game.turns_elapsed}"
        )
        if self.__game.winner == domain.Mark.BLUE:
            self.__status_var.set("Blue wins!")
        elif self.__game.winner == domain.Mark.RED:
            self.__status_var.set("Red wins!")
        elif self.__game.acting_player == domain.Mark.BLUE:
            self.__status_var.set("Blue to play:")
        elif self.__game.acting_player == domain.Mark.RED:
            self.__status_var.set("Red to play:")

    def square_image(self, square: domain.Mark):
        if square == domain.Mark.BLANK:
            return self.__images[0]
        if square == domain.Mark.BLUE:
            return self.__images[1]
        if square == domain.Mark.RED:
            return self.__images[2]

    def go_back(self):
        if self.__displayed_turn == 0:
            return
        self.__displayed_turn -= 1
        self.__update_state_displays()

    def go_forward(self):
        if self.__displayed_turn == self.__game.turns_elapsed:
            return
        self.__displayed_turn += 1
        self.__update_state_displays()

    def click_square(self, position: int):
        try:
            self.__game.play(position)
        except domain.RewritableTicTacToeError as e:
            self.__message_var.set(str(e))
        else:
            self.__displayed_turn = self.__game.turns_elapsed
            self.__update_state_displays()

    def reset(self):
        self.__game = domain.Game()
        self.__displayed_turn = 0
        self.__update_state_displays()

    def undo(self):
        self.__game.undo_once()
        self.__displayed_turn = self.__game.turns_elapsed
        self.__update_state_displays()

    def undo_to_here(self):
        self.__game.undo_until(self.__displayed_turn)
        self.__update_state_displays()


if __name__ == "__main__":
    MainWindow().mainloop()
