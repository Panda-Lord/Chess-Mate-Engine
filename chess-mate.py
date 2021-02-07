def board_reset():
        """Create and set up board"""
        white = (1, 2)
        black = (7, 8)
        board = {}
        numbers = range(1,9)
        pieces = "rhbqkbhr"
        for y in numbers:
            for x in numbers:
                color = None
                piece = None
                square = None
                if y in (1, 8):
                    piece = pieces[y-1]
                elif y in (2, 7):
                    piece = "p"
                if y in white:
                    color = "w"
                elif y in black:
                    color = "b"
                if color and piece:
                    square = {"color" : color, "piece" : piece}
                board[(x, y)] = square
        return (board, {"turn": 0, "check": False, "en_passant": False, "history": []})

class Moves():
    """Class for moves for each piece, each move returns a tuple of coordinates in format (move_to, attack_square, en_passant_eligible), 
    en_assant_eligible returns coordinates of recent double pawn move or True if en passant move is valid to differentiate this attack"""
    def __init__(self, board, info, start):
        self.board = board
        self.info = info
        self.x = start[0]
        self.y = start[1]
        self.extent = range(1,9)
        self.piece = self.board[start]
        self.en_passant = self.info["en_passant"]
        if self.piece["color"] == "w":
            self.direction = 1
        elif self.piece["color"] == "b":
            self.direction = -1

    def pawn_forward(self):
        """Single move forward by pawn"""
        move = (self.x, self.y + 1 * self.direction)
        if self.board[move] or move[0] not in self.extent or move[1] not in self.extent:
            move = False
        return (move, None, False)

    def pawn_double(self):
        """Pawn double move"""
        if (self.direction == 1 and self.y != 2) or (self.direction == -1 and self.y != 7):
            print("test")
            return (False, None, False)
        move = (self.x, self.y + 2 * self.direction)
        if self.board[move] and self.board[self.x, self.x + 1 * self.direction] or move[0] not in self.extent or move[1] not in self.extent:
            move = False
        return (move, None, move)
    
    def pawn_attack(self, x):
        """diagonal pawn attack"""
        move = (self.x + x, self.y + 1 * self.direction)
        if self.board.get(move):
            if self.board[move]["color"] != self.piece["color"]:
                return (move, move, False)
        return (False, None, False)
    
    def pawn_en_passant(self, x):
        """en passant attack"""
        attack = (self.x + x, self.y)
        if self.en_passant == attack:
            move = (self.x + 1, self.y + 1 * self.direction)
            if not self.board[move] and not self.board[self.x, self.x + 1 * self.direction] or move[0] in self.extent or move[1] in self.extent:
                return (move, attack, True)
        return (False, None, True)

class Pieces():
    """Class for pieces control and moves"""
    def __init__(self, board, info, start):
        self.board = board
        self.info = info
        self.start = start
        
    def pawn_moves(self):
        moves = Moves(self.board, self.info, self.start)
        valid_moves = []
        valid_moves.append(moves.pawn_forward())
        valid_moves.append(moves.pawn_double())
        valid_moves.append(moves.pawn_attack(1))
        valid_moves.append(moves.pawn_attack(-1))
        valid_moves.append(moves.pawn_en_passant(1))
        valid_moves.append(moves.pawn_en_passant(-1))
        valid_moves = tuple(filter(lambda move: move[0] != False, valid_moves))
        return valid_moves

class Game():
    """Class responsible for general game control"""
    def __init__(self, game):
        self.board = game[0]
        self.info = game[1]

    def ascii(self):
        """Prints ASCII board in console"""
        rows = ""
        rim = " +------------------------+ \n"
        letters = "   A  B  C  D  E  F  G  H  \n"
        for y in range(1, 9):
            row = ""
            for x in range(1, 9):
                if self.board[(x, y)]:
                    piece = self.board[(x, y)].get("piece")
                else:
                    piece = "."
                row = row + " " + piece + " "
            rows = str(y) + "|" + row + "|" + str(y) + "\n" + rows
        return print(f"{letters}{rim}{rows}{rim}{letters}")

    def get_moves(self, start):
        """Gets moves for specific piece"""
        piece = self.board[start]
        if not piece:
            return False

        pieces = Pieces(self.board, self.info, start)
        pieces_dict = {"p": pieces.pawn_moves()}

        return pieces_dict[piece["piece"]]
        





        


board = board_reset()

print(board)
round = Game(board)

# # print(round.valid_moves("h7"))

round.ascii()

print(round.get_moves((1, 2)))

# # print(coord_calc("H3", -1, 1))