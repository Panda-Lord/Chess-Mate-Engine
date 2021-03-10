import random
import chess_moves

# class Min_Max():
#     """Min max algo"""

#     def __init__(self, board, info):
#         self.board = board
#         self.info = info
#         self.moves = chess_moves.Pieces_Moves(self.board, self.info)
#         self.weight = {
#             None: 0,
#             "p": 100,
#             "h": 300,
#             "b": 300,
#             "r": 500,
#             "k": 700,
#             "upgrade": 800,
#             "q": 900
#         }
    
#     def col_switch(self, color):
#         if color == "w":
#             return "b"
#         elif color == "b":
#             return "w"

#     def iterate_moves(self, level):
#         for position, piece in self.board.items():
#             if piece:
#                 if piece.get("color", False) == color:
#                     for m in self.moves.get_moves(position):

#     def execute_fake_move(self, move):
#         """fake move to be iterated over by min max"""
#         weight = 0
#         start = move[0]
#         move = move[1]
#         piece = self.board[move]
#         if move[1]:
#             self.board[move[1]] = None
#         self.board[move] = None
#         self.board[move[0]] = piece
#         self.info["turn"] += 1
#         if move[3]:
#             weight = self.weight[move[3]]
#         return [weight, self.board, self.info]

#     def valuate_moves(self, color, min_max):
#         weight = 0
#         moving = None
#         for position, piece in self.board.items():
#             if piece:
#                 if piece.get("color", False) == color:
#                     for move in self.moves.get_moves(position):
#                         moving = move
#                         weight, board, info = self.execute_fake_move(move)
#                         iteration = Min_Max(board, info)
#                         weight += iteration.valuate_moves(self.col_switch(color))
#         return weight

class AI_Moves():
    """all logic to do with algos for AI moves"""

    def __init__(self, board, info):
        self.board = board
        self.info = info
        self.moves = chess_moves.Pieces_Moves(self.board, self.info)
        self.weight = {
            "p": 100,
            "h": 300,
            "b": 300,
            "r": 500,
            "k": 700,
            "upgrade": 800,
            "q": 900,
            "m": 10000
        }

        self.info["turn"] += 1

    def random_move(self, color):
        """returns random move for given color/player"""
        moves = self.moves.get_all_moves(color)
        start = random.choice(list(moves))
        move = random.choice(moves[start])
        return (start, move)
                            