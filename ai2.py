import copy

# 定数定義
BLACK = 1  # 黒石
WHITE = 2  # 白石

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
    現在の盤面の評価値を計算する（位置スコア + モビリティ）。
    """
    score = 0
    # 位置スコアを計算
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += POSITION_SCORES[y][x]
            elif board[y][x] == (3 - stone):
                score -= POSITION_SCORES[y][x]
    # モビリティの計算を追加
    player_moves = len(find_valid_moves(board, stone))
    opponent_moves = len(find_valid_moves(board, 3 - stone))
    mobility_score = player_moves - opponent_moves
    score += mobility_score * 5  # モビリティの重み
    return score

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

def can_place_x_y(board, stone, x, y):
    """
    指定した位置 (x, y) に stone の石を置けるかを判定する。
    """
    if board[y][x] != 0:
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

def alphabeta(board, stone, depth, alpha, beta, maximizing_player):
    """
    アルファベータ法を用いた最善の手の探索。
    """
    if depth == 0:
        return evaluate_board(board, stone), None

    valid_moves = find_valid_moves(board, stone if maximizing_player else 3 - stone)
    if not valid_moves:
        return evaluate_board(board, stone), None

    best_move = None

    if maximizing_player:
        max_eval = float('-inf')
        for x, y in valid_moves:
            new_board = apply_move(board, stone, x, y)
            eval, _ = alphabeta(new_board, stone, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = (x, y)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move

    else:
        min_eval = float('inf')
        opponent = 3 - stone
        for x, y in valid_moves:
            new_board = apply_move(board, opponent, x, y)
            eval, _ = alphabeta(new_board, stone, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = (x, y)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

class nekosanAI:
    """
    アルファベータ法、モビリティ、終盤の完全探索を備えた強化AI。
    """
    def __init__(self, depth=3, endgame_depth=8):
        self.depth = depth
        self.endgame_depth = endgame_depth  # 終盤用の探索深さ

    def face(self):
        return "🐱"

    def place(self, board, stone):
        """
        アルファベータ法を用いて最善の手を計算する。
        終盤では完全探索を行う。
        """
        remaining_moves = len(find_valid_moves(board, stone)) + len(find_valid_moves(board, 3 - stone))
        if remaining_moves <= 12:  # 終盤と判断
            _, best_move = alphabeta(board, stone, self.endgame_depth, float('-inf'), float('inf'), True)
        else:
            _, best_move = alphabeta(board, stone, self.depth, float('-inf'), float('inf'), True)
        return best_move if best_move else (-1, -1)
