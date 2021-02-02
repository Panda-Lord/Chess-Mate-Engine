def board_reset(position = 0):
        """Create and set up board"""
        if position == 0:
            white = "12"
            black = "78"
        elif position == 1:
            white = "78"
            black = "12"
        board = {}
        numbers = "12345678"
        letters = "abcdefgh"
        pieces = "rhbqkbhr"
        for n in numbers:
            for l in letters:
                color = None
                piece = None
                square = None
                if n in "81":
                    piece = pieces[ord(l)-97]
                elif n in "72":
                    piece = "p"
                if n in white:
                    color = "w"
                elif n in black:
                    color = "b"
                if color and piece:
                    square = {"color" : color, "piece" : piece}
                board[l+n] = square
        return board  

class Game():
    """Class responsible for movement, validation and anything to do with the game process"""
    def __init__(self, board, move = None):
        self.board = board
        self.move = move

    def ascii(self):
        """Prints ASCII board in console"""
        count = 0
        set_up = ""
        rim = " +------------------------+ \n"
        letters = "   A  B  C  D  E  F  G  H  \n"
        for square, value in self.board.items():
            count += 1
            position = "."
            if count == 1:
                set_up = set_up + square[1] + "|"
            if value:
                position = value["piece"]
            set_up = set_up + " " + position + " "
            if count == 8:
                set_up = set_up + "|" + square[1] + "\n"
                count = 0
        ascii_board = f"{letters}{rim}{set_up}{rim}{letters}"
        return ascii_board
            



    # def validate(self)
    #     """validates the move"""


# board = board_reset()
# print(board)

# round = Game(board)

# print(round.ascii())