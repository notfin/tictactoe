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
    X_count = 0
    O_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                X_count += 1
            if board[i][j] == O:
                O_count += 1
    if X_count == 0 and O_count == 0: # board is empty
        return X
    if X_count > O_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check that action is valid for board
    if action not in actions(board):
        raise Exception

    # deep copy board
    board_copy = copy.deepcopy(board)

    # check which player's move it is
    curr_player = player(board_copy)

    # update board with X or O (based on player)
    board_copy[action[0]][action[1]] = curr_player

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(3): # vertical win
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            return board[row][0]
    for col in range(3): # horizontal win
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            return board[0][col]

    if board[0][0] == board[1][1] and board[1][1] == board[2][2]: #downward diagonal
        return board[0][0]
    if board[2][0] == board[1][1] and board[1][1] == board[0][2]: #downward diagonal
        return board[2][0]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not winner(board) == None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def max_value(board, alpha, beta):
    if terminal(board):
        return (utility(board), (0,0))
    v = -math.inf
    max_action = ()

    for action in actions(board):
        curr_min = min_value(result(board, action), alpha, beta)[0]
        if curr_min > v:
            max_action = action
        v = max(v, curr_min)
        alpha = max(alpha, v)
        if beta <= alpha:
            break
    return (v, max_action)


def min_value(board, alpha, beta):
    if terminal(board):
        return (utility(board), (0,0))
    v = math.inf
    min_action = ()

    for action in actions(board):
        curr_max = max_value(result(board, action), alpha, beta)[0]
        if curr_max < v:
            min_action = action
        v = min(v, curr_max)
        beta = min(beta, v)
        if beta <= alpha:
            break
    return (v, min_action)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X: # maximizing player
        max_move = max_value(board, -math.inf, math.inf)[1]
        return max_move
    else: # minimizing player
        min_move = min_value(board, -math.inf, math.inf)[1]
        return min_move


#############################
# Tests

empty_board = initial_state()
X_moves_board = [[X, EMPTY, O],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
O_moves_board = [[EMPTY, X, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, X, EMPTY]]
one_move_board = [[O, X, O],
                    [X, O, X],
                    [EMPTY, X, O]]
O_won = [[O, X, O],
        [X, O, X],
        [X, X, O]]
X_won = [[X, X, X],
        [O, O, X],
        [X, O, O]]
tie_board = [[O, X, O],
            [O, X, X],
            [X, O, X]]
O_will_move = [[X, EMPTY, X],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, O]]
X_will_win = [[X, O, X],
            [O, O, X],
            [EMPTY, EMPTY, EMPTY]]
O_will_win = [[X, O, X],
            [O, O, X],
            [EMPTY, EMPTY, EMPTY]]
tie = [[X, O, X],
      [O, EMPTY, X],
      [EMPTY, X, O]]
tie_in_two = [[EMPTY, X, O],
            [O, X, X],
            [X, EMPTY, O]]

assert player(empty_board) == X
assert player(X_moves_board) == X
assert player(O_moves_board) == O
assert actions(one_move_board) == {(2, 0)}
assert actions(O_moves_board) == {(0,0), (0,2), (1,0), (1,2), (2,0), (2,2)}
assert result(O_moves_board, (0,0)) ==  [[O, X, EMPTY],
            [EMPTY, O, EMPTY],
            [EMPTY, X, EMPTY]]
assert result(empty_board, (2,2)) ==  [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, X]]
assert result(X_moves_board, (0,1)) ==  [[X, X, O],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
assert winner(one_move_board) == O
assert winner(O_won) == O
assert winner(O_moves_board) == None
assert terminal(X_won) == True
assert terminal(one_move_board) == True
assert terminal(X_moves_board) == False
assert utility(X_won) == 1
assert utility(one_move_board) == -1
assert utility(tie_board) == 0
assert minimax(one_move_board) == None
assert minimax(O_will_move) == (0, 1)
assert minimax(X_will_win) == (2,2)
assert minimax(tie) == (1,1)
assert minimax(tie_in_two) == (2,1)
assert minimax(empty_board) == (0,1)



