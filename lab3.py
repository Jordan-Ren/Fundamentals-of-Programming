"""6.009 Lab 3 -- HyperMines"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


class HyperMinesGame:
    def __init__(self, dimensions, bombs):
        """Start a new game.

        This method should properly initialize the "board", "mask",
        "dimensions", and "state" attributes.

        Args:
           dimensions (list): Dimensions of the board
           bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate
        """
        self.board = []
        self.mask = []
        self.dimensions = dimensions
        self.state = 'ongoing'
        self.make_board(self.dimensions, 0, self.board, self.mask)
        self.bombs = bombs
        for coord in self.bombs:
            self.set_bombs(coord, self.board, ".")
            bomb_coord = self.neighbors(coord)
            for neighbor in bomb_coord:
                x = self.get_coords(neighbor)
                if x != '.':
                    self.increase_coords(neighbor, self.board, 1)

    def get_board(self):
        return self.board

    def get_state(self):
        return self.state

    def update_mask(self, coord):
        def helper(coord, mask):
            if len(coord) == 1:
                mask[coord[0]] = True
                return mask[coord[0]]
            for i in range(len(mask)):
                if i == coord[0]:
                    return helper(coord[1:], mask[i])
        return helper(coord, self.mask)

    def check_mask(self, coord):
        def helper(coord, mask):
            if len(coord) == 1:
                return mask[coord[0]]
            for i in range(len(mask)):
                if i == coord[0]:
                    return helper(coord[1:], mask[i])
        return helper(coord, self.mask)

    def get_mask(self):
        return self.mask

    def make_board(self, dimensions, elem, board, mask):
        if len(dimensions) == 1:
            for i in range(dimensions[0]):
                board.append(elem)
                mask.append(False)
            return board
        for i in range(dimensions[0]):
            board.append([])
            mask.append([])
            self.make_board(dimensions[1:], 0, board[i], mask[i])

    def increase_coords(self, coord, board, val):
        def helper(coord, board, val):
            if len(coord) == 1:
                board[coord[0]] += val
                return board[coord[0]]
            for i in range(len(board)):
                if i == coord[0]:
                    return helper(coord[1:], board[i], val)
        return helper(coord, board, val)

    def get_coords(self, coord):
        def helper(coord, board):
            if len(coord) == 1:
                return board[coord[0]]
            for i in range(len(board)):
                if i == coord[0]:
                    return helper(coord[1:], board[i])
        return helper(coord, self.board)

    def set_bombs(self, coord, board, val):
        '''
        sets coordinate to a given val
        '''
        def helper(coord, board, val):
            if len(coord) == 1:
                board[coord[0]] = val
                return board[coord[0]]
            for i in range(len(board)):
                if i == coord[0]:
                    return helper(coord[1:], board[i], val)
        return helper(coord, board, val)

    def is_in_bounds(self, coords, dim):
        if coords >= dim or coords < 0:
            return False
        return True

    def neighbors(self, coords):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed
        """
        def helper(coords, dim):
            temp = []
            if len(coords) == 1:
                for i in range(-1,2):
                    if self.is_in_bounds(coords[0] + i, dim[0]):
                        temp.append([coords[0] + i])
                return temp
            for sub in helper(coords[1:], dim[1:]):
                for k in range(-1,2):
                    if self.is_in_bounds(coords[0] + k, dim[0]):
                        copy = sub.copy()
                        copy.insert(0, coords[0] + k)
                        temp.append(copy)
            return temp

        final = helper(coords, self.dimensions)
        for L in final:
            if L == coords:
                final.remove(L)
        return final

    def is_victory(self):
        """Returns whether there is a victory in the game.

        A victory occurs when all non-bomb squares have been revealed.
        (Optional) Implement this method to properly check for victory in an N-Dimensional board.

        Returns:
            boolean: True if there is a victory and False otherwise
        """
        coords = self.iterate(self.mask)
        for i in coords:
            x = self.check_mask(i)
            y = self.get_coords(i)
            if y == '.' and x:
                return False
            if y != '.' and not x:
                return False

        return True

    def dig(self, coord) :
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed
        """
        def dig_help(coord):
            if self.state != 'ongoing' or self.check_mask(coord):
                return 0

            if self.get_coords(coord) == '.':
                self.update_mask(coord)
                self.state = 'defeat'
                return 1

            if self.get_coords(coord) != 0:
                self.update_mask(coord)
                return 1

            count = 1
            self.update_mask(coord)
            if self.get_coords(coord) == 0:
                for neighbor in self.neighbors(coord):
                    count += dig_help(neighbor)
            return count
        count = dig_help(coord)
        if self.is_victory() and self.state == 'ongoing':
            self.state = 'victory'
        return count

    def iterate(self, n_array):
        '''
        Creates a list of coordinates in the given board
        returns the list.
        '''
        final = []
        def helper(n_array, dim):
            if len(dim) == 1:
                for i in range(dim[0]):
                    final.append([i])
                return final
            for sub in range(len(helper(n_array[1:], dim[1:]))):
                for i in range(dim[0]):
                    temp = final[sub].copy()
                    temp.append(i)
                    final.append(temp)
            return final
        helper(n_array, self.dimensions)
        result = []
        for L in final:
            L.reverse()
            if len(L) == len(self.dimensions):
                result.append(L)
        return result


    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Args:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           An n-dimensional array (nested lists)
        """
        board = self.iterate(self.board)
        n_array = []
        mask = []
        self.make_board(self.dimensions, 0, n_array, mask)
        for coord in board:
            if xray or self.check_mask(coord):
                if self.get_coords(coord) == 0:
                    self.set_bombs(coord, n_array, " ")
                else:
                    self.set_bombs(coord, n_array, str(self.get_coords(coord)))
            else:
                self.set_bombs(coord, n_array, "_")
        return n_array

    # ***Methods below this point are for testing and debugging purposes only. Do not modify anything here!***

    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))

    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game







game = HyperMinesGame([3,3,3], [[0, 0, 0], [2,2,2]])
# print(game.get_state())
# print(game.dig([1,1,1,1 ]))
# print(game.render())
# print(game.neighbors([2,2,2]))

# print("original board: ", game.get_board())
#
print("render original: ", game.render())
game.dig([1,1,1])
print("board after dig: ", game.get_board())
print("render after dig: ", game.render())
print(game.is_victory())
