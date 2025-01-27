import copy
import random

# 定数定義
BLACK = 1  # 黒石
WHITE = 2  # 白石

# 6x6の初期状態のオセロボードを定義
board = [
    [0, 0, 0, 0, 0, 0],  # 0は空きマスを表す
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],  # 中央に黒石(1)と白石(2)が配置されている
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# ボード上の位置に対するスコア
POSITION_SCORES = [
    [100, -20, 10, 10, -20, 100],
    [-20, -50, -2, -2, -50, -20],
    [10, -2, 1, 1, -2, 10],
    [10, -2, 1, 1, -2, 10],
    [-20, -50, -2, -2, -50, -20],
    [100, -20, 10, 10, -20, 100],
]

def evaluate_board(board, stone):
    """
    現在の盤面の評価値を計算する。
    """
    score = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += POSITION_SCORES[y][x]
            elif board[y][x] == (3 - stone):
                score -= POSITION_SCORES[y][x]
    return score

def can_place_x_y(board, stone, x, y):
    """
    指定した位置 (x, y) に stone の石を置けるかを判定する。
    """
    if board[y][x] != 0:  # 空きマスでない場合は置けない
        return False

    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            found_opponent = True
            nx += dx
            ny += dy

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True

    return False

def apply_move(board, stone, x, y):
    """
    指定した位置に石を置いた後の新しい盤面を返す。
    """
    new_board = copy.deepcopy(board)
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    new_board[y][x] = stone

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flipped_positions = []

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == opponent:
            flipped_positions.append((nx, ny))
            nx += dx
            ny += dy

        if 0 <= nx < len(board[0]) and 0 <= ny < len(board) and new_board[ny][nx] == stone:
            for px, py in flipped_positions:
                new_board[py][px] = stone

    return new_board

def minimax(board, stone, depth, maximizing_player):
    """
    ミニマックス法を用いて最善の手を探索する。
    """
    if depth == 0:
        return evaluate_board(board, stone), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    new_board = apply_move(board, stone, x, y)
                    eval, _ = minimax(new_board, stone, depth - 1, False)
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (x, y)
        return max_eval, best_move

    else:
        min_eval = float('inf')
        opponent = 3 - stone
        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, opponent, x, y):
                    new_board = apply_move(board, opponent, x, y)
                    eval, _ = minimax(new_board, stone, depth - 1, True)
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (x, y)
        return min_eval, best_move
        
def find_valid_moves(board, stone):
    """
    現在の盤面で stone を置けるすべての合法手をリストとして返す。
    """
    valid_moves = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                valid_moves.append((x, y))
    return valid_moves

class nekosanAI:
    """
    ミニマックス法を用いたAI。
    """
    def __init__(self, depth=3):
        self.depth = depth

    def face(self):
        return "🐱"

    def place(self, board, stone):
        """
        ミニマックス法を用いて最善の手を計算する。
        """
        valid_moves = find_valid_moves(board, stone)  # 置ける場所を探す
        if not valid_moves:  # 置ける場所がない場合
            return (-1, -1)  # パスを示す

        _, best_move = minimax(board, stone, self.depth, True)
        return best_move if best_move in valid_moves else valid_moves[0]

