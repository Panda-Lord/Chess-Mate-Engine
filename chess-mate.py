import random

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
        return (board, {"turn": 1, "check": False, "mate": False, "en_passant": False, "history": []})

class Moves():
    """Class for moves for each piece, each move returns a tuple of coordinates in format (move_to, attack_square, en_passant_eligible), 
    en_assant_eligible returns coordinates of recent double pawn move or True if en passant move is valid to differentiate this attack"""
    def __init__(self, board, info, start):
        self.board = board
        self.info = info
        self.x = start[0]
        self.y = start[1]
        self.limits = range(1,9)
        self.piece = self.board[start]
        self.en_passant = self.info["en_passant"]
        if self.piece["color"] == "w":
            self.direction = 1
        elif self.piece["color"] == "b":
            self.direction = -1

    def pawn_forward(self):
        """Single move forward only, can't beat"""
        move = (self.x, self.y + 1 * self.direction)
        if move[0] not in self.limits or move[1] not in self.limits:
            move = False
        elif self.board[move]:
            move = False
        return (move, None, False)

    def pawn_double(self):
        """Double move forward only, can't beat"""
        if (self.direction == 1 and self.y != 2) or (self.direction == -1 and self.y != 7):
            return (False, None, False)
        if self.pawn_forward()[0] == False:
            return (False, None, False)
        move = (self.x, self.y + 2 * self.direction)
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
            if move[0] in self.limits and move[1] in self.limits:
                if not self.board[move] and not self.board[self.x, self.x + 1 * self.direction]:
                    return (move, attack, True)
        return (False, None, True)

    def piece_move(self, x, y):
        """Move and beat in any direction"""
        move = (self.x + x, self.y + y)
        if move[0] in self.limits and move[1] in self.limits:
            if self.board.get(move, False):
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
                distance += 1
                if move[0]:
                    valid_moves.append(move)
                    if self.board.get(move[1], False):
                        break
                else:
                    break
        return tuple(filter(lambda move: move[0] != False, valid_moves))   

    # def castling()
    # *** to do, encastling ***       

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
        return tuple(moves.loop_directions(directions))
    
    def horse_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Horse (Knight)"""
        valid_moves = []
        distances = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        for dist in distances:
            valid_moves.append(moves.piece_move(dist[0], dist[1]))
        return tuple(filter(lambda move: move[0] != False, valid_moves))           

    def bishop_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Bishop"""
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        return tuple(moves.loop_directions(directions))

    def queen_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Queen"""
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        return tuple(moves.loop_directions(directions))

    def king_moves(self, start):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for King"""
        color = self.board[start]["color"]
        if color == "w":
            color = "b"
        else:
            color = "w"
        valid_moves = []
        distances = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
        for dist in distances:
            valid_moves.append(moves.piece_move(dist[0], dist[1]))
        valid_moves = list(filter(lambda move: move[0] != False, valid_moves))
        if (self.info["turn"] % 2 == 0 and color == "w") or (self.info["turn"] % 2 != 0 and color == "b"):
            return tuple(filter(lambda move: move[0] not in self.all_attacks(color), valid_moves))
        else:
            return tuple(valid_moves)

    def all_attacks(self, color):
        """"""
        attack_moves = []
        for start, piece in self.board.items():
            if piece:
                if piece["color"] == color:
                    attack_moves = attack_moves + list(map(lambda attack_move: attack_move[1], list(filter(lambda move: move[1] != None and move[2] != True, self.get_moves(start)))))
        return tuple(set(attack_moves))

    def is_check_move(self, move, start):
        """checks if any of the list of moves would create "check" status"""
        new_board = self.board.copy()
        new_board[move[1]] = self.board[start]
        new_board[start] = None
        color = self.board[start]["color"]
        if color == "w":
            color = "b"
        else:
            color = "w"
        attack_moves = self.all_attacks(color)
        for move in attack_moves:
            if new_board.get(move, False) == "k":
                return True
        return False

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

    def valid_moves_list(self, start):
        """Filters moves to make sure they don't include any possible checks"""
        moves = self.get_moves(start)
        moves1 = tuple(filter(lambda move: not self.is_check_move(move[0], start), moves))
        return moves1

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
        """Gets moves for specific piece based off its location via function in Pieces class"""
        piece = Pieces_Moves(self.board, self.info)
        return piece.valid_moves_list(start)            

    def move_piece(self, start, end):
        """Checks if correct player is taking the turn and then if then if move is in list of valid moves. Lastly, calls a function to check if "check" condition exists on king"""
        if not self.board[start]:
            return (False, "Sqaure is empty")
        if (self.info["turn"] % 2 != 0 and self.board[start]["color"] == "b") or (self.info["turn"] % 2 == 0 and self.board[start]["color"] == "w"):
            """checks for correct turn"""
            return (False, "Other players turn")
        moves = self.get_moves(start)
        for move in moves:
            check = False
            if move[0] == end:
                self.board[move[1]] = None
                self.board[end] = self.board[start]
                self.board[start] = None
                check = (False, False)
                check = self.check_status(end)
                return (
                self.board,
                    {
                        "turn": self.info["turn"] + 1,
                        "check": check[0],
                        "mate": check[1],
                        "en_passant": move[2],
                        "history": self.info["history"] + [f"{start[0]}{start[1]}{end[0]}{end[1]}"]
                    }
                )
        return (False, "Invalid move")

    # def update_board(self, start, end, attack, check, mate)      

    def check_status(self, start):
        """Retuns a tuple with False or True for (check, mate)"""
        check = False
        mate = False
        for move in self.get_moves(start):
            attack = self.board.get(move[1], False)
            if attack:
                if attack.get("piece", False) == "k":
                    check = True
                    if not self.get_moves(move[1]):
                        mate = True
                        print("check")
        return (check, mate)

    def check_mate(self):
        """checks for game over / check mate status"""
        if self.info["mate"]:
            if self.info["turn"] % 2 == 0:
                player = "White"
            else:
                player = "Black"
            print(f"*** Check Mate! {player} wins the game ***")
            return True
        
    def play(self):
        check_mate = False
        while not check_mate:
            start = input("Move from:")
            start = (ord(start[0])-96, int(start[1]))
            end = input("Move to:")
            end = (ord(end[0])-96, int(end[1]))
            valid_squares = True
            for number in start[0], start[1], end[0], end[1]:
                if number not in range(1,9):
                    valid_squares = False
            if valid_squares:
                update_game = self.move_piece(start, end)
                if update_game[0]:
                    self.board = update_game[0]
                    self.info = update_game[1]
                else:
                    print(f"*** {update_game[1]}, try again. ***")
            else:
                print("*** Not valid square, try again ***")
            # print(self.board)
            # print(self.info)
            self.ascii()
            check_mate = self.check_mate()

    def play_random_ai(self):
        check_mate = False
        while not check_mate:
            ai_moves = {}
            if self.info["turn"] % 2 == 0:
                color = "b"
            else:
                color = "w"
            for position, piece in self.board.items():
                if piece:
                    if piece.get("color", False) == color:
                        moves = self.get_moves(position)
                        if moves:
                            ai_moves[position] = moves
            start = random.choice(list(ai_moves))
            end = random.choice(ai_moves[start])[0]
            print(f'move from {start}')
            print(f'move to {end}')
            valid_squares = True
            for number in start[0], start[1], end[0], end[1]:
                if number not in range(1,9):
                    valid_squares = False
            if valid_squares:
                update_game = self.move_piece(start, end)
                if update_game[0]:
                    self.board = update_game[0]
                    self.info = update_game[1]
                else:
                    print(f"*** {update_game[1]}, try again. ***")
            else:
                print("*** Not valid square, try again ***")
            # print(self.board)
            # print(self.info)
            if end[1] in [1,8] and self.board[end]["piece"] == "p":
                self.board[end]["piece"] = "q"
            self.ascii()
            check_mate = self.check_mate()

board = board_reset()
# print(board)
new_game = Game(board)
new_game.ascii()
new_game.play_random_ai()