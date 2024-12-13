import random
from copy import deepcopy


class GameState:
    def __init__(self, board_file=None):
        self.board = []
        self.board_pieces = []
        self.current_player = "W"  # White starts the game by default
        if board_file:
            self.load_board_from_file(board_file)
            self._get_board()

    def load_board_from_file(self, board_file):
        """Load the board from a .txt file."""
        with open(board_file, "r") as file:
            self.board = [line.strip().split() for line in file.readlines()]

    def get_legal_moves(self, player):
        """Return a list of legal moves for the given player."""
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece.startswith(player):
                    legal_moves.extend(self._get_piece_moves(piece, row, col))
        #print(legal_moves)
        return legal_moves
    
    def _get_board(self):
        for row in range(8):
            for col in range(8):
                if self.board[row][col] != 'O':
                    self.board_pieces.append([row, col])
                else:
                    pass
        return self.board_pieces

    def _get_piece_moves(self, piece, row, col):
        """Get legal moves for a specific piece."""
        moves = []
        if "P" in piece: # pawn
            moves = self._get_pawn_moves(row, col, piece.startswith("W"))
        elif "N" in piece: # knight
            moves = self._get_knight_moves(row, col)
        elif "A" in piece: # bishop
            moves = self._get_bishop_moves(row, col)
        elif "R" in piece: # rook
            moves = self._get_rook_moves(row, col)
        elif "Q" in piece: # queen
            moves = self._get_queen_moves(row, col)
        elif "K" in piece: # king
            moves = self._get_king_moves(row, col)
        #print(piece, moves)
        #print("end")
        return moves

    def _get_pawn_moves(self, row, col, is_white):
        # Does not account for En Passant captures as of now
        moves = []
        direction = -1 if is_white else 1
        # Move forward
        if 0 <= row + direction < 8 and self.board[row + direction][col] == ".":
            moves.append((row, col, row + direction, col))
        # Capture diagonally
        for dc in [-1, 1]:
            nr, nc = row + direction, col + dc
            if (
                0 <= nr < 8
                and 0 <= nc < 8
                and self.board[nr][nc].startswith("B" if is_white else "W")
            ):
                moves.append((row, col, nr, nc))
        return moves

    def _get_knight_moves(self, row, col):
        moves = []
        knight_deltas = [
            (-2, 1),
            (-1, 2),
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
        ]
        for dr, dc in knight_deltas:
            nr, nc = row + dr, col + dc # nr, nc = new row, new column
            if (
                0 <= nr < 8
                and 0 <= nc < 8
                and not self.board[nr][nc].startswith(self.current_player)
            ):
                moves.append((row, col, nr, nc))
        return moves

    def _get_bishop_moves(self, row, col):
        moves = []
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nr, nc = row, col
            while True:
                nr, nc = nr + dr, nc + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if [nr, nc] in self.board_pieces:
                        nr = 9
                        break
                    if self.board[nr][nc] == ".":
                        moves.append((row, col, nr, nc))
                        break
                    elif self.board[nr][nc].startswith(self.current_player):
                        break
                    else:
                        moves.append((row, col, nr, nc))
                        break
                else:
                    break
        return moves

    def _get_rook_moves(self, row, col):
        moves = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row, col
            while True:
                nr, nc = nr + dr, nc + dc
                while 0 <= nr < 8 and 0 <= nc < 8:
                    if [nr, nc] in self.board_pieces:
                        nr = 9
                        break
                    if self.board[nr][nc] == ".":
                        moves.append((row, col, nr, nc))
                        break
                    elif self.board[nr][nc].startswith(self.current_player):
                        break
                    else:
                        moves.append((row, col, nr, nc))
                        break
                else:
                    break
        #print(moves)
        return moves

    def _get_queen_moves(self, row, col):
        return self._get_bishop_moves(row, col) + self._get_rook_moves(row, col)

    def _get_king_moves(self, row, col):
        moves = []
        king_deltas = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for dr, dc in king_deltas:
            nr, nc = row + dr, col + dc
            if (
                0 <= nr < 8
                and 0 <= nc < 8
                and not self.board[nr][nc].startswith(self.current_player)
            ):
                moves.append((row, col, nr, nc))
        return moves
    
    def is_king_in_check(self):
        """Check if the king is in check."""
        opponent_player = 'W' if self.current_player == 'B' else 'B'
        king_row, king_col = None, None
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == opponent_player + 'K':
                    king_row, king_col = row, col
                    break
        if king_row is None or king_col is None:
            return False
 
        knight_row, knight_col = None, None
        bishop_row, bishop_col = None, None
        rook_row, rook_col = None, None
        queen_row, queen_col = None, None
        pawn_row, pawn_col = None, None
 
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.current_player + 'N':
                    knight_row, knight_col = row, col
                    break
 
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.current_player + 'A':
                    bishop_row, bishop_col = row, col
                    break
 
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.current_player + 'R':
                    rook_row, rook_col = row, col
                    break
 
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.current_player + 'Q':
                    queen_row, queen_col = row, col
                    break
 
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == self.current_player + 'P':
                    pawn_row, pawn_col = row, col
                    break
 
        if knight_row is not None and knight_col is not None:
            knight_moves = self._get_knight_moves(knight_row, knight_col)
            for move in knight_moves:
                if move[2] == king_row and move[3] == king_col:
                    return True
 
        if pawn_row is not None and pawn_col is not None:
            pawn_moves = []
            if opponent_player == 'W':
                pawn_moves = self._get_pawn_moves(pawn_row, pawn_col, True)
            else:
                pawn_moves = self._get_pawn_moves(pawn_row, pawn_col, False)
            for move in pawn_moves:
                if move[2] == king_row and move[3] == king_col:
                    return True
 
        if bishop_row is not None and bishop_col is not None:
            bishop_moves = self._get_bishop_moves(bishop_row, bishop_col)
            for move in bishop_moves:
                if move[2] == king_row and move[3] == king_col:
                    return True
 
        if rook_row is not None and rook_col is not None:
            rook_moves = self._get_rook_moves(rook_row, rook_col)
            for move in rook_moves:
                if move[2] == king_row and move[3] == king_col:
                    return True
 
        if queen_row is not None and queen_col is not None:
            queen_moves = self._get_queen_moves(queen_row, queen_col)
            for move in queen_moves:
                if move[2] == king_row and move[3] == king_col:
                    return True
        return False
    
    def stalemate(self):
        """Check if the game is in a stalemate."""
        opponent_player = 'W' if self.current_player == 'B' else 'B'
        king_row, king_col = None, None
        if self.is_king_in_check() == False:
            for row in range(8):
                for col in range(8):
                    if self.board[row][col] == opponent_player + 'K':
                        king_row, king_col = row, col
                        break
            if king_row is None or king_col is None:
                return False
            if self.get_legal_moves(opponent_player) == []:
                return True
        return False

    def make_move(self, move):
        """Apply a move to the board and return a new game state."""
        src_row, src_col, dest_row, dest_col = move
        new_board = deepcopy(self.board)
        new_board[dest_row][dest_col] = new_board[src_row][src_col]
        new_board[src_row][src_col] = "."
        new_state = GameState()
        new_state.board = new_board
        new_state.current_player = "B" if self.current_player == "W" else "W"
        return new_state

    def is_game_over(self):
        """Check if the game is over."""
        return not any("WK" in row for row in self.board) or not any(
            "BK" in row for row in self.board
        )

    def evaluate(self, player):
        """Evaluate the game from the player's perspective."""
        if self.is_king_in_check():
            return -1 if player == "W" else 1
        if not any("WK" in row for row in self.board):
            return -1 if player == "W" else 1
        if not any("BK" in row for row in self.board):
            return 1 if player == "W" else -1
        return 0  # Draw or ongoing game

    def __str__(self):
        """Return a string representation of the board."""
        #print(self.stalemate())
        #print(self.board_pieces)
        return "\n".join([" ".join(row) for row in self.board])

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

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        """Check if all legal moves have been expanded."""
        return len(self.children) == len(
            self.state.get_legal_moves(self.state.current_player)
        )

    def best_child(self, exploration_weight=1.0):
        """Select the best child using UCB1."""
        return max(
            self.children,
            key=lambda child: child.value / (child.visits + 1)
            + exploration_weight * (2 * (self.visits**0.5) / (child.visits + 1)),
        )


class MCTS:
    def __init__(self, exploration_weight=1.0):
        self.exploration_weight = exploration_weight

    def search(self, state, simulations=1000):
        root = MCTSNode(state)
        for _ in range(simulations):
            node = self._select(root)
            reward = self._simulate(node.state)
            self._backpropagate(node, reward)
        return root.best_child(0).state

    def _select(self, node):
        """Select a node to expand."""
        while not node.state.is_game_over() and node.is_fully_expanded():
            node = node.best_child(self.exploration_weight)
        if not node.state.is_game_over():
            self._expand(node)
        return random.choice(node.children) if node.children else node

    def _expand(self, node):
        """Expand the node by adding a new child node."""
        moves = node.state.get_legal_moves(node.state.current_player)
        for move in moves:
            if not any(
                child.state == node.state.make_move(move) for child in node.children
            ):
                child_state = node.state.make_move(move)
                node.children.append(MCTSNode(child_state, node))

    def _simulate(self, state):
        """Simulate the game to the end and return the reward."""
        current_state = deepcopy(state)
        while not current_state.is_game_over():
            moves = current_state.get_legal_moves(current_state.current_player)
            if not moves:
                break
            move = random.choice(moves)
            current_state = current_state.make_move(move)
            #print("")
            #print(state)
        return current_state.evaluate(state.current_player)

    def _backpropagate(self, node, reward):
        """Backpropagate the reward up the tree."""
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent


# Example Usage
if __name__ == "__main__":
    state = GameState(board_file="boards/test3.txt")
    print("Initial Board State:")
    print(state)

    mcts = MCTS()
    best_state = mcts.search(state, simulations=5000)
    print("\nBest Move Board State:")
    print(best_state)
