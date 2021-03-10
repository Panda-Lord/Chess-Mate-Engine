class Moves():
    """Class for moves types, each move returns a tuple of coordinates in format (move_to, attack_square, en_passant_eligible, beats/if_upgradable), 
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
        swap = None
        move = (self.x, self.y + 1 * self.direction)
        if move[0] not in self.limits or move[1] not in self.limits:
            move = False
        elif self.board[move]:
            move = False
        elif move[1] == 1 or move[1] == 8:
            swap = "upgrade"
        return (move, None, False, swap)

    def pawn_double(self):
        """Double move forward only, can't beat"""
        if (self.direction == 1 and self.y != 2) or (self.direction == -1 and self.y != 7):
            return (False, None, False)
        if self.pawn_forward()[0] == False:
            return (False, None, False)
        move = (self.x, self.y + 2 * self.direction)
        return (move, None, move, None)
    
    def pawn_attack(self, x, is_empty):
        """diagonal pawn move and beat"""
        move = (self.x + x, self.y + 1 * self.direction)
        beats = None
        if self.board.get(move):
            if self.board[move]["color"] != self.piece["color"]:
                beats = self.board[move]["piece"]
                if move[1] == 1 or move[1] == 8:
                    beats = "upgrade"
                return (move, move, False, beats)
        elif is_empty and move in self.board.keys():
            return (move, move, False, beats)
        return (False, None, False, beats)
    
    def pawn_en_passant(self, x):
        """en passant attack"""
        attack = (self.x + x, self.y)
        if self.en_passant == attack:
            move = (self.x + x, self.y + 1 * self.direction)
            if move[0] in self.limits and move[1] in self.limits:
                if not self.board[move] and not self.board[self.x, self.y + 1 * self.direction]:
                    return (move, attack, True, "p")
        return (False, None, True, None)

    def piece_move(self, x, y):
        """Move and beat in any direction"""
        beats = None
        move = (self.x + x, self.y + y)
        if move[0] in self.limits and move[1] in self.limits:
            if self.board.get(move, False):
                if self.board[move]["color"] == self.piece["color"]:
                    move = False
                else:
                    beats = self.board[move]["piece"]
            return (move, move, False, beats)
        return (False, None, False, beats)

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
    # *** to do, castling ***       

class Pieces_Moves():
    """Class for pieces control and moves"""
    def __init__(self, board, info):
        self.board = board
        self.info = info
 
        
    def pawn_moves(self, start, is_empty):
        """returns a tuple of valid moves for pawn"""
        moves = Moves(self.board, self.info, start)
        valid_moves = []
        valid_moves.append(moves.pawn_forward())
        valid_moves.append(moves.pawn_double())
        valid_moves.append(moves.pawn_attack(1, is_empty))
        valid_moves.append(moves.pawn_attack(-1, is_empty))
        valid_moves.append(moves.pawn_en_passant(1))
        valid_moves.append(moves.pawn_en_passant(-1))
        return tuple(filter(lambda move: move[0] != False, valid_moves))
    
    def rook_moves(self, start, is_empty):
        """returns tuple of valid moves for Rook"""
        moves = Moves(self.board, self.info, start)
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        return tuple(moves.loop_directions(directions))
    
    def horse_moves(self, start, is_empty):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Horse (Knight)"""
        valid_moves = []
        distances = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        for dist in distances:
            valid_moves.append(moves.piece_move(dist[0], dist[1]))
        return tuple(filter(lambda move: move[0] != False, valid_moves))           

    def bishop_moves(self, start, is_empty):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Bishop"""
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
        return tuple(moves.loop_directions(directions))

    def queen_moves(self, start, is_empty):
        moves = Moves(self.board, self.info, start)
        """returns tuple of valid moves for Queen"""
        directions = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        return tuple(moves.loop_directions(directions))

    def king_moves(self, start, is_empty):
        """returns tuple of valid moves for King"""
        moves = Moves(self.board, self.info, start)
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
            all_attacks = self.all_attacks(color)
            # print(all_attacks)
            valid_moves = tuple(filter(lambda move: move[1] not in all_attacks, valid_moves))
            # print(valid_moves)
        else:
            valid_moves = tuple(valid_moves)
        return valid_moves

    def all_attacks(self, color):
        """Get all possible attack moves for a color/player as tuple"""
        attack_moves = []
        for position, piece in self.board.items():
            if piece:
                if piece["color"] == color:
                    attack_moves = attack_moves + list(map(lambda attack_move: attack_move[1], list(filter(lambda move: move[1] != None and move[2] != True, self.move_options(position, True)))))
        return tuple(set(attack_moves))

    def is_check_status(self, color):
        """checks if check status is True"""
        if color == "w":
            color = "b"
        else:
            color = "w"
        attacks = self.all_attacks(color)
        for attack in attacks:
            if self.board[attack]:
                if self.board[attack].get("piece", False) == "k":
                    return True
        return False

    def is_check_move(self, move, start):
        """checks if any of the list of moves would create "check" status"""
        piece = self.board[start]
        color = piece["color"]
        imaginary_board = self.board.copy()
        imaginary_board[start] = None
        imaginary_board[move] = piece
        imaginary_info = self.info.copy()
        imaginary_move = Pieces_Moves(imaginary_board, imaginary_info)
        return imaginary_move.is_check_status(color)

    def move_options(self, start, is_empty = False):
        """Gets all moves for piece at specified location, not accounting for check status"""
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
        return pieces_dict[piece["piece"]](start, is_empty)

    def get_moves(self, start):
        """Goes through mvoe options and returns all valid moves that would not end in check status"""
        moves = self.move_options(start)
        moves = tuple(filter(lambda move: not self.is_check_move(move[0], start), moves))
        return moves

    def get_all_moves(self, color):
        """get all moves for color"""
        all_moves = {}
        for position, piece in self.board.items():
                    if piece:
                        if piece.get("color", False) == color:
                            moves = self.get_moves(position)
                            if moves:
                                all_moves[position] = moves
        return all_moves