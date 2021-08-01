"""
Tic Tac Toe Player
"""
import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = count_o = 0
    for row in board:
        for cell in row:
            if cell == X:
                count_x += 1
            elif cell == O:
                count_o += 1
    return O if count_x > count_o else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                action_set.add((i, j))
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise IOError("Requested Action is Invalid")

    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)

    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Find out which player just moved (and is thus a candidate for winning the game)
    current_player = X if player(board) is O else O

    # Just using a dictionary for sake of readability
    score_dict = {"row": 0, "column": 0, "diagonal": 0, "lanogaid": 0}

    for i in range(3):
        if board[i][i] is current_player:
            score_dict["diagonal"] += 1
        if board[i][2-i] is current_player:
            score_dict["lanogaid"] += 1
        score_dict["row"] = 0
        score_dict["column"] = 0
        for j in range(3):
            if board[i][j] is current_player:
                score_dict["row"] += 1
            if board[j][i] is current_player:
                score_dict["column"] += 1
        # not very efficient sadly
        if 3 in score_dict.values():
            return current_player
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return bool(winner(board) is not None or is_full(board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) is X:
        return 1
    if winner(board) is O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # In case provided state is terminal
    if terminal(board):
        return None
    # determine current player and iterate over each action availible to them
    current_player = player(board)
    if current_player is X:
        current_action_val = float('-inf')
        beta = float('inf')
        for action in actions(board):
            candidate_val = min_value(result(board, action), current_action_val, beta)
            if candidate_val > current_action_val:
                current_action = action
                current_action_val = candidate_val
    else:
        current_action_val = float('inf')
        alpha = float('-inf')
        for action in actions(board):
            candidate_val = max_value(result(board, action), alpha, current_action_val)
            if candidate_val < current_action_val:
                current_action = action
                current_action_val = candidate_val

    return current_action


def max_value(state, alpha, beta):
    """
    Returns maximum value of given state
    """
    val = float('-inf')
    if terminal(state):
        return utility(state)

    for action in actions(state):
        val = max(val, min_value(result(state, action), alpha, beta))
        alpha = max(alpha, val)
        if val >= beta:
            return val
    return val


def min_value(state, alpha, beta):
    """
    Returns minimum value of given state
    """
    val = float('inf')
    if terminal(state):
        return utility(state)

    for action in actions(state):
        val = min(val, max_value(result(state, action), alpha, beta))
        beta = min(beta, val)
        if val <= alpha:
            return val
    return val


def is_full(board):
    """
    Returns True if all squares are occupied by a player, and false otherwise
    """
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False
    return True
