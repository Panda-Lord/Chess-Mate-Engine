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
                    piece = pieces[x-1]
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
        """Single move forward only, can't beat"""
        move = (self.x, self.y + 1 * self.direction)
        if self.board[move] or move[0] not in self.extent or move[1] not in self.extent:
            move = False
        return (move, None, False)

    def pawn_double(self):
        """Double move forward only, can't beat"""
        if (self.direction == 1 and self.y != 2) or (self.direction == -1 and self.y != 7):
            return (False, None, False)
        move = (self.x, self.y + 2 * self.direction)
        if self.board[move] and self.board[self.x, self.x + 1 * self.direction] or move[0] not in self.extent or move[1] not in self.extent:
            move = False
        return (move, None, move)
    
    def pawn_attack(self, x):
        """diagonal pawn move and beat"""
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

    def piece_move(self, x, y):
        """Move and beat in any direction"""
        move = (self.x + x, self.y + y)
        if move[0] in self.extent and move[1] in self.extent:
            if self.board.get(move):
                if self.board[move]["color"] == self.piece["color"]:
                    move = False
            return (move, move, False)
        return (False, None, False)

    def loop_directions(self, directions):
        """loops directional moves for bishop, rook and queen"""
        valid_moves = []
        for dir in directions:
            distance = 1
            while True:
                move = self.piece_move(distance * dir[0], distance * dir[1])
                valid_moves.append(move)
                if not self.board.get(move[1]):
                    distance = 1
                    break
                distance += 1
        valid_moves = tuple(filter(lambda move: move[0] != False, valid_moves))            

class Pieces_Moves():
    """Class for pieces control and moves"""
    def __init__(self, board, info):
        self.board = board
        self.info = info
 
        
    def pawn_moves(self, start):
        """returns a tuple of valid moves for pawn"""
        moves = Moves(self.board, self.info, start)
        valid_moves = []
        valid_moves.append(moves.pawn_forward())
        valid_moves.append(moves.pawn_double())
        valid_moves.append(moves.pawn_attack(1))
        valid_moves.append(moves.pawn_attack(-1))
        valid_moves.append(moves.pawn_en_passant(1))
        valid_moves.append(moves.pawn_en_passant(-1))
        return tuple(filter(lambda move: move[0] != False, valid_moves))
    
    def rook_moves(self, start):
        """returns tuple of valid moves for Rook"""
        moves = Moves(self.board, self.info, start)
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        return moves.loop_directions(directions)
    
    def horse_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Horse (Knight)"""
        valid_moves = []
        distances = ((2, 3), (2, -3), (-2, 3), (-2, -3), (3, 2), (3, -2), (-3, 2), (-3, -2))
        for dist in distances:
            valid_moves.append(moves.piece_move(dist[0], dist[1]))
        return tuple(filter(lambda move: move[0] != False, valid_moves))           

    def bishop_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Bishop"""
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        return moves.loop_directions(directions)

    def queen_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Queen"""
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        return moves.loop_directions(directions)

    def king_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for King"""
        color = self.board[start]["color"]
        valid_moves = []
        distances = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        for dist in distances:
            valid_moves.append(moves.piece_move(dist[0], dist[1]))
        valid_moves = filter(lambda move: move[0] != False, valid_moves)
        return self.king_check(moves, color)
    
    def king_check(self, moves, color):
        """checks for all possible attack moves on the board and filters the King moves down to exlude all attack moves, or elsy anythin that would cause a check condition"""
        valid_moves =[]
        for start, piece in self.board.items():
            print(piece["color"] != color)
            if piece["color"] != color:
                attack_moves = tuple(map(lambda attack_move: attack_move[1], filter(lambda move: move[1] != None and move[2] != True, self.get_moves(start))))
                valid_moves = valid_moves + filter(lambda move: move[0] not in attack_moves, moves)
        return tuple(valid_moves)

    def get_moves(self, start):
        """Checks for the piece at start location and calls in move function accordingly to get valid pieces"""
        piece = self.board[start]
        if not piece:
            return False

        pieces_dict = {
            "p": self.pawn_moves,
            "r": self.rook_moves,
            "h": self.horse_moves,
            "b": self.bishop_moves,
            "q": self.queen_moves,
            "k": self.king_moves            
            }
        return pieces_dict[piece["piece"]](start)        

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
        """Gets moves for specific piece via function in Pieces class"""
        pieces = Pieces_Moves(self.board, self.info)
        return pieces.get_moves(start)

    def move_piece(self, start, end):
        for move in self.get_moves(start):
            if move[0] == end:
                self.board[end] = self.board[start]
                self.board[start] = None
                self.board[move[1]] = None
                # print("valid move")
                return (
                self.board,
                    {
                        "turn": self.info["turn"] + 1,
                        "check": False,
                        "en_passant": move[2],
                        "history": self.info["history"] + [f"{start[0]}{start[1]}{end[0]}{end[1]}"]
                    }
                )
        # print("invalid move")
        return False
        
    def play(self):
        while True:
            start = input("Move from:")
            start = (ord(start[0])-96, int(start[1]))
            # print(start)
            end = input("Move to:")
            end = (ord(end[0])-96, int(end[1]))
            # print(end)
            update_game = self.move_piece(start, end)
            if update_game:
                self.board = update_game[0]
                self.info = update_game[1]
            else:
                print("Invalid move, try again.")
            self.ascii()
            # for key, value in self.board.items():
            #     print(f"{key} {value}")




        


board = board_reset()
print(board)
new_game = Game(board)
new_game.ascii()
new_game.play()

# # print(round.valid_moves("h7"))

# round.ascii()

# print(round.get_moves((2, 1)))

# # print(coord_calc("H3", -1, 1))