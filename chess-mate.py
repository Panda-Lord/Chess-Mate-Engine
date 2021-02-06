def board_reset(swap = False):
        """Create and set up board"""
        if swap == False:
            white = "12"
            black = "78"
        elif swap == True:
            white = "78"
            black = "12"
        board = {}
        numbers = "87654321"
        letters = "abcdefgh"
        pieces = "rhbqkbhr"
        for n in numbers:
            for l in letters:
                color = None
                piece = None
                square = None
                if n in "81":
                    piece = pieces[ord(l)-97]
                # elif n in "1":
                #     piece = pieces[-1-(ord(l)-97)]
                elif n in "72":
                    piece = "p"
                if n in white:
                    color = "w"
                elif n in black:
                    color = "b"
                if color and piece:
                    square = {"color" : color, "piece" : piece}
                board[l+n] = square
        return (board, swap)

def coord_calc(current, add_letter, add_number):
    """Takes in a string of chess cordinates, position change by number of squares on each axis and returns calculated string"""
    letter = chr(ord(current[0]) + add_letter)
    number = str(int(current[1]) + add_number)
    if letter not in "abcdefgh" or number not in "12345678":
        return False
    return letter + str(number)

class Game():
    """Class responsible for movement, validation and anything to do with the game process"""
    def __init__(self, board, move = None):
        self.board = board[0]
        self.swap = board[1]
        self.move = move

    def ascii(self):
        """Prints ASCII board in console"""
        count = 0
        set_up = ""
        rim = " +------------------------+ \n"
        letters = "   A  B  C  D  E  F  G  H  \n"
        for square, value in self.board.items():
            count += 1
            placement = "."
            if count == 1:
                set_up = set_up + square[1] + "|"
            if value:
                placement = value["piece"]
            set_up = set_up + " " + placement + " "
            if count == 8:
                set_up = set_up + "|" + square[1] + "\n"
                count = 0
        ascii_board = f"{letters}{rim}{set_up}{rim}{letters}"
        return ascii_board
    
    def valid_moves(self, position):
        """lists all valid moves for given location and piece present"""
        piece = self.board[position]
        moves = []
        
        def pawn():
            """Pawn check"""
            if not self.swap:
                bottom = "w"
            elif self.swap:
                bottom = "b"
            direction = 1
            if not piece["color"] == bottom:
                direction = -1
            square = coord_calc(position, 0, 1 * direction)
            if not self.board[square]:
                moves.append({"move": square})
                if direction == 1:
                    start = "2"
                elif direction == -1:
                    start = "7"
                if start in position:
                    square =  coord_calc(position, 0, 2 * direction)
                    if not self.board[square]:
                        moves.append({"move": square})
            square = coord_calc(position, 1, 1 * direction)
            if square:
                if self.board[square]:
                    if self.board[square].get("color") != piece["color"]:
                        moves.append({"move": square, "attack": self.board[square]["piece"]})
            square = coord_calc(position, -1, 1 * direction)
            if square:
                if self.board[square]:
                    if self.board[square].get("color") != piece["color"]:
                        moves.append({"move": square, "attack": self.board[square]["piece"]})
            if direction == 1:
                start = "5"
            elif direction == -1:
                start = "4"
            if start in position:
                special = coord_calc(position, -1, 0)
                if self.board[square]:
                    if self.board[special].get("special") == "pawn_special" and self.board[special]["color"] != piece["color"]:
                        square = coord_calc(position, -1, 1 * direction)
                        if not square:
                            moves.append({"move": square, "attack": special})
                            special = coord_calc(position, -1, 0)
                special = coord_calc(position, -1, 0)
                if self.board[square]:
                    if self.board[special].get("special") == "pawn_special" and self.board[special]["color"] != piece["color"]:
                        square = coord_calc(position, -1, 1 * direction)
                        if not square:
                            moves.append({"move": square, "attack": special})
            return moves

            def 

        pieces = {"p": pawn()}
        return pieces.get(piece["piece"], False)
            



    # def validate(self)
    #     """validates the move"""
    #     piece = 
        
        


board = board_reset()
# print(board)
round = Game(board)
print(round.valid_moves("h7"))

# print(round.ascii())

# print(coord_calc("H3", -1, 1))