import enum
from typing import Iterable, Self


class Mark(enum.Enum):
    BLANK = "."
    BLUE = "o"
    RED = "x"

    @property
    def opponent(self):
        match self:
            case Mark.BLUE:
                return Mark.RED
            case Mark.RED:
                return Mark.BLUE


class RewritableTicTacToeError(Exception):
    pass


class IllegalActionError(RewritableTicTacToeError):
    pass


class GameState:

    def __init__(
            self,
            squares: Iterable[Mark] | None = None,
            acting_player: Mark = Mark.BLUE,
        ):
        if squares is None:
            squares = [Mark.BLANK] * 9
        self.__squares: list[Mark] = list(squares)
        self.__acting_player = acting_player

    @property
    def squares(self):
        return self.__squares.copy()

    @property
    def acting_player(self):
        return self.__acting_player

    @property
    def winner(self):
        if Mark.BLANK != self.square(1) == self.square(2) == self.square(3):
            return self.square(1)
        if Mark.BLANK != self.square(4) == self.square(5) == self.square(6):
            return self.square(4)
        if Mark.BLANK != self.square(7) == self.square(8) == self.square(9):
            return self.square(7)
        if Mark.BLANK != self.square(1) == self.square(4) == self.square(7):
            return self.square(1)
        if Mark.BLANK != self.square(2) == self.square(5) == self.square(8):
            return self.square(2)
        if Mark.BLANK != self.square(3) == self.square(6) == self.square(9):
            return self.square(3)
        if Mark.BLANK != self.square(1) == self.square(5) == self.square(9):
            return self.square(1)
        if Mark.BLANK != self.square(3) == self.square(5) == self.square(7):
            return self.square(3)

    def __eq__(self, other: Self):
        return self.__squares == other.__squares

    def square(self, position: int):
        return self.__squares[position - 1]

    def copy(self):
        return GameState(self.__squares, self.__acting_player)

    def play(self, position: int, player: Mark | None = None):
        if self.winner is not None:
            raise IllegalActionError
        if player not in (self.__acting_player, None):
            raise IllegalActionError
        self.__squares[position - 1] = self.__acting_player
        self.__acting_player = self.__acting_player.opponent


class Game:

    def __init__(self, starting_states: Iterable[GameState] | None = None):
        if not starting_states:
            starting_states = [GameState()]
        self.__states_seen = [state.copy() for state in starting_states]
        self.__positions_played: list[int] = []

    @staticmethod
    def from_position_sequence(positions: Iterable[int]):
        new_game_state = Game()
        for position in positions:
            new_game_state.play(position)
        return new_game_state

    def __current_state(self):
        return self.__states_seen[-1]

    @property
    def acting_player(self):
        return self.__current_state().acting_player

    @property
    def positions_played(self):
        return self.__positions_played.copy()

    @property
    def winner(self):
        return self.__current_state().winner

    def __eq__(self, other: Self):
        if len(self.__states_seen) != len(other.__states_seen):
            return False
        if self.__current_state() != other.__current_state():
            return False
        for state in self.__states_seen:
            if state not in other.__states_seen:
                return False
        return True

    def __getitem__(self, index: int):
        return self.__states_seen[index]

    def __len__(self):
        return len(self.__states_seen)

    def __repr__(self):
        return f"<{''.join(map(str, self.__positions_played))}>"

    def copy(self):
        new_game_state = Game()
        new_game_state.__states_seen = [
            state.copy() for state in self.__states_seen
        ]
        new_game_state.__positions_played = self.__positions_played.copy()
        return new_game_state

    def play(self, position: int, player: Mark | None = None):
        new_state = self.__current_state().copy()
        new_state.play(position, player)
        if new_state in self.__states_seen:
            raise IllegalActionError
        self.__states_seen.append(new_state)
        self.__positions_played.append(position)

    def undo_once(self):
        self.__positions_played.pop()
        self.__states_seen.pop()

    def undo_until(self, index: int):
        index = index % len(self.__states_seen)
        for ii in range(len(self.__states_seen) - 1 - index):
            self.undo_once()
