import numpy as np
import random
from observer import Observer
import tensorflow as tf
import math
from copy import copy, deepcopy
YELLOW_PLAYER = 1
RED_PLAYER = -1

PLAYERS = {1: "Yellow", -1: "Red"}

EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4


class Node():
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state  # Instance of Connect4Game
        self.children = []
        self.children_move = []
        self.parent = parent

    def add_child(self, child_state, move):
        child = Node(child_state, parent=self)
        self.children.append(child)
        self.children_move.append(move)

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_explored(self):
        if len(self.children) == len(self.state.get_valid_locations()):
            return True
        return False


class Bot(Observer):

    def __init__(self, game, bot_type=None, model=None):
        self._game = game
        # Bot type determines how the bot picks his moves
        self._type = bot_type

        #print("Created bot of type " + str(self._type))
        self._model = None
        if model is not None:
            self._model = model

    def update(self, obj, event, *argv):
        print(obj)

    def drop_piece(self, board, row, col, piece):
        # print(col, row)
        board[col][row] = piece

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[col][r] == 0:
                return r

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[c][r] == piece and board[c+1][r] == piece and board[c+2][r] == piece and board[c+3][r] == piece:
                    # print("horizontal")
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[c][r] == piece and board[c][r+1] == piece and board[c][r+2] == piece and board[c][r+3] == piece:
                    # print("vertical")
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[c][r] == piece and board[c+1][r+1] == piece and board[c+2][r+2] == piece and board[c+3][r+3] == piece:
                    # print("pdiago")
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[c][r] == piece and board[c+1][r-1] == piece and board[c+2][r-2] == piece and board[c+3][r-3] == piece:
                    # print("ndiago")
                    return True
        return False

    def is_terminal_node(self, board):
        # print(self.winning_move(board, self._game._turn*-1) or self.winning_move(board,
        #                                                                          self._game._turn) or self.get_valid_locations(board) is None)
        return self.winning_move(board, self._game._turn*-1) or self.winning_move(board, self._game._turn) or self.get_valid_locations(board) is None

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self._game._turn*-1
        if piece == self._game._turn*-1:
            opp_piece = self._game._turn

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0
        # Score center column
        center_array = [int(i) for i in list(board[COLUMN_COUNT//2][:])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[:][r])]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[c][:])]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # Score posiive sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[c+i][r+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[c+i][r+3-i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self._game._turn):
                    return (None, math.inf)
                elif self.winning_move(board, self._game._turn*-1):
                    return (None, -math.inf)
                else:  # Game is over, no more valid moves
                    # print("WHAT 3")
                    return (None, 0)
            else:  # Depth is zero
                # print("kaka")
                return (None, self.score_position(board, self._game._turn))
        elif maximizingPlayer:
            # print("depth ", depth)
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)

                b_copy = []
                for i in range(0, len(board)):
                    b_copy.append(board[i].copy())
                # b_copy = deepcopy(board)
                # if(row is not None and col is not None):
                self.drop_piece(b_copy, row, col, self._game._turn)
                new_score = self.minimax(
                    b_copy, depth-1, alpha, beta, False)[1]
                # print(new_score)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = []
                for i in range(0, len(board)):
                    b_copy.append(board[i].copy())
                # b_copy = deepcopy(board)
                # if(row is not None and col is not None):
                self.drop_piece(b_copy, row, col, self._game._turn*-1)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def monte_carlo_tree_search(self, iterations, root, factor):
        """
            Main function of MCTS
        """
        for i in range(iterations):
            front, turn = self.tree_policy(root, 1, factor)
            # print(turn)
            reward = self.default_policy(front.state, turn)
            #print("reward:", reward)
            self.backup(front, reward, turn)

        ans = self.best_child(root, 0)
        #print("ANS:", ans.state.last_move[1])
        #print([(c.reward/c.visits) for c in ans.parent.children])
        #print([c.reward for c in ans.parent.children])
        return ans.state.last_move[0]

    def tree_policy(self, node, turn, factor):
        """
            Expands the root node and takes the best child everytime until we reach a winning
            state.
        """
        #turn = node.state._turn
        a = 0
        while not node.state.last_move or not node.state.check_win(node.state.last_move):
            if not node.fully_explored():
                #print("FULLY EXPLORED")
                return self.expand(node, turn), -turn
            else:
                # print(a)
                node = self.best_child(node, factor)
                # print(node.state.last_move)
                b = node.state.check_win(node.state.last_move)
                # print(node.state._board)
                turn *= -1
                # if not b:
                #     exit(2)
                #print("TURN2:", turn)
            a += 1

        return node, turn

    def expand(self, node, turn):
        """
            Add a child state to the node
        """
        tried_children_move = [m for m in node.children_move]
        free_cols = node.state.get_valid_locations()

        for col in free_cols:
            if col not in tried_children_move:
                new_state = node.state.copy_state()
                # print(node.state._board)
                new_state.place(col)
                # print(node.state._board)
                # print(new_state._board)
                #new_state.last_move = [col]
                break

        node.add_child(new_state, col)
        return node.children[-1]

    def backup(self, node, reward, turn):
        #print("turn", turn)
        while node != None:
            node.visits += 1
            node.reward -= turn*reward
            #print("node reward", node.reward)
            node = node.parent
            turn *= -1
        return

    def default_policy(self, state_a, turn):
        """
            Simulates random moves until the game is won by someone and returns a
            reward.
        """
        state = state_a.copy_state()
        while not state.last_move or not state.check_win(state.last_move):
            free_cols = state.get_valid_locations()
            col = random.choice(free_cols)
            state.place(col)
            turn *= -1

        reward_bool = state.check_win(state.last_move)
        if reward_bool and turn == -1:
            reward = 1
        elif reward_bool and turn == 1:
            reward = -1
        else:
            # print("PROBLEM")
            reward = 0
        return reward

    def best_child(self, node, factor):
        best_score = -10000000.0
        best_children = []
        for c in node.children:
            exploit = c.reward / c.visits
            explore = math.sqrt(math.log(2.0*node.visits)/float(c.visits))
            score = exploit + factor*explore
            if score == best_score:
                best_children.append(c)
            if score > best_score:
                best_children = [c]
                best_score = score
        # print(best_score)
        res = random.choice(best_children)
        # print(res.state._board)
        return res

    def make_move(self):
        """
            Picks the column in which the bot should place the next disc.
            The considered moving options depend on the bot type.

            :return: the column number where the bot should play the next move
        """
        #print(PLAYERS[self._game._turn] + " is about to play :")
        column = None
        # In case the bot type is 0, the bot checks for winning moves, and if there aren't,
        # then picks a valid random move.
        if self._type == 0:
            win_col = self.get_winning_move()
            if win_col is not None:
                column = win_col
            else:
                column = self.get_random_move()
        # In case the bot type is 1, the bot checks for winning moves, and if there aren't,
        # then checks if there is any move that blocks a direct winning move for the opponent.
        # If there is no such move, it picks a valid random move.
        elif self._type == 1:
            win_col = self.get_winning_move()
            if win_col is not None:
                #print("Winning column :", win_col)
                column = win_col
            else:
                def_move = self.get_defensive_move()
                if def_move is not None:
                    #print("Defensive column :", def_move)
                    column = def_move
                else:
                    column = self.get_random_move()
                    #print("Random move", column)
        elif self._type == 2:
            column, minimax_score = self.minimax(
                self._game._board, 5, -math.inf, math.inf, True)
            # print(column)
        elif self._type == 3:
            o = Node(self._game.copy_state())
            column = self.monte_carlo_tree_search(100, o, 2.0)
        else:
            flat_board = [
                [item for sublist in self._game._board for item in sublist]]
            # print(flat_board)
            if self._game._turn == -1:
                flat_board *= -1
            output = self._model.predict(flat_board)
            output = output[0]
            free_cols = []
            for i in range(len(self._game._board)):
                if self._game._board[i][self._game._rows-1] == 0:
                    free_cols.append(i)

            found = False
            while not found:
                column = np.argmax(output)
                if sum(output) == 0:
                    column = self.get_random_move()
                if column in free_cols:
                    found = True
                else:
                    output[column] = 0

        # print("-------------------------")
        self._game.place(column)

    def get_winning_move(self):
        """
            Checks whether there is a winning column available for the next
            move of the bot.

            :return: winning column
        """
        column = None
        for c_win in range(self._game._cols):
            for r in range(self._game._rows):
                if self._game._board[c_win][r] == 0:
                    self._game._board[c_win][r] = self._game._turn
                    is_winner = self._game.check_win((c_win, r))
                    self._game._board[c_win][r] = 0
                    if is_winner:
                        column = c_win
                        return column
                    break
        return column

    def get_valid_locations(self, board):
        free_cols = []
        for i in range(COLUMN_COUNT):
            if board[i][ROW_COUNT-1] == 0:
                free_cols.append(i)
                # print()
        if len(free_cols) == 0:
            return None
        return free_cols

    def get_random_move(self):
        """
            Picks a valid random column where the bot can play his next move.

            :return: valid random column 
        """
        free_cols = self.get_valid_locations(self._game._board)
        column = random.choice(free_cols)
        return column

    def get_defensive_move(self):
        """
            Checks whether the bot could play a move that blocks a direct winning
            move from the opponent.

            :return: column to be played to avoid losing immediatly
        """
        column = None
        for c_win in range(self._game._cols):
            for r in range(self._game._rows):
                if self._game._board[c_win][r] == 0:
                    self._game._board[c_win][r] = -1*self._game._turn
                    is_winner = self._game.check_win((c_win, r))
                    self._game._board[c_win][r] = 0
                    if is_winner:
                        column = c_win
                        return column
                    break
        return column
