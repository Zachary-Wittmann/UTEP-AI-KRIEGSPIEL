import random
from copy import deepcopy

class Player:
    def __init__(self, player, board_file=None):
        self.player_pieces = [] # available player pieces
        self.board = []
        self.board_pieces = []
        self.player = player # player = "white", player = "black"
        if board_file:
            self.load_board_from_file(board_file)
    
    def load_board_from_file(self, board_file):
        """Load the board from a .txt file. Parse from opponent pieces"""
        with open(board_file, "r") as file:
            #self.board = [line.strip().split() for line in file.readlines()]
            board = []
            player_pieces = []
            for line in file.readlines():
                pieces = line.split()
                for i in range(len(pieces)):
                    if self.player == "W":
                        player_pieces.append(pieces)
                        if pieces[i][0] == 'B':
                            pieces[i] = 'O'
                    if self.player == "B":
                        player_pieces.append(pieces)
                        if pieces[i][0] == 'W':
                            pieces[i] = 'O'
                board.append(pieces)
            self.board = board
            self.player_pieces = player_pieces
        return self.board , self.player_pieces

    def choose_piece_human(self): # human chooses piece
        piece = input("Choose a piece to move.")
        return piece
    
    def choose_piece_pc(self):  # computer chooses piece
        piece = random.choice(self.player_pieces)
        return piece

    def make_move_human(self, piece): # human move
        move_row, move_column = map(int, input("Enter "+piece+" move(row, column, ex: 4 5):").split())
        return move_row, move_column
    
    def make_move_pc(self): # computer move
        move_row = 0 # current placeholder
        move_column = 0 # current placeholder
        return move_row, move_column
    
    def _get_board(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != 'O':
                    self.board_pieces.append([row, col])
                else:
                    pass
        return self.board_pieces

    
               

    def __str__(self):
        """Return a string representation of the board."""
        print(self._get_board())
        return "\n".join([" ".join(row) for row in self.board])

if __name__ == "__main__":
    state = Player("W", board_file="boards/test2.txt")
    print("Initial Board State:")
    print(state)

