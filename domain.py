class GameEndedError(Exception):
    pass


class IllegalPlayError(Exception):
    pass


class NoHistoryError(Exception):
    pass


class Grid:

    def __init__(self, tiles, previous_move=None):
        self.__tiles = tiles
        self.__previous_move = previous_move

    def __repr__(self):
        grid_str = ""
        for tile in self.__tiles:
            if tile:
                grid_str = grid_str + str(tile)
            else:
                grid_str = grid_str + "."
        return "\n".join((grid_str[:3], grid_str[3:6], grid_str[6:]))

    def __getitem__(self, index):
        return self.__tiles[index]

    def __eq__(self, other):
        return self.__tiles == other.__tiles
    
    @property
    def previous_move(self):
        return self.__previous_move

    @property
    def winner(self):
        winners = [None, False, False]
        if self.__tiles[0] == self.__tiles[1] == self.__tiles[2]:
            winners[self.__tiles[0]] = True
        if self.__tiles[3] == self.__tiles[4] == self.__tiles[5]:
            winners[self.__tiles[3]] = True
        if self.__tiles[6] == self.__tiles[7] == self.__tiles[8]:
            winners[self.__tiles[6]] = True
        if self.__tiles[0] == self.__tiles[3] == self.__tiles[6]:
            winners[self.__tiles[0]] = True
        if self.__tiles[1] == self.__tiles[4] == self.__tiles[7]:
            winners[self.__tiles[1]] = True
        if self.__tiles[2] == self.__tiles[5] == self.__tiles[8]:
            winners[self.__tiles[2]] = True
        if self.__tiles[0] == self.__tiles[4] == self.__tiles[8]:
            winners[self.__tiles[0]] = True
        if self.__tiles[2] == self.__tiles[4] == self.__tiles[6]:
            winners[self.__tiles[2]] = True
        if winners[1] and not winners[2]:
            return 1
        elif winners[2] and not winners[1]:
            return 2

    def play(self, player, tile):
        tiles = list(self.__tiles)
        tiles[tile] = player
        return Grid(tuple(tiles), tile)


class RewritableTTT:

    def __init__(self):
        self.__history = [Grid((0, 0, 0, 0, 0, 0, 0, 0, 0))]
        self.__next_player = 1

    @property
    def history(self):
        return self.__history

    @property
    def next_player(self):
        return self.__next_player

    @property
    def winner(self):
        return self.__history[-1].winner

    def play(self, tile):
        if self.winner is not None:
            raise GameEndedError("here is some sample text")
        if tile not in range(9):
            raise ValueError()
        # Extra rule to not allow immediate overwrite
        # if tile == self.__history[-1].previous_move:
        #     raise IllegalPlayError()
        prev_grid = self.__history[-1]
        next_grid = prev_grid.play(self.__next_player, tile)
        if next_grid in self.__history:
            raise IllegalPlayError()
        self.__history.append(next_grid)
        self.__next_player = 3 - self.__next_player

    def undo(self):
        if len(self.__history) < 2:
            raise NoHistoryError()
        self.__history.pop()
        self.__next_player = 3 - self.__next_player
