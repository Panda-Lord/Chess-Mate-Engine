import random
import chess_moves
import ai_algo
import pdb

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
        return (board, {"turn": 1, "check": False, "mate": False, "en_passant": False, "history": [], "stale_count": 0, "castling": None})

class Game():
    """Class responsible for general game control"""
    def __init__(self, game, player_white, player_black, print_board = False, difficulty = None):
        self.board = game[0]
        self.info = game[1]
        self.player_white = player_white
        self.player_black = player_black
        self.print_board = print_board
        self.difficulty = difficulty

    def ascii(self):
        """Prints ASCII board in console"""
        rows = ""
        rim = " +------------------------+ \n"
        letters = "   A  B  C  D  E  F  G  H  \n"
        for y in range(1, 9):
            row = ""
            for x in range(1, 9):
                if self.board[(x, y)]:
                    piece_info = self.board[(x, y)]
                    piece = piece_info.get("piece")
                    if piece_info.get("color") == "w":
                        print_color = "\033[92m"
                    elif piece_info.get("color") == "b":
                        print_color = "\033[91m"
                else:
                    piece = "."
                    print_color = "\033[0m"
                row = row + " " + print_color + piece + "\033[0m" + " "
            rows = str(y) + "|" + row + "|" + str(y) + "\n" + rows
        return print(f"{letters}{rim}{rows}{rim}{letters}")

    def get_moves(self, start):
        """Gets possible moves for specific piece based off its location"""
        moves = chess_moves.Pieces_Moves(self.board, self.info)
        return moves.get_moves(start)            

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
                if move[3]: 
                    stale_count = 0
                else:
                    stale_count = self.info["stale_count"] + 1
                check = (False, False)
                check = self.check_status(end)
                return (
                self.board,
                    {
                        "turn": self.info["turn"] + 1,
                        "check": check[0],
                        "mate": check[1],
                        "en_passant": move[2],
                        "history": self.info["history"] + [f"{start[0]}{start[1]}{end[0]}{end[1]}"],
                        "stale_count": stale_count,
                        "castling": None
                    }
                )
        return (False, "Invalid move")

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
                        moves = []
                        color = attack["color"]
                        for position, piece in self.board.items():
                            if piece:
                                if piece.get("color", False) == color:
                                    get_moves = chess_moves.Pieces_Moves(self.board, self.info)
                                    moves.append(get_moves.get_moves(position))
                            if len(moves) == 0:
                                mate = True
        return (check, mate)

    def check_mate(self):
        """checks for game over / check mate status"""
        if self.info["mate"]:
            if self.info["turn"] % 2 == 0:
                player = "White"
            else:
                player = "Black"
            return player
        return False

    def request_move(self, turn):
        """request move as CLI input"""
        valid = False
        while not valid:
            start = input("Move from:")
            end = input("Move to:")
            if len(start) != 2 or len(end) != 2:
                square = False
                print("Invalid entry, try again")            
            start = (ord(start[0])-96, int(start[1]))
            end = (ord(end[0])-96, int(end[1]))
            square = True
            if square:
                for number in start[0], start[1], end[0], end[1]:
                    if number not in range(1,9):
                        square = False
                        print("invalid square, try again")
            if square:
                if not self.board[start]:
                    print("Empty start square, try again")
                elif self.board[start].get("color", False) == "turn":
                    print("Invalid move, other players turn, try again")
                else:
                    for move in self.get_moves(start):
                        if end == move[0]:
                            valid = True
                            return (start, move)
                    print("invalid move, try again")
            
    def ai_random(self, color):
        """gets random move"""
        ai_moves = ai_algo.AI_Moves(self.board, self.info)
        return ai_moves.random_move(color)

    def game_update(self, move):
        start = move[0]
        move = move[1]
        piece = self.board[start]
        if move[1]:
            self.board[move[1]] = None
        self.board[start] = None
        self.board[move[0]] = piece
        self.info["turn"] += 1
        self.info["history"].append("".join(str(x) for x in [start[0], start[1], move[0][0], move[0][1]]))
        if move[3] and move[3] in "phbrq":
            self.info["stale_count"] = 0
        else:
            self.info["stale_count"] += 1
        return [self.board, self.info]

    def play(self, move = None):
        """general play function"""
        if self.info["turn"] % 2 == 0:
            turn = "b"
        else:
            turn = "w"
        if turn == "w":
            player = self.player_white
        else:
            player = self.player_black
        if self.print_board:
            self.ascii()
        player_fork = {
            "human": self.request_move,
            "ai_random": self.ai_random,
            # "ai_min_max": ai_function()
        }
        return player_fork[player](turn)

    def swap_eligible(self):
        for position, piece in self.board.items():
            if position[1] == 1 or position[1] == 8:
                if piece and piece["piece"] == "p":
                    return position
        return False

    def swap(self, piece, position):
        self.board[position]["piece"] = piece

def main():
    game = Game(board_reset(), "human", "ai_random", True, None)
    end_game = False
    while not end_game:
        board = game.game_update(game.play())
        if board[1]["stale_count"] == 50:
            end_game = "stale"
        end_game = game.check_mate()
    status = {
        "stale": "*** Stale Mate! Game over! ***",
        "white": "*** Check Mate! White wins the game! ***",
        "black": "*** Check Mate! Black wins the game! ***",
    }
    print(status[end_game])

if __name__ == "__main__":
    main()